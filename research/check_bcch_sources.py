"""Check candidate sources on a GitHub runner and save public summaries."""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


ENDPOINT = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
CANDIDATES = {
    "real_gdp": "F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T",
    "headline_inflation": "G073.IPC.V12.2023.M",
    "core_inflation": "G073.IPCSV.V12.2023.M",
    "policy_rate": "F022.TPM.TIN.D001.NO.Z.D",
    "nominal_bond_2y": "F022.BCLP.TIS.AN02.NO.Z.D",
    "nominal_bond_5y": "F022.BCLP.TIS.AN05.NO.Z.D",
    "nominal_bond_10y": "F022.BCLP.TIS.AN10.NO.Z.D",
    "inflation_compensation_5y": "F022.BOSP.TAS.AN05.Z.Z.D",
    "copper": "F019.PPB.PRE.40.M",
    "observed_usd": "F073.TCO.PRE.Z.D",
    "trade_balance_candidate": "F068.B1.VAR.T0.0.S.N.Z.Z.Z.Z.6.0.M",
    "exports_china": "F068.B1.FLU.Z.0.C.N.Z.Z.CN.Z.6.0.M",
    "exports_us": "F068.B1.FLU.Z.0.C.N.Z.Z.US.Z.6.0.M",
    "exports_total": "F068.B1.FLU.Z.0.C.N.Z.Z.Z.Z.6.0.M",
}


class SourceError(Exception):
    """An error message that contains public status information only."""


def request_json(token, parameters):
    query = urlencode({"token": token, **parameters})
    for attempt in range(3):
        try:
            with urlopen(f"{ENDPOINT}?{query}", timeout=35) as response:
                payload = json.load(response)
            if payload.get("Codigo") != 0:
                raise SourceError("API returned an unsuccessful response code")
            return payload
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise SourceError(f"HTTP status {error.code}") from None
        except (URLError, TimeoutError):
            if attempt == 2:
                raise SourceError("Network request failed after three attempts") from None
        time.sleep(attempt + 1)
    raise SourceError("Request did not complete")


def read_catalog(token, frequency):
    try:
        payload = request_json(token, {"function": "SearchSeries", "frequency": frequency})
        entries = payload.get("SeriesInfos")
        if not isinstance(entries, list):
            raise SourceError("Unexpected metadata response structure")
        return {"frequency": frequency, "status": "success", "entries": entries}
    except SourceError as error:
        return {"frequency": frequency, "status": "failed", "error": str(error), "entries": []}
    except Exception as error:
        return {"frequency": frequency, "status": "failed", "error": type(error).__name__, "entries": []}


def public_metadata(entry):
    fields = ("seriesId", "frequencyCode", "spanishTitle", "englishTitle",
              "firstObservation", "lastObservation", "updatedAt")
    return {field: entry.get(field) for field in fields}


def read_candidate(token, item, metadata, last_date):
    name, series_id = item
    result = {"name": name, "series_id": series_id}
    if series_id in metadata:
        result["metadata"] = public_metadata(metadata[series_id])
    try:
        payload = request_json(token, {
            "function": "GetSeries", "timeseries": series_id,
            "firstdate": "2010-01-01", "lastdate": last_date,
        })
        series = payload.get("Series") or {}
        if series.get("seriesId") != series_id:
            raise SourceError("Returned series identifier differs from requested identifier")
        rows = series.get("Obs")
        if not isinstance(rows, list):
            raise SourceError("Unexpected observations response structure")
        observations = {}
        statuses = Counter()
        for row in rows:
            status = row.get("statusCode")
            statuses[status] += 1
            if status != "OK":
                continue
            date = datetime.strptime(row["indexDateString"], "%d-%m-%Y").date().isoformat()
            value = float(row["value"])
            if not math.isfinite(value):
                continue
            if date in observations:
                raise SourceError("Duplicate observation date")
            observations[date] = value
        if not observations:
            raise SourceError("No valid observations returned in requested sample")
        dates = sorted(observations)
        result.update({
            "status": "success", "valid_observations": len(dates),
            "first_valid_date_in_requested_sample": dates[0],
            "latest_valid_date": dates[-1],
            "source_status_counts": dict(statuses),
            "sample_observations": [{"date": date, "value": observations[date]} for date in dates[-5:]],
        })
    except SourceError as error:
        result.update(status="failed", error=str(error))
    except Exception as error:
        result.update(status="failed", error=type(error).__name__)
    return result


def discover_candidates(metadata):
    results = {"sovereign_risk": [], "general_government_fiscal": [], "monthly_goods_trade": []}
    for entry in metadata.values():
        title = f"{entry.get('spanishTitle', '')} {entry.get('englishTitle', '')}".lower()
        if re.search(r"\bcds\b|\bembi\b|credit default|sovereign spread|spread soberano", title):
            results["sovereign_risk"].append(public_metadata(entry))
        if ("general government" in title or "gobierno general" in title) and re.search(
                r"gross debt|deuda bruta|net lending|net borrowing|endeudamiento neto|balance fiscal", title):
            results["general_government_fiscal"].append(public_metadata(entry))
        if entry.get("frequencyCode") == "MONTHLY" and re.search(
                r"balanza comercial|trade balance|bienes.*importaciones|goods.*imports", title):
            results["monthly_goods_trade"].append(public_metadata(entry))
    return results


def main():
    token = os.environ.get("BCCH_API_TOKEN", "").strip()
    if not token:
        print("BCCH_API_TOKEN is required for the authenticated source audit.")
        return 2
    started_at = datetime.now(timezone.utc)
    with ThreadPoolExecutor(max_workers=3) as executor:
        catalogs = list(executor.map(lambda frequency: read_catalog(token, frequency),
                                     ("DAILY", "MONTHLY", "QUARTERLY")))
    metadata = {entry["seriesId"]: entry for catalog in catalogs
                for entry in catalog["entries"] if entry.get("seriesId")}
    last_date = started_at.date().isoformat()
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(
            lambda item: read_candidate(token, item, metadata, last_date), CANDIDATES.items()))
    success = all(catalog["status"] == "success" for catalog in catalogs)
    success = success and all(result["status"] == "success" for result in results)
    report = {
        "purpose": "Source feasibility audit for dashboard planning",
        "started_at_utc": started_at.isoformat(timespec="seconds"),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "success" if success else "needs_attention",
        "requested_start": "2010-01-01", "requested_end": last_date,
        "catalog_checks": [{key: value for key, value in catalog.items() if key != "entries"}
                           | {"series_count": len(catalog["entries"])} for catalog in catalogs],
        "series_checks": results,
        "additional_candidates": discover_candidates(metadata),
    }
    public_report = json.dumps(report, ensure_ascii=True, indent=2).replace(token, "[redacted]")
    output = Path("research/results/bcch-source-check.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(public_report + "\n", encoding="utf-8")
    print(public_report)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())

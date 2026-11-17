# Chile source audit results

Source checks completed on 16 November 2026. The latest local audit completed at 23:35:20 UTC and retrieved 16 of 18 candidate BCCh series. Both country-export candidates returned API response code −50. The [public JSON report](../research/results/bcch-source-check.json) includes counts, source status codes, metadata, and observation samples.

The initial GitHub run exposed a response-decoding error. After support for UTF-8 and Windows-1252 was added, the [corrected GitHub run](https://github.com/greg-at-k/vitals-chile/actions/runs/43979985759) retrieved 12 of its 14 candidates. The local audit expanded the candidate list with four fiscal and GDP inputs. Both audits retain a `needs_attention` status for the rejected country-export codes.

## Retrieved series

| Series | Latest valid period in the requested sample | Access result |
| --- | --- | --- |
| Real GDP | 2026 Q2 | Downloaded |
| Headline inflation | October 2026 | Downloaded |
| Core inflation excluding volatile items | October 2026 | Downloaded |
| Policy rate | 16 November 2026 | Downloaded |
| Two-year nominal bond yield | 11 November 2026 | Downloaded |
| Five-year nominal bond yield | 12 November 2026 | Downloaded |
| Ten-year nominal bond yield | 12 November 2026 | Downloaded |
| Five-year bond inflation compensation | 16 November 2026 | Downloaded |
| Monthly copper price | October 2026 | Downloaded |
| Daily observed dollar | 16 November 2026 | Downloaded |
| Monthly trade-balance candidate | October 2026 | Downloaded |
| Total goods exports | October 2026 | Downloaded |
| General-government net lending or borrowing | 2026 Q2 | Downloaded |
| Gross general-government debt | 2026 Q2 | Downloaded |
| Nominal GDP | 2026 Q2 | Downloaded |
| National-accounts general-government balance ratio candidate | 2026 Q2 | Downloaded |

Quarterly API observations use quarter-start dates. The date `2026-04-01` therefore represents 2026 Q2. Monthly observations use month-start dates. Daily source metadata can extend beyond the requested sample, so this table uses actual valid observations within the request ending 16 November 2026.

The bond maturities have different latest observation dates. A valid snapshot needs their latest shared date, which will be calculated from the complete downloaded histories.

## Fiscal findings

The API provides DIPRES general-government inputs through `F051.B04.FLU.G.C.CLP.T` for net lending or borrowing and `F051.F2.STO.G.Z.CLP.T` for debt. Nominal GDP is available through `F032.PIB.FLU.N.CLP.EP18.Z.Z.0.T`.

The balance input has missing observations in the requested 2010-onward history. The full source-status counts are retained in the JSON report. Its metadata's first-observation date alone overstates the usable continuous history.

The separate national-accounts ratio candidate uses a different statistical framework from the DIPRES release. It remains a comparison candidate while the fiscal definition is finalized. The preferred DIPRES-based display can use downloaded amounts and a compatible trailing-year GDP denominator after units and vintages are verified.

## Trade findings

The country-series identifiers read from a public BDE basket are absent from the authenticated monthly catalog and fail through `GetSeries`. Their public-table appearance therefore does not establish API availability.

The public legacy country-trade workbook downloads successfully and includes an `X fob` export sheet. Its month headers extend only through February 2021 in the inspected copy. The legacy aggregate trade workbook also contains historical monthly and cumulative columns. A current automated destination source still needs to be established. [Official country workbook](https://si3.bcentral.cl/estadisticas/Principal1/Excel/SE/COMEX/xls/Balanza_comercial_por_paises_mensual.xls), [Official aggregate workbook](https://si3.bcentral.cl/estadisticas/Principal1/Excel/SE/COMEX/xls/Balanza_comercial.xls)

The proposed China and US shares remain in scope. Source work must identify a current BCCh download, a suitable official customs series, or another primary international dataset, then reconcile the export denominator.

## Sovereign risk

The daily, monthly, and quarterly API catalogs did not reveal a CDS or EMBI spread series under the searched names. A country-risk survey response appeared in discovery. That measures survey respondents' assessment of exchange-rate drivers and cannot supply the requested sovereign spread.

## Exchange rate inputs

Public IMF requests retrieved monthly histories from January 1976 onward. Chile CPI and CLP per USD extend through October 2026. US CPI extends through September 2026. The [initial IMF coverage report](../research/results/imf-source-check.json) records the 16 November checks.

The user selected a trailing 30-year benchmark on 17 November. A fresh check identifies October 1996–September 2026 as the current window. It contains 359 valid shared observations and one missing required-input month, October 2025. The arithmetic mean excludes that month, and the chart will retain the gap. The [benchmark check](../research/results/rer-benchmark-check.json) records the dates, valid count, and an independently checked identity relating actual and implied FX to the real index.

## Evidence scope

These results establish source access and candidate behavior for planning. Per-series comparisons with original releases and the completed dashboard's end-to-end refresh evidence remain implementation tasks. The initial encoding failure has been corrected and checked with both response encodings and a sanitized HTTP-error case.

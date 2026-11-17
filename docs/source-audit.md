# Chile source audit results

## Working implementation evidence — 17 November 2026

The first complete production-adapter refresh succeeded at 19:29:33 UTC, following a start at 19:28:14 UTC. Its record and underlying downloaded values are saved in `data/dashboard.json`. This run retrieved all configured available BCCh, IMF, and country-workbook inputs and calculated the dashboard figures before atomically replacing the file. Sovereign risk was explicitly excluded as unavailable.

Five automated tests passed: all Streamlit sections, viewing windows and reload; actual/implied FX identity; common-date curve and spread; twelve-month destination shares recomputed from source months; and propagation of a missing fiscal quarter. These checks establish calculation and app execution behavior. Browser rendering and original-release spot checks for every series remain incomplete. Public Streamlit deployment also remains outstanding.

The [hosted end-to-end refresh](https://github.com/greg-at-k/vitals-chile/actions/runs/44161248332) subsequently passed, retrieving sources from 19:41:40 to 19:42:55 UTC, running all five tests, and publishing the complete dataset in commit `c4934df`. Its run URL and completion timestamp are embedded in the published dataset. The local Streamlit server also returned HTTP 200 from its health endpoint.

Source checks began on 16 November 2026 and continued on 17 November. The 16 November local API audit completed at 23:35:20 UTC and retrieved 16 of 18 candidate BCCh series. Both country-export candidates returned API response code −50. A current public workbook resolved country-export access on 17 November. The [API JSON report](../research/results/bcch-source-check.json) includes counts, source status codes, metadata, and observation samples; the [trade report](../research/results/trade-source-check.json) records the successful workbook checks.

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

The first inspected legacy country workbook ended in February 2021. A newer official index points to the current `.xlsx` workbook, downloaded successfully without authentication on 17 November at 17:35:05 UTC. The `X_por_país` sheet contains 286 monthly observations from January 2003 through October 2026, in millions of US dollars FOB. In this copy, United States is row 11, China row 51, and Total row 75. [Current official index](https://si3.bcentral.cl/estadisticas/Principal1/enlaces/excel/SE/Excel_SE_Comercio.html), [Current workbook](https://si3.bcentral.cl/estadisticas/Principal1/excel/SE/COMEX/Excel/Mensual/02_Balanza_comercial_mensual_por_paises.xlsx)

Use the same sheet's Total row as the denominator for both destination shares. The largest absolute difference between its Total and the aggregate sheet's monthly exports was about 0.00000014 million USD, consistent with numerical rounding. The October 2026 API trade balance differed from the workbook's monthly balance by about 0.000000013 million USD. This establishes that the selected API series supplies the monthly FOB balance rather than an already accumulated balance.

The October 2026 workbook reports exports of 1,843.2384668 million USD to the US, 2,588.6959097 million USD to China, and 10,287.2957845 million USD in total. Shares computed from the twelve months ending October are 16.7932% for the US and 33.3701% for China. The public trade report retains values and comparison differences. These access and arithmetic checks resolve the country-data route; production refresh code and per-release evidence remain future implementation work.

## Sovereign risk

The daily, monthly, and quarterly API catalogs did not reveal a CDS or EMBI spread series under the searched names. A country-risk survey response appeared in discovery. That measures survey respondents' assessment of exchange-rate drivers and cannot supply the requested sovereign spread.

The user has no confirmed Bloomberg, LSEG, or J.P. Morgan access. Current official presentations cite commercial CDS or EMBI inputs, and the inspected World Bank Global Economic Monitor API indicator list did not expose a current spread feed. A World Bank reproducibility package explicitly requires authorized J.P. Morgan access for its EMBIG inputs. These findings leave public automated access unresolved. Keep the panel visibly pending in the design rather than substituting a different economic measure. [World Bank licensing example](https://reproducibility.worldbank.org/catalog/644/study-description), [Inspected GEM indicator catalog](https://api.worldbank.org/v2/sources/15/indicators?format=json&per_page=1000)

## Exchange rate inputs

Public IMF requests retrieved monthly histories from January 1976 onward. Chile CPI and CLP per USD extend through October 2026. US CPI extends through September 2026. The [initial IMF coverage report](../research/results/imf-source-check.json) records the 16 November checks.

The user selected a trailing 30-year benchmark on 17 November. A fresh check identifies October 1996–September 2026 as the current window. It contains 359 valid shared observations and one missing required-input month, October 2025. The arithmetic mean excludes that month, and the chart will retain the gap. The [benchmark check](../research/results/rer-benchmark-check.json) records the dates, valid count, and an independently checked identity relating actual and implied FX to the real index.

## Evidence scope

These results establish source access and candidate behavior for planning. Per-series comparisons with original releases and the completed dashboard's end-to-end refresh evidence remain implementation tasks. The initial encoding failure has been corrected and checked with both response encodings and a sanitized HTTP-error case.

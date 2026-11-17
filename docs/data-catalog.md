# Chile dashboard data catalog

Updated following user review, 17 November 2026.

The proposed series cover domestic activity, inflation, interest rates, public finances, exchange rates, and trade. The Central Bank of Chile is abbreviated BCCh and its statistical database is BDE. DIPRES is Chile's budget directorate.

The tables distinguish economic definitions from access checks. Authenticated source checks retrieved 16 of 18 candidate BCCh series. The two country-export codes returned API error −50. The [source audit](source-audit.md) records the results and latest valid periods. The dashboard's latest observation dates will come from downloaded observations.

## Indicator count

| Area | Headline indicators | Count |
| --- | --- | --- |
| Growth | Real GDP growth | 1 |
| Inflation | Headline and core inflation | 2 |
| Rates and sovereign risk | Policy rate, nominal yield curve, inflation compensation, sovereign risk | 4 |
| Public finances | Government balance and gross debt | 2 |
| Exchange rates | Nominal and bilateral real exchange rates | 2 |
| Commodities and trade | Copper, goods trade balance, export shares for China and the US | 4 |
| Total | Yield curve counted as one item | 15 |

Counting the three yield-curve maturities individually raises the total to 17. The implied nominal exchange-rate line and 10-year minus 2-year spread are derived views. Calculation inputs, such as nominal GDP in a fiscal denominator, also explain why API source-check counts differ from the dashboard inventory. The user has confirmed all 15 headline indicators for the personal-use dashboard.

## Activity and inflation

| Measure | Units and frequency | Source and identifier | Proposed transformation and chart |
| --- | --- | --- | --- |
| Real GDP growth | Percent, quarterly | BCCh, `F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T` | Compute `100 × (GDP[t] / GDP[t−4] − 1)` from the original chained-volume series. Show a line with a zero reference. |
| Headline inflation | Percent change over 12 months, monthly | BCCh analytic splice using INE inputs, `G073.IPC.V12.2023.M` | Display the published annual change. The current analytic splice provides historical consistency with the proposed core series. |
| Core inflation | Percent change over 12 months, monthly | BCCh CPI excluding volatile items, `G073.IPCSV.V12.2023.M` | Display the published annual change alongside headline inflation. Label the exclusion definition explicitly. |

GDP metadata identifies a chained-volume series with a 2018 reference and observations beginning in 1996. The proposed annual changes use the original quarterly series. Both inflation measures use BCCh's published analytic splice. Their vintage and rebasing notes belong in the chart's methodology. [GDP metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F032.PIB.FLU.R.CLP.EP18.Z.Z.0.T), [Inflation metadata](https://si3.bcentral.cl/Search/Buscar/Index/?or=pop&pageID=1&st=ipc+2023)

For the assignment's source comparison, check GDP against a BCCh national-accounts release, headline inflation against the corresponding INE release, and core inflation against the BCCh source table. Historical splices may require a comparison against the same vintage.

## Rates and sovereign risk

| Measure | Units and frequency | Source and identifier | Proposed display |
| --- | --- | --- | --- |
| Monetary policy rate | Percent per year, daily | BCCh, `F022.TPM.TIN.D001.NO.Z.D` | Step chart with the latest published rate and date. |
| Nominal peso yield curve | Percent per year, daily | BCCh secondary-market BCP/BTP benchmarks. `F022.BCLP.TIS.AN02.NO.Z.D`, `F022.BCLP.TIS.AN05.NO.Z.D`, `F022.BCLP.TIS.AN10.NO.Z.D` | A snapshot at 2, 5, and 10 years, using one common observation date. |
| Curve slope | Basis points, derived for the snapshot | Same nominal yields | `100 × (10-year yield − 2-year yield)` when yields are stored in percent. Show the spread beside the curve. |
| Five-year inflation compensation | Percent per year, daily | BCCh published bond measure, `F022.BOSP.TAS.AN05.Z.Z.D` | Historical line. Display the publisher's measure and explain its definition. |
| Sovereign risk | Basis points. Frequency depends on final source. | Proposed five-year CDS or a published sovereign bond spread. Automated source remains unresolved. | Historical line with the instrument, currency, tenor, benchmark, and source identified. |

Public rate tables identify the nominal benchmarks as BCP/BTP. The older search descriptions emphasize BCP. Their time coverage and current instrument composition need confirmation from API metadata and notes. The chart title should identify the published benchmark family. [BCCh nominal bond table](https://si3.bcentral.cl/Siete/ES/Siete/Cuadro/CAP_BDP/MN_TASA_INTERES_09/TMS_15/), [Policy-rate metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F022.TPM.TIN.D001.NO.Z.D)

Inflation compensation reflects expected inflation and premiums. BCCh publishes a dedicated five-year bond series, making it a promising source. Confirm the exact calculation and continuity before selecting it for the app. [Series metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F022.BOSP.TAS.AN05.Z.Z.D), [BCCh explanation](https://www.bcentral.cl/documents/33528/133214/and_01042022.pdf/cf0b235a-e26f-7944-d1aa-f421c2c409fa?t=1648820928677)

The interface will show observed yields by maturity, the common observation date, and the numerical 10-year minus 2-year spread. Economic interpretation is left to the viewer. The maturity axis preserves the distances between the observed tenors.

A sovereign bond spread must compare instruments with compatible currency and maturity. A CDS series needs its contract convention. Searches of public BDE metadata for CDS and EMBI have yet to establish a usable series. This panel remains in the proposed scope while access is investigated. [Ministry of Finance definition of country risk](https://old.hacienda.cl/preguntas-frecuentes/inversionistas/que-es-el-riesgo-pais.html)

## Public finances

Both requested measures will cover general government, including the consolidated central and municipal governments.

| Measure | Units and frequency | Preferred source | Proposed transformation |
| --- | --- | --- | --- |
| General government balance | Percent of GDP, quarterly trailing year | DIPRES amounts redistributed by BCCh, `F051.B04.FLU.G.C.CLP.T`, and nominal GDP `F032.PIB.FLU.N.CLP.EP18.Z.Z.0.T` | Sum four consecutive quarterly balance amounts and divide by matching trailing-year GDP after unit conversion. Verify against the DIPRES trailing-year ratio. Positive values indicate surplus. |
| Gross general government debt | Percent of GDP, quarterly | DIPRES amounts redistributed by BCCh, `F051.F2.STO.G.Z.CLP.T`, and the same nominal GDP input | Divide quarter-end debt by matching trailing-year GDP after unit conversion. Verify against the DIPRES ratio and record vintage differences. |

The general-government operations report includes quarterly, year-to-date, and trailing-year columns. The dashboard will use a trailing-year balance consistently. Annual history is also available. Authenticated downloads of the proposed balance and GDP inputs succeeded through 2026 Q2. Missing balance observations require complete-quarter checks before summing. [Quarterly operations](https://www.dipres.gob.cl/598/w3-propertyvalue-25270.html), [2026 Q2 report](https://www.dipres.gob.cl/598/articles-429191_version_PDF.pdf?ts=1790780517), [Annual operations](https://www.dipres.gob.cl/598/w3-propertyvalue-15495.html)

DIPRES publishes a separate quarterly general-government debt release. Its figures will provide the original-source comparison for the BCCh delivery route. General-government debt has a different institutional coverage from central-government debt. The general-government total downloaded successfully through 2026 Q2. [General-government debt releases](https://www.dipres.gob.cl/598/w3-propertyvalue-24801.html)

## Copper and trade

| Measure | Units and frequency | Source and identifier | Proposed transformation |
| --- | --- | --- | --- |
| Refined copper price | US dollars per pound, monthly | BCCh, `F019.PPB.PRE.40.M`, refined copper BML | Use the published monthly price. Retain the original price provider in the metadata. |
| Goods trade balance | Millions of US dollars, monthly | BCCh, `F068.B1.VAR.T0.0.S.N.Z.Z.Z.Z.6.0.M` identifies a monthly trade-balance series | Confirm its precise transformation and FOB basis before use. Proposed display has monthly bars and a trailing 12-month sum. |
| China's share of goods exports | Percent, monthly trailing year | BCCh exports to China, `F068.B1.FLU.Z.0.C.N.Z.Z.CN.Z.6.0.M` | Divide trailing 12-month exports to China by trailing 12-month total exports and multiply by 100. |
| US share of goods exports | Percent, monthly trailing year | BCCh exports to US, `F068.B1.FLU.Z.0.C.N.Z.Z.US.Z.6.0.M` | Apply the same formula using exports to the US. |
| Total goods exports input | Millions of US dollars FOB, monthly | BCCh, `F068.B1.FLU.Z.0.C.N.Z.Z.Z.Z.6.0.M` | Use as the common denominator after checking compatibility with the destination series. |

Country-series identifiers were read from the public BCCh export table, but both returned API error −50 and are absent from the authenticated monthly catalog. The legacy downloadable country workbook ends in February 2021. A current destination source remains to be selected. The total-export input downloaded through October 2026. The trailing-year calculation will require twelve consecutive months for each destination and a compatible denominator. [Country export table](https://si3.bcentral.cl/siete/ES/Siete/Canasta?idCanasta=XCD1N2215), [Total exports metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F068.B1.FLU.Z.0.C.N.Z.Z.Z.Z.6.0.M)

The monthly balance identifier's name alone does not settle whether it already incorporates a transformation. Resolve this before calculating a trailing sum. Verify FOB import and export valuation against the published monthly trade tables. [Balance metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F068.B1.VAR.T0.0.S.N.Z.Z.Z.Z.6.0.M), [Official trade workbooks](https://si3.bcentral.cl/estadisticas/Principal1/Excel/SE/COMEX/excel.html), [Copper metadata](https://si3.bcentral.cl/Search/Buscar/Index/?st=F019.PPB.PRE.40.M)

## Nominal and real exchange rates

The main comparison will use monthly actual and historical-benchmark-implied Chilean pesos per US dollar. The bilateral real index will appear alongside it. A daily observed-dollar quote can provide a separate latest-market reference.

| Input | Units and frequency | Source and key | Access check |
| --- | --- | --- | --- |
| Monthly actual exchange rate | CLP per USD, monthly period average | IMF ER, `CHL.XDC_USD.PA_RT.M` | Downloaded history from January 1976 through October 2026. |
| Chile consumer prices | CPI index, monthly | IMF CPI, `CHL.CPI._T.IX.M` | Downloaded history from January 1976 through October 2026. |
| US consumer prices | CPI index, monthly | IMF CPI, `USA.CPI._T.IX.M` | Downloaded history from January 1976 through September 2026, with gaps elsewhere in the history. |
| Daily observed dollar | CLP per USD, daily | BCCh, `F073.TCO.PRE.Z.D` | Authenticated download through 16 November 2026. |

These IMF keys and the calculation come from the user's Salamanca project. Source tests retrieved the histories from January 1976 onward. The latest shared month in the 17 November check is September 2026. The trailing 30-year window is October 1996–September 2026 and contains 359 valid shared months. October 2025 lacks a required input. Preserve that gap and exclude it from the benchmark mean. [Benchmark check](../research/results/rer-benchmark-check.json), [IMF API information](https://data.imf.org/en/Resource-Pages/IMF-API), [Salamanca methodology](https://github.com/greg-at-k/salamanca)

Let `E[t]` be CLP per USD, `P_US[t]` the US CPI, and `P_CL[t]` Chile's CPI. Calculate the bilateral real rate as `q[t] = E[t] × P_US[t] / P_CL[t]`. Larger values indicate real peso depreciation.

For a reference period B, calculate `q_bar` as the arithmetic mean of valid monthly `q` values in B. Then calculate the real index as `100 × q[t] / q_bar` and the implied nominal exchange rate as `E_implied[t] = q_bar × P_CL[t] / P_US[t]`.

The agreed default reference period is the trailing 360 calendar months ending at the latest month shared by the three inputs. Average valid monthly real rates within that window and retain gaps in the charts. The window advances with new shared monthly data. Zooming changes the visible dates independently. The chart's short caption defines the implied line as the nominal rate consistent with the reference period's average bilateral real exchange rate.

Both actual and implied lines share one CLP-per-USD axis. The tooltip will show the month, both rates, the reference period, and the real index. When the actual rate exceeds the implied rate, the peso is weaker in real terms relative to that historical benchmark. The benchmark alone establishes a historical comparison.

## Sample and metadata rules

The agreed default viewing window is 2010 onward. Full history and shorter 5- and 10-year views will be available where coverage permits. The real exchange-rate benchmark uses its separate trailing 30-year history. Fiscal quarterly history may begin later. The catalog records each series' actual coverage after download.

Every chart will display units, native frequency, source, latest observation date, and transformation. A monthly point will be labeled by month and a quarterly point by quarter. Provider release or update dates and retrieval timestamps will be stored separately.

Develop the full personal-use dashboard first. The assignment's 4–8-indicator deliverable will be considered afterward, using a selected view or a separate tool and repository as appropriate. Its final format is deferred to that later task.

## Remaining source checks

1. Resolve the rejected country-export candidates using a current primary source.
2. Verify source notes and one observation for each selected series against its original release. Download coverage is recorded in the source audit.
3. Resolve the trade-balance transformation and the export denominator's compatibility.
4. Verify fiscal units, denominator vintages, and calculated ratios against DIPRES releases.
5. Establish a reliable automated sovereign-risk source and its publication permissions.
6. Preserve IMF source flags and gaps, including the missing month identified in the trailing 30-year benchmark check.

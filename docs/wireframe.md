# Chile dashboard wireframe

Draft for review, 16 November 2026.

The proposed Streamlit layout gives readers a quick view of Chile's economy, then space to inspect rates, public finances, and the external sector. Chart metadata and economic definitions stay close to the relevant plots.

## Desktop layout

```text
VITALS CHILE
Chile economic dashboard
Last successful data refresh [timestamp and timezone]

[Real GDP growth]  [Headline inflation]  [Policy rate]  [Observed USD]
 value + quarter   value + month        value + date  CLP per USD + date

Economy | Rates and risk | Public finances | External sector | Sources

VIEWING WINDOW   [5 years] [10 years] [Since 2010] [Full] [Custom]

Selected section charts

Every chart has units, frequency, source, latest observation, and method.
```

The four overview cards each carry their own observation period. The refresh timestamp describes the dataset retrieval. It remains visible above the navigation.

## Economy

```text
REAL GDP GROWTH                  HEADLINE AND CORE INFLATION
Quarterly annual change          Monthly annual change
Line chart with zero reference   Two lines with direct labels

                                POLICY RATE
                                Daily step chart
```

GDP will retain its quarterly frequency. Inflation will retain its monthly frequency. Hover labels will use those periods directly. The policy-rate chart can also appear in the rates section, using the same data and formatting.

## Rates and risk

```text
NOMINAL PESO YIELD CURVE          SOVEREIGN RISK
Observation date                 Instrument and benchmark
Yield versus years to maturity   Historical spread chart
2y ------- 5y ------- 10y
10y minus 2y spread [basis points]

FIVE YEAR INFLATION COMPENSATION
Historical line
Definition and source notes
```

The yield curve uses the latest date shared by its required maturities. All plotted rates come from that date. The date selector initially opens at that snapshot and may offer an earlier common date. The first design emphasizes the snapshot, matching the user's preference.

The maturity axis is numerical, preserving the unequal distance from 2 to 5 years and 5 to 10 years. Visible points identify observed maturities. A simple connecting line joins them.

Shape labels will distinguish upward, downward, flat, and mixed patterns once a flatness threshold is agreed. A short caption connects flattening and inversion with closer attention to the growth outlook. Units and the exact spread allow interpretation alongside that label.

The sovereign-risk chart awaits a confirmed source. Its eventual heading must name the chosen measure, such as a five-year sovereign CDS spread or a particular bond spread.

## Public finances

```text
GENERAL GOVERNMENT BALANCE       GROSS GENERAL GOVERNMENT DEBT
Trailing year, percent of GDP    Quarter end, percent of GDP
Bars around zero                Line chart

Government coverage and GDP denominator definitions
```

The balance and debt charts have separate axes and explicit definitions. The balance shows a flow over the trailing year. Debt shows a stock at quarter end. Both use general-government coverage.

## External sector

```text
ACTUAL AND IMPLIED EXCHANGE RATE                         full width
CLP per USD
Actual monthly average  ———————————
Historical benchmark implied  - - - - -
Reference period [Jan 2015–Dec 2019, proposed]

About the implied rate [expandable explanation and arithmetic]

BILATERAL REAL EXCHANGE RATE      COPPER
Reference period average = 100   US dollars per pound
Line and 100 reference           Monthly line

GOODS TRADE BALANCE              EXPORT DESTINATION SHARES
Monthly bars                    China and United States
Trailing year view control      Trailing year percentages
```

The actual-versus-implied chart anchors the real exchange-rate discussion in the familiar price of a US dollar. A short explanation will state that a higher actual line means the peso is weaker in real terms relative to the selected historical benchmark.

The benchmark period is independent of the viewing window. A reader must explicitly change the benchmark to recalculate the implied line. Both the chart and downloads identify the active benchmark.

Actual exchange rates can extend beyond the latest common CPI month. The implied and real-index lines end where their required inputs end. The display will identify both coverage dates.

Trade balance will offer monthly and trailing-year views on one chart. Export shares will put China and the US on the same percentage axis, calculated over identical twelve-month windows.

## Sources and refresh

```text
DATA STATUS
Series | Latest observation | Last successful retrieval | Status

[Download data] [Download methodology] [View refresh log]

SOURCE AND METHOD DETAILS
Exact series identifiers, definitions, transformations, and coverage

VERIFICATION
Series | Checked period | Source value | Dashboard value | Evidence
```

Readers can inspect evidence without leaving the app's main navigation. A failed source retrieval will retain the last verified data and its original successful retrieval time, with the failed attempt reported separately.

## Visual direction

Proposed typography is Source Sans 3, subject to Streamlit configuration support. Use an off-white background, dark navy text, restrained copper accents, and teal for comparison lines. Distinguish series with labels and line patterns as well as color.

Charts should have generous width, limited grid lines, readable axes, and consistent numeric formatting. GDP and inflation use one decimal place by default, yields use two, and CLP per USD uses an appropriate rounded display with precise downloaded values.

On narrow screens, overview cards wrap into two columns and chart columns stack vertically. The actual-versus-implied exchange-rate chart remains a single full-width panel. Native navigation should remain easy to reach.

## Review choices

- Confirm the overview card selection and section order.
- Review the proposed 2010 default start and 2015–2019 exchange-rate benchmark after checking coverage.
- Choose how much exchange-rate explanation should be visible before expanding details.
- Review the yield-curve shape labels and a possible flatness threshold.
- Resolve the expanded scope against the assignment's indicator range.

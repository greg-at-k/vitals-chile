# Vitals Chile

Planning for a public Chile economic dashboard deployed with Streamlit.

The dashboard will help readers assess Chile's growth, inflation, financing conditions, fiscal position, and exposure to external shocks. The current work covers source feasibility, economic definitions, layout, and refresh design.

## Planning documents

- [Data catalog](docs/data-catalog.md) identifies proposed series, sources, units, transformations, and remaining source checks.
- [Dashboard wireframe](docs/wireframe.md) describes the proposed Streamlit layout and chart interactions.
- [Refresh and verification plan](docs/refresh-plan.md) describes GitHub Actions downloads, published data, local testing, and submission evidence.

## Project setup

Public repository — [greg-at-k/vitals-chile](https://github.com/greg-at-k/vitals-chile).

Intended deployment — Streamlit Community Cloud.

The repository secret `BCCH_API_TOKEN` has been confirmed by name. GitHub Actions will use it for authenticated Central Bank downloads. Public datasets will supply both local and hosted Streamlit sessions.

Local environment files and Streamlit secrets are covered by `.gitignore`. Git ignore rules control tracking. Files in the working directory remain accessible to local tools.

## Current decisions

The proposed scope includes GDP, headline and core inflation, the policy rate, a nominal yield-curve snapshot, government balance and gross debt, copper, nominal and bilateral real exchange rates, actual versus historical-benchmark-implied CLP per USD, goods trade balance, export shares for China and the US, sovereign risk, and inflation compensation.

The assignment specifies 4–8 indicators. This expanded scope needs an explicit submission decision. Chart grouping and derived views will be documented transparently.

Source metadata has been reviewed. Chile and US IMF CPI and Chile monthly FX sample requests succeeded on 16 November 2026. Authenticated Central Bank downloads, fiscal workbook parsing, and sovereign-risk access remain to be checked.

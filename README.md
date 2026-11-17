# Vitals Chile

Planning for a public Chile economic dashboard for personal monitoring, deployed with Streamlit.

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

The 17 November review confirms the overview cards, section order, and a chart window starting in 2010. The real exchange-rate benchmark uses the trailing 30 years, with a short visible explanation. The yield curve displays observed values and the numerical spread for viewer interpretation.

The agreed personal-use scope includes all 15 headline indicators, or 17 when the curve's three maturities are counted separately, plus the implied FX line and curve spread as derived views. Build and refine this full dashboard first. A later assignment deliverable will address the 4–8-indicator requirement through a selected view or a separate tool and repository. Its format will be decided at that stage.

Authenticated BCCh checks retrieved 16 of 18 candidate series on 16 November 2026. The two rejected country-export codes need an alternative current source. Chile and US IMF CPI and Chile monthly FX sample requests also succeeded. Sovereign-risk access remains unresolved. See the [source audit](docs/source-audit.md).

## Run the source checks locally

The local research environment loads `BCCH_API_TOKEN` from `.env` when it is absent from the process environment. Install the research dependencies, then run the source check.

```powershell
.\.venv\Scripts\python.exe -m pip install -r research/requirements.txt
.\.venv\Scripts\python.exe research/check_bcch_sources.py
```

The current audit reports `needs_attention` while the two country-export candidates fail. Its JSON output includes coverage, observation samples, and public status information. The manually triggered [GitHub source audit](https://github.com/greg-at-k/vitals-chile/actions/workflows/source-audit.yml) uses the repository secret.

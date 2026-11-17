# Chile dashboard refresh and verification plan

Updated following user review, 17 November 2026.

Implementation note: the first working version uses a single atomic `data/dashboard.json` file on `main`, rather than a separate data branch. The weekly Friday 23:17 UTC workflow refreshes all inputs and also accepts manual runs. The app reads this complete file with a five-minute cache and a bundled fallback. Its reload button reads published data; upstream refresh is triggered in GitHub. See [running instructions](running.md). The more detailed split-frequency schedule below remains a proposal, not the implemented schedule.

The full personal-use dashboard is the current deliverable. GitHub Actions will retrieve and validate source data. A versioned public dataset will supply Streamlit both locally and on Community Cloud. The repository's `BCCH_API_TOKEN` secret will be available to the downloader during its GitHub job. An assignment-specific view or separate tool will be considered after the personal dashboard is developed.

## Data flow

```text
BCCh API + IMF API + DIPRES releases
                    |
                    v
GitHub Actions download and validation
                    |
                    v
Versioned public dataset + source metadata + refresh log
                    |
             +------+------+
             |             |
             v             v
      Local Streamlit   Hosted Streamlit
```

The proposed first implementation stores compact normalized data and a manifest in a dedicated data branch of `greg-at-k/vitals-chile`. The app will retrieve a manifest and read files from the immutable commit it names. This keeps one app session's dataset internally consistent across a refresh. The exact file format will be chosen after the source checks.

## Private API token

The user has created the repository secret `BCCH_API_TOKEN`. Its existence was confirmed through a metadata-only listing. The user subsequently added the token to the gitignored local `.env` for local source testing. Source-check processes load it without including its value in public output.

The job will pass the secret to the download process as an environment variable. BDE's documented REST authentication includes a token parameter in the request. Request errors and diagnostic output must omit authenticated URLs. Public logs and artifacts will contain whitelisted source identifiers, dates, values, and status summaries. [BDE API documentation](https://si3.bcentral.cl/estadisticas/Principal1/Web_Services/documentacion_en.html)

GitHub hides saved secret values in its settings and API. Job code can access those values at execution time, so workflow-edit access is a path to using or exposing them. An environment secret can add approval controls before a job receives it. The user selected a repository secret after discussing this access model. [GitHub secret documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

A local `.env` is optional for running the authenticated downloader locally. A file in this workspace would be readable by local tools even when gitignored. Local Streamlit tests will use published public data under the proposed design.

## Source feasibility checks

A manually triggered GitHub Actions source audit and a local source-check command now test authentication, inspect available series metadata, and retrieve observations for the catalog's candidates. The [audit results](source-audit.md) identify successful downloads and rejected country-export candidates.

The source audit differs from the eventual scheduled dashboard refresh in its completion criteria. A source-audit result establishes access and candidate-series behavior. The completed dashboard needs an end-to-end refresh that publishes a validated dataset and updates its charts.

## Proposed schedule

For personal monitoring, the proposed frequency follows the source data's frequency, with manual refresh available on demand.

| Data | Proposed automatic check |
| --- | --- |
| Policy rate, nominal bond yields, inflation compensation, daily FX | Once each weekday at 23:17 UTC |
| GDP, monthly inflation, copper, trade, fiscal inputs, monthly IMF CPI and FX | Once weekly on Friday at 23:17 UTC |

This is a recommendation for review. A single weekly refresh for all series, plus manual refresh, is also compatible with a regular schedule. A weekday market check keeps the snapshot and daily FX more current. Per-series observation and retrieval dates identify the age of every input.

## Request volume and pacing

BCCh states a limit of five series per second per account and no daily request cap. The source audit now runs sequentially and pauses one second before each API request. This is comfortably below the published limit. [BCCh API limits](https://si3.bcentral.cl/estadisticas/Principal1/Web_Services/ayuda_soporte.html)

Routine refreshes retrieve configured series. Catalog discovery supports initial setup and source repairs. Normal app visits read the saved dataset and cache, so visitor count does not multiply source requests. Concurrent manual refresh requests will share one job queue. Transient failures will have bounded retries, and HTTP 429 responses will honor the provider's retry instructions.

An IMF numerical quota has yet to be verified from primary documentation. The proposed IMF workload is a few paced requests per week. Any additional provider's limits will be checked when its source is selected.

Scheduled GitHub Actions can be delayed, so the app will report actual successful retrieval times. The workflow should use one concurrency group to serialize publication. [GitHub schedule behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

The external job also allows data retrieval while a Community Cloud app is hibernating. When a reader opens the app, it will read the latest published manifest. [Streamlit app management](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)

## Validation and publication

Each source adapter will verify the series identifier, expected frequency, date parsing, numeric values, and source status flags. Duplicate observations will require explicit resolution. Missing observations will retain gaps. Published data will preserve the provider's available historical revisions.

The job will stage due downloads and calculations before publication. Inputs due on a slower schedule retain their previous verified values and successful retrieval times. All panels using shared inputs, including actual and implied exchange rates, will derive from the same staged inputs. A failed required download will preserve the previously published complete dataset. The attempt log will identify the failure, while the app continues to show the last successful dataset and its retrieval times.

The manifest will include a dataset version, publication time, last successful refresh, and per-series identifiers, units, frequency, coverage, retrieval time, source update date where available, source flags, and transformation details. Public source URLs will be sanitized.

For the yield curve, choose the latest date with observations for all selected maturities. For the implied exchange rate and real index, align monthly CPI and FX inputs and calculate the benchmark from valid observations within the trailing 360 calendar months ending at the latest shared month. Preserve missing-input months. For destination shares, require complete shared twelve-month windows and a positive export denominator.

An unchanged dataset after a successful source request is a successful refresh. Record both the check time and whether observations or values changed. A failed retrieval retains its previous successful retrieval timestamp.

## Local and hosted testing

The public Streamlit deployment remains the selected target. Streamlit runs a Python backend, which can call data sources when a reader requests a refresh. The data branch in GitHub supplies durable saved datasets, while Streamlit's cache holds a working copy. [Streamlit architecture](https://docs.streamlit.io/develop/concepts/architecture/architecture), [Caching](https://docs.streamlit.io/develop/concepts/architecture/caching)

The manual controls must state what they do. Reloading the latest published dataset can be handled inside the app. Requesting a new upstream download can use the GitHub workflow's manual trigger. An in-app button that starts that workflow would require a suitably scoped GitHub credential in Streamlit's private secrets. This button's implementation remains part of design review.

The planned app can run locally with Streamlit after the first public dataset is published. Local tests will exercise chart rendering, date filters, downloads, benchmark changes, missing-data displays, and source details using those public data.

Authenticated download tests can run manually in GitHub Actions using the repository secret. Source adapters that use public IMF and DIPRES data can also run locally. The user can choose local token configuration later if local authenticated-download debugging becomes necessary.

Deploy the finished app from the public repository to Streamlit Community Cloud. Pin the supported Python and package versions after checking dependency compatibility. The hosted app will use the same dataset-reading path as local tests. [Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)

## Assignment evidence

For each underlying series, select one published observation and record the series identifier, reference period, original source URL, source value, imported value, units, rounding tolerance, check date, and result. A derived chart also needs an independent recomputation from its underlying observations.

| Display | Independent check |
| --- | --- |
| GDP growth | Recalculate one annual change from quarterly real GDP observations. |
| Headline and core inflation | Compare each selected monthly annual change with its corresponding official source. |
| Policy rate | Match a dated rate with a BCCh announcement or published source table. |
| Yield curve | Match every plotted maturity on the shared snapshot date and recalculate the spread. |
| Government balance and debt | Match each ratio, coverage definition, and GDP denominator with the DIPRES release. |
| Copper | Match the price, quotation unit, and monthly averaging convention with its published source. |
| Actual and implied exchange rates | Match monthly FX and both CPI inputs, then independently calculate the benchmark, implied rate, and real index. |
| Trade balance | Match the published goods balance and recompute a trailing sum after validating the source transformation. |
| China and US shares | Match both destination values and total exports, then independently recalculate both shares. |
| Sovereign risk | Match the selected instrument, reference date, units, and published spread. |
| Inflation compensation | Match the published compensation and its underlying source convention. |

Retain a successful end-to-end refresh log with start and completion times, series results, publication version, and the GitHub run link. Capture the app showing that refresh timestamp and chart observation dates. Keep the source-audit evidence identified separately from the final refresh evidence.

## Implementation sequence

1. Finish the source audit and update the data catalog with authenticated coverage and resolved definitions.
2. Finish the visual design using the reviewed layout, trailing 30-year benchmark, and agreed full personal-use scope.
3. Implement source adapters and one validated public dataset publication.
4. Build the agreed Streamlit charts and controls against the published data.
5. Complete per-series verification and exercise an end-to-end refresh.
6. Deploy the personal-use dashboard to Streamlit Community Cloud and retain verification evidence.
7. In a later task, decide whether the assignment needs a selected 4–8-indicator view or a separate tool and repository.

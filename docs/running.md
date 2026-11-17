# Running and deploying Vitals Chile

Install Python dependencies and launch the app from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

The app reads the published `data/dashboard.json` from GitHub, with a five-minute cache and a bundled-file fallback. **Reload published data** clears that cache. It does not download new upstream observations. To use only the local saved dataset, set `VITALS_LOCAL_DATA=1`.

Run `python refresh.py` to download new observations using `BCCH_API_TOKEN` from the environment or gitignored `.env`. Publication replaces the dataset only after every required source and calculation succeeds. API requests are sequential and paced. Null inputs retain chart gaps; the curve uses a shared date. A failed refresh leaves the previous file intact and returns a nonzero exit status.

GitHub's **Refresh dashboard data** workflow runs Fridays at 23:17 UTC and supports **Run workflow**. It uses the repository secret and commits the complete dataset to `main`. This first implementation uses one atomic JSON file on the code branch, simplifying the proposed separate-data-branch design. The file includes raw observations, calculations, and a successful-refresh record. GitHub Actions retains failed-attempt logs separately. App visitors never need the source token. Scheduled workflows on inactive public repositories may be disabled by GitHub.

Run checks with `python -m unittest discover -s tests`. Calculation tests cover actual/implied FX consistency, shared curve dates, export-share arithmetic, and missing fiscal quarters. Streamlit AppTest exercises all sections, viewing windows, and reload. These checks do not verify browser appearance or replace original-release comparisons.

For Streamlit Community Cloud, sign in with GitHub, choose `greg-at-k/vitals-chile`, branch `main`, and entrypoint `streamlit_app.py`. Select a Python version compatible with the pinned dependencies (local testing uses Python 3.14). No app secrets are required. The source secret stays in GitHub Actions. Public deployment requires access to the user's Streamlit account and has not been completed by preparing these files.

Sovereign risk remains unavailable. Fiscal ratios are shown as calculated figures with original DIPRES release comparisons pending. The source catalog and source audit distinguish completed access checks from pending verification; this version does not yet satisfy the assignment's per-series original-source evidence requirement.

# South Asia Data Observatory (Streamlit)

Interactive analytics dashboards for Bangladesh and India with maps, KPIs, and regional comparisons.

## Run Locally
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```

## Deploy (Streamlit Community Cloud)
1. Push this repository to GitHub.
2. Go to Streamlit Community Cloud and create a new app.
3. Set the entry point to `app.py`.
4. Ensure `requirements.txt` is present in the repo root.

## Notes
- Data files are loaded from local CSVs in the project root.
- Pages live under `pages/`.

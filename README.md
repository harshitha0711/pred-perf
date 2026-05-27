# Student Performance Predictor
A simple Streamlit app for predicting student exam scores.
## Setup (Windows PowerShell)
1. Open PowerShell in the project root:
   ```powershell
   cd C:\Users\Dell\harshi\pred-perf
   ```
2. Activate the existing virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Install Python dependencies if they are not already installed:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with your MongoDB URI if you want database persistence:
   ```text
   MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/
   ```
   If you do not have MongoDB available, the app will still run using an in-memory fallback.
5. Start the Streamlit app:
   ```powershell
   streamlit run app.py
   ```
6. Open the app in your browser at:
   ```text
   http://localhost:8502
   ```
## Notes
- Do not commit `.env` or `node_modules/` to Git.
- This repo already ignores `venv/`, `node_modules/`, and `.env`.
- If Streamlit gives an error about missing packages, make sure you installed `requirements.txt` inside the activated `venv`.
- Run `streamlit run app.py` from the activated `venv` in the project root. If the app cannot connect to MongoDB, it will still run with an in-memory fallback.


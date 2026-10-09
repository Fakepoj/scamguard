# SCAMGUARD v0.4 FRONTEND

React + Vite frontend for the ScamGuard hybrid scam detection API.

## Features
- Message analyzer
- FastAPI integration
- Risk score visualization
- Threat signal cards
- URL intelligence
- ML/rule metrics
- Security recommendations
- Recent analysis history
- Responsive layout
- Sample messages

## Run
Start the backend first:

```powershell
cd C:\Users\l2e\Documents\scamguard-v0.3
uvicorn app.main:app --reload
```

Then in this frontend folder:

```powershell
npm install
npm run dev
```

Open `http://localhost:5173`.

## Build
```powershell
npm run build
```

The frontend expects the backend at `http://127.0.0.1:8000`.

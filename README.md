\# ScamGuard



\*\*ScamGuard\*\* is a scam detection application designed to help users identify potentially fraudulent messages and suspicious URLs using a combination of rule-based analysis, URL inspection, local intelligence, and machine learning.



\## Features



\* Suspicious message analysis

\* URL and link risk assessment

\* Rule-based scam detection

\* Machine-learning-assisted classification

\* Local intelligence checks

\* OCR support for image-based content

\* Feedback handling for future improvements

\* Automated backend tests

\* Web-based frontend interface



\## Project Structure



```text

scamguard/

├── backend/

│   ├── app/

│   ├── data/

│   ├── models/

│   ├── tests/

│   ├── requirements.txt

│   └── train.py

├── frontend/

│   ├── src/

│   ├── index.html

│   └── package.json

├── .gitignore

└── README.md

```



\## Technology Stack



\* \*\*Backend:\*\* Python, FastAPI

\* \*\*Frontend:\*\* React, Vite

\* \*\*Machine Learning:\*\* Model-based text classification

\* \*\*Testing:\*\* pytest



\## Getting Started



\### Backend



Open a terminal in the `backend` directory, create and activate a Python virtual environment, and install the dependencies.



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

```



Start the API using the command appropriate for the application entry point:



```powershell

uvicorn app.main:app --reload

```



\### Frontend



Open another terminal:



```powershell

cd frontend

npm install

npm run dev

```



Use the local URL displayed by Vite to access the frontend.



\## Testing



From the `backend` directory, run:



```powershell

python -m pytest

```



\## Security and Limitations



ScamGuard provides risk assessments, not guarantees. A message classified as safe may still be fraudulent, and suspicious content may be legitimate. Users should independently verify requests for money, credentials, and sensitive information.



\## Development Status



This project is under active development. Features and detection performance may change as the system evolves.



\## Author



\*\*Kenneth Fatore\*\*



GitHub: \[@fakepoj](https://github.com/fakepoj)


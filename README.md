# Advanced Healthcare System

A ready-to-run Flask healthcare management demo for a final-year IT project.

## Modules
- Dashboard
- Patient Management
- Doctor Management
- Appointment Scheduling
- Digital Prescriptions
- Health-check endpoint

## Run locally
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## Render deployment
1. Upload this project to a GitHub repository.
2. In Render, create a new Web Service and select the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy.

`render.yaml` is included for Blueprint deployment.

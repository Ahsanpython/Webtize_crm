# PyCRM Starter (Django + DRF + Chart.js)

A Python-based CRM for managing **Clients, Projects, Timesheets, and Invoices**, with a **dashboard** featuring charts.

## Features
- Add clients and projects (HR-friendly forms).
- Track project budget, estimated hours, time spent, and progress.
- Timesheet entries per project (billable/non-billable).
- Invoices with items and status (draft/sent/paid/overdue).
- Dashboard with charts: revenue by month, invoice status, project status, burn-down/time-left.
- REST API endpoints for charts and data.
- Clean Bootstrap UI (not Django admin look).

## Quick Start
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# env
cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata demo  # optional demo data
python manage.py runserver
```

Open: http://127.0.0.1:8000/  (Dashboard)
API docs (schema): http://127.0.0.1:8000/api/

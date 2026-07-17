# AGENTS.md

## Project
Python (Flask) web-based scientific calculator. Flask backend evaluates expressions; HTML/CSS/JS frontend provides the UI.

## Quick Start
```bash
pip install -r requirements.txt
python app.py          # starts on http://localhost:5000
```

## Tests
```bash
python -m pytest tests/
```
Run tests before and after changes.

## Architecture
- `app.py` — Flask server, safe expression evaluator (ast-based, no eval)
- `templates/index.html` — calculator page
- `static/style.css` — grid layout, scientific button styling
- `static/script.js` — button handlers, display logic, fetch to backend API

## Key Conventions
- Expression evaluation must use ast parsing — never use `eval()` or `exec()`
- All arithmetic logic lives in `app.py`; frontend only builds expression strings
- Frontend sends POST to `/calculate` with `{"expression": "..."}`
- Expressions use Python math function names: `sin`, `cos`, `sqrt`, `log`, `factorial`, etc.

## Gotchas
- `pip install` before running; Flask is the only dependency
- Division by zero and invalid expressions return error JSON, not 500s
- Trig functions expect radians by default

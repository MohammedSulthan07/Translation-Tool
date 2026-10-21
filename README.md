# TASK 1 — LinguaFlow Language Translation Tool

A polished Flask web application for translating text with a clean, responsive UI.

## What this project implements
- Source-language and target-language selectors.
- Microsoft Azure Translator integration.
- Keyless MyMemory fallback for quick local demos when Azure credentials are not present.
- Clear translated output panel.
- Copy-to-clipboard button.
- Browser text-to-speech button.
- Responsive mobile layout and character counter.

## Project structure
```text
app.py
requirements.txt
.env.example
README.md
templates/index.html
static/style.css
static/app.js
```

## Run locally
1. Install Python 3.10+.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   # Windows: .venv\\Scripts\\activate
   # Linux/macOS: source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Optional: configure Microsoft Azure Translator:
   ```bash
   # Windows PowerShell
   $env:AZURE_TRANSLATOR_KEY="your-key"
   $env:AZURE_TRANSLATOR_REGION="your-region"

   # Linux/macOS
   export AZURE_TRANSLATOR_KEY="your-key"
   export AZURE_TRANSLATOR_REGION="your-region"
   ```
5. Start:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000`.

## Notes
The Azure path is the production-style integration requested by the assignment. When the two Azure variables are missing, the application automatically uses MyMemory so that the UI can still be demonstrated without provisioning a paid/cloud credential. For a deployed application, configure Azure Translator and follow its quota/rate-limit guidance.

## Technologies
Python, Flask, REST API, HTML5, CSS3, JavaScript, Microsoft Azure Translator, MyMemory, Web Speech API.

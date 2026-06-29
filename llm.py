# Campaign Brief Generator — Setup Guide

## What you're getting

A Streamlit dashboard that:
1. Takes a MOM file (PDF, DOCX, or TXT)
2. Sends it to GPT-5 with rules locked in (MOM is the only source of truth, no fabrication, gaps marked clearly)
3. Shows you an editable brief on screen
4. Lets you download the result as Excel, CSV, Word, or PDF

Right now it runs in **demo mode** — no API key needed, Generate just returns a pre-built sample response so you can test the whole flow.

## Project structure

```
campaign_brief_app/
├── app.py                  <- the Streamlit dashboard itself
├── schema.py                <- the field list (edit this to add/remove brief fields)
├── prompts.py                <- the instructions sent to GPT-5
├── llm.py                    <- calls GPT-5 (or returns demo data if no key set)
├── parser.py                  <- extracts text from uploaded PDF/DOCX/TXT
├── requirements.txt
├── exporters/
│   ├── excel_export.py
│   ├── csv_export.py
│   ├── docx_export.py
│   └── pdf_export.py
└── test_outputs/
    └── yummiez_simulated_response.json   <- the demo-mode sample data
```

## Step 1 — Put this on GitHub

1. Create a new repository (can be private).
2. Upload everything in `campaign_brief_app/` to it, keeping the folder structure exactly as is.

## Step 2 — Deploy on Streamlit Cloud

1. Go to share.streamlit.io and sign in.
2. Click "New app", point it at your repo, and set the main file to `app.py`.
3. Click Deploy. You'll get a link like `yourname-campaignbrief.streamlit.app`.

At this point the app is live and running in demo mode — anyone with the link can upload a file, click Generate, and see the sample brief, edit it, and download it in all 4 formats. This is the right moment to test the dashboard itself before spending on a real API key.

## Step 3 — Go live with real GPT-5 calls (when ready)

1. Get an OpenAI API key from platform.openai.com.
2. In your Streamlit Cloud app settings, find "Secrets" and add:
   ```
   OPENAI_API_KEY = "sk-..."
   ```
3. Save. The app will restart automatically and demo mode will switch off — the banner at the top will disappear, and Generate will now call GPT-5 for real.

## Editing the brief fields later

If you ever need to add, remove, or rename a field in the brief, do it in **one place**: `schema.py`, in the `BRIEF_FIELDS` list. Every other file — the prompt, the dashboard tabs, all 4 exporters — reads from that list automatically. You never need to touch them individually.

## A note on cost

Every click of "Generate Brief" is one GPT-5 API call. Costs scale with how long your MOMs are and how often you generate. Worth keeping an eye on usage in your OpenAI dashboard once this is live with a real key.

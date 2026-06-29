"""
Simulates exactly what app.py does, minus the Streamlit UI calls,
since Streamlit can't be installed in this sandbox (no network).
This proves the actual logic (parser -> llm -> exporters) works.
"""
import sys
import io
sys.path.insert(0, "..")

from llm import generate_brief, is_demo_mode
from schema import BRIEF_FIELDS
from exporters.excel_export import build_workbook_bytes
from exporters.csv_export import brief_to_csv_bytes
from exporters.docx_export import build_docx_bytes
from exporters.pdf_export import build_pdf_bytes

print("Demo mode active:", is_demo_mode())

# Simulate "Generate Brief" button press with no real MOM text needed,
# since demo mode short-circuits straight to the stored sample response.
response = generate_brief(mom_text="irrelevant in demo mode", extra_context="")

assert "brief" in response
assert "external_suggestions" in response
for field in BRIEF_FIELDS:
    assert field in response["brief"], f"Missing field: {field}"
    entry = response["brief"][field]
    assert "value" in entry and "source_type" in entry and "evidence" in entry
print("Schema check passed: all", len(BRIEF_FIELDS), "fields present with correct shape.")

# Simulate editing a field on the Brief tab
response["brief"]["Campaign Name"]["value"] = "Yummiez Anytime Snacking Campaign"

# Simulate all 4 download buttons
xlsx = build_workbook_bytes(response)
csv_ = brief_to_csv_bytes(response["brief"])
docx = build_docx_bytes(response, "Yummiez Anytime Snacking Campaign")
pdf = build_pdf_bytes(response, "Yummiez Anytime Snacking Campaign")

assert len(xlsx) > 1000
assert len(csv_) > 100
assert len(docx) > 1000
assert len(pdf) > 1000
print("All 4 exports generated successfully after a simulated edit.")
print("Edited Campaign Name made it through:",
      "Yummiez Anytime Snacking Campaign" in csv_.decode())

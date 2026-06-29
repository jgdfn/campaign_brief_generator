import json
import sys
sys.path.append("..")

from exporters.excel_export import build_workbook_bytes
from exporters.csv_export import brief_to_csv_bytes
from exporters.docx_export import build_docx_bytes
from exporters.pdf_export import build_pdf_bytes

with open("yummiez_simulated_response.json") as f:
    response = json.load(f)

xlsx_bytes = build_workbook_bytes(response)
csv_bytes = brief_to_csv_bytes(response["brief"])
docx_bytes = build_docx_bytes(response, "Godrej Yummiez Influencer Campaign")
pdf_bytes = build_pdf_bytes(response, "Godrej Yummiez Influencer Campaign")

with open("test.xlsx", "wb") as f: f.write(xlsx_bytes)
with open("test.csv", "wb") as f: f.write(csv_bytes)
with open("test.docx", "wb") as f: f.write(docx_bytes)
with open("test.pdf", "wb") as f: f.write(pdf_bytes)

print("xlsx bytes:", len(xlsx_bytes))
print("csv bytes:", len(csv_bytes))
print("docx bytes:", len(docx_bytes))
print("pdf bytes:", len(pdf_bytes))
print("All 4 exporters ran successfully.")

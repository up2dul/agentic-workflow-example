from mistralai import Mistral
from dotenv import load_dotenv
import os

load_dotenv()

mistral_client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

uploaded_pdf = mistral_client.files.upload(
    file={
        "file_name": "company.pdf",
        "content": open("company.pdf", "rb"),
    },
    purpose="ocr",
)

signed_url = mistral_client.files.get_signed_url(file_id=uploaded_pdf.id)

ocr_result = mistral_client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": signed_url.url,
    },
)

pages = ocr_result.model_dump().get("pages")
all_text = ""
for page in pages:
    all_text += page.get("markdown")

with open("results/ocr_result.md", "w") as f:
    f.write(all_text)

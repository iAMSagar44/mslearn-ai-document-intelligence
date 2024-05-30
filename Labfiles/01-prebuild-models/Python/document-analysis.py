from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import requests
import logging


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

# Create a console handler
console_handler = logging.StreamHandler()
# Add the console handler to the logger
_LOGGER.addHandler(console_handler)

# Store connection information
endpoint = "https://doc-intell-rs.cognitiveservices.azure.com/"
key = "0af5e32dca5046beb0b2ef8f2189007b"

fileUri = "https://github.com/MicrosoftLearning/mslearn-ai-document-intelligence/blob/main/Labfiles/01-prebuild-models/sample-invoice/sample-invoice.pdf?raw=true"
response = requests.get(fileUri)
fileLocale = "en-US"
fileModelId = "prebuilt-invoice"

print(f"\nConnecting to Forms Recognizer at: {endpoint}")
print(f"Analyzing invoice at: {fileUri}")

# Create the client
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Analyse the invoice
poller = document_analysis_client.begin_analyze_document(model_id=fileModelId, document=response.content, locale=fileLocale)

# Display invoice information to the user
receipts = poller.result()

for idx, receipt in enumerate(receipts.documents):
    vendor_name = receipt.fields.get("VendorName")
    if vendor_name:
        print(f"Vendor Name: '{vendor_name.value}, with confidence {vendor_name.confidence}.")


    customer_name = receipt.fields.get("CustomerName")
    if customer_name:
        print(f"Customer Name: '{customer_name.value}, with confidence {customer_name.confidence}.")


    invoice_total = receipt.fields.get("InvoiceTotal")
    if invoice_total:
        print(f"Invoice Total: '{invoice_total.value.symbol}{invoice_total.value.amount}, with confidence {invoice_total.confidence}.")

print("\nAnalysis complete.\n")
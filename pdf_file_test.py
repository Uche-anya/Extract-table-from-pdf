import PyPDF2

file_path = "C:/Users/UCHE/Downloads/PaymentAdvice ANYA UCHECHUKWU.pdf"


with open(file_path, "rb") as f:
    reader = PyPDF2.PdfReader(f)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

if text.strip():
    print("This PDF is text-based.")
else:
    print("This PDF is scanned (image-based).")


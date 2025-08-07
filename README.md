# 🏥 AI Insurance Claims OCR Processor

**Automated document processing for insurance workflows using AI-powered OCR technology**

![Demo Screenshot](https://via.placeholder.com/800x400?text=Insurance+OCR+Demo+Preview)

## 📌 Introduction

An end-to-end solution that automates insurance document processing:
- Extracts key information from PDFs and images
- Supports multilingual documents (English, Chinese)
- Reduces manual data entry by 80%

## 🚀 Key Features

- **Multi-format Processing**:
  - PDF (scanned/native)
  - Images (PNG, JPG, JPEG)

- **Smart Data Extraction**:
  - Policyholder information
  - Payment methods
  - Bank account details
  - Claim-specific data

- **Advanced OCR**:
  - Tesseract 5 with LSTM
  - Custom-trained insurance terminology
  - Confidence scoring system

## 🛠 Technical Stack

| Component       | Technology |
|-----------------|------------|
| Frontend        | Streamlit  |
| OCR Engine      | Tesseract  |
| PDF Processing  | Poppler    |
| Image Handling  | PIL/Pillow |
| NLP Processing  | Regex/Spacy|

## ⚙️ Installation

### Prerequisites
- Python 3.8+
- Tesseract OCR ([Windows installer](https://github.com/UB-Mannheim/tesseract/wiki))
- Poppler ([Windows binaries](https://github.com/oschwartz10612/poppler-windows/releases))

### Setup
```bash
# Clone repository
git clone https://github.com/yourrepo/insurance-ocr.git
cd insurance-ocr

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
echo "TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe" >> .env
echo "POPPLER_PATH=C:\poppler-24.08.0\Library\bin" >> .env

# Run the application
streamlit run app.py
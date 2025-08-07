# 🏥 AI Insurance Claims OCR Processor

**Automated document processing for insurance workflows using AI-powered OCR technology**

## Demo screenshot (Above)

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
- Tesseract OCR ([Windows installer](https://github.com/UB-Mannheim/tesseract/wiki))   # Remember its location
- Poppler ([Windows binaries](https://github.com/oschwartz10612/poppler-windows/releases))   # Remember its location
#### On my computer, need to setup Environment Variables to use everywhere
window + R -> sysdm.cpl -> Advanced -> Environment Variables -> Path (System Variables) -> Edit -> New
- Tesseract OCR: path\Tesseract-OCR
- Poppler: path\Release-24.08.0-0\poppler-24.08.0-0\Library\bin
#### File main.py, change:
- TESSERACT_PATH = r'path\Tesseract-OCR\tesseract.exe'
- POPPLER_PATH = r"path\Release-24.08.0-0\poppler-24.08.0\Library\bin" if os.path.exists(r"path\Release-24.08.0-0\poppler-24.08.0\Library\bin") else None

### Setup
```bash
# Clone repository
git clone https://github.com/yourrepo/insurance-ocr.git
cd insurance-ocr

# Should create a virtual environment to avoid conflict
# Command Prompt terminal
python -m venv env # Can change the environment name "env" to what you want
venv\Scritps\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

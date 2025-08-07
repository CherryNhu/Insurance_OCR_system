import streamlit as st
import pytesseract
from PIL import Image
import pdf2image
import re
import os
import tempfile
from datetime import datetime

# ================================================
# SYSTEM CONFIGURATION (IMPORTANT)
# ================================================
# 1. Configure Tesseract OCR
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    st.error("Tesseract OCR not found. Please install it correctly")

# 2. Configure Poppler (PDF processing)
POPPLER_PATH = r"C:\Users\quynh\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin" if os.path.exists(r"C:\Users\quynh\Downloads\Release-24.08.0-0\poppler-24.08.0\Library\bin") else None
if not POPPLER_PATH:
    st.warning("Poppler not configured correctly. Some PDF features may not work")

# ================================================
# MAIN PROCESSING FUNCTIONS
# ================================================
def process_file(uploaded_file):
    """Process uploaded file and return extracted text"""
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getbuffer())
            temp_path = tmp_file.name

        # Process PDF
        if uploaded_file.type == "application/pdf":
            if not POPPLER_PATH:
                raise Exception("Poppler not installed. Cannot process PDF")
            
            images = pdf2image.convert_from_path(temp_path, poppler_path=POPPLER_PATH)
            if not images:
                raise Exception("Could not read PDF file")
            image = images[0]
        
        # Process image
        else:
            image = Image.open(temp_path)
        
        # Convert image
        image = image.convert('L')  # Grayscale
        
        # Perform OCR
        text = pytesseract.image_to_string(image, lang=st.session_state.lang, config='--oem 3 --psm 6')
        
        # Clean up
        os.unlink(temp_path)
        
        return text, image
    
    except Exception as e:
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.unlink(temp_path)
        raise e

def extract_insurance_info(text):
    """Extract key information from text"""
    data = {
        "document_type": None,
        "payment_method": None,
        "bank_account": {
            "holder": None,
            "bank": None,
            "number": None,
            "currency": None
        },
        "fps_phone": None,
        "cheque_method": None
    }
    
    # Detect document type
    if any(x in text for x in ["Insurance Claim", "Policy", "Claim Form"]):
        data["document_type"] = "Insurance Claim Form"
    
    # Payment method
    payment_patterns = {
        "Bank Transfer": r"Direct Credit|Bank Transfer",
        "FPS": r"FPS|Fast Payment",
        "Cheque": r"Cheque|Check"
    }
    
    for method, pattern in payment_patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            data["payment_method"] = method
            break
    
    # Bank information
    bank_info = re.search(r"Bank Name[:：]\s*(.+?)\n", text)
    if bank_info:
        data["bank_account"]["bank"] = bank_info.group(1).strip()
    
    # Account number
    acc_num = re.search(r"Account No\.\s*[:：]\s*([0-9A-Z\s]+)\n", text)
    if acc_num:
        data["bank_account"]["number"] = "".join(acc_num.group(1).split())
    
    # Phone number
    phone = re.search(r"Phone\s*[:：]\s*([0-9\s]+)\n", text)
    if phone:
        data["fps_phone"] = phone.group(1).replace(" ", "")
    
    return data

# ================================================
# USER INTERFACE
# ================================================
st.set_page_config(
    page_title="AI Insurance Claims Processor",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'lang' not in st.session_state:
    st.session_state.lang = "eng"

# Header
st.title("🏥 AI Insurance Claims Processor")
st.markdown("""
**Automated information extraction from insurance documents**  
Reduce manual data entry by 80% with advanced OCR technology
""")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload document (PDF/Image)",
        type=['pdf', 'png', 'jpg', 'jpeg'],
        help="Supports PDF and image files (PNG, JPG) up to 200MB"
    )
    
    st.divider()
    st.subheader("OCR Settings")
    
    # Language selection
    lang_options = {
        "English": "eng",
        "Chinese": "chi_tra",
        "Multilingual": "eng+chi_tra"
    }
    selected_lang = st.selectbox(
        "Document language",
        options=list(lang_options.keys()),
        index=0
    )
    st.session_state.lang = lang_options[selected_lang]
    
    # Display options
    st.checkbox("Show full extracted text", key="show_full_text")
    st.checkbox("Show processed image", key="show_processed_img", value=True)

# Main content
if uploaded_file:
    with st.spinner("🔄 Processing..."):
        try:
            # Process file
            text, processed_img = process_file(uploaded_file)
            
            # Extract information
            extracted_data = extract_insurance_info(text)
            
            # Display results
            st.success("✅ Processing completed!")
            
            # Display tabs
            tab1, tab2 = st.tabs(["Extracted Information", "Raw Data"])
            
            with tab1:
                st.subheader("📋 Extracted Information")
                
                # Display in columns
                cols = st.columns(2)
                
                with cols[0]:
                    st.markdown("**General Information**")
                    st.metric("Document Type", extracted_data["document_type"] or "Not detected")
                    st.metric("Payment Method", extracted_data["payment_method"] or "Not detected")
                
                with cols[1]:
                    st.markdown("**Bank Information**")
                    if extracted_data["bank_account"]["bank"]:
                        st.metric("Bank Name", extracted_data["bank_account"]["bank"])
                    if extracted_data["bank_account"]["number"]:
                        st.metric("Account Number", extracted_data["bank_account"]["number"])
                    if extracted_data["fps_phone"]:
                        st.metric("FPS Phone", f"+852 {extracted_data['fps_phone']}")
                
                if st.session_state.show_processed_img:
                    st.divider()
                    st.subheader("🖼️ Processed Image")
                    st.image(processed_img, caption="Image processed for OCR", use_container_width=True)
            
            with tab2:
                st.subheader("📜 Raw Extracted Text")
                st.text_area("Content", text, height=300)
                
                st.download_button(
                    "📥 Download Text",
                    data=text,
                    file_name="extracted_text.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            if "Poppler" in str(e):
                st.warning("""
                **Fixing Poppler Error:**
                1. Download Poppler from [official page](https://github.com/oschwartz10612/poppler-windows/releases)
                2. Extract to `C:\\poppler-24.08.0`
                3. Add to PATH: `C:\\poppler-24.08.0\\Library\\bin`
                """)
else:
    st.info("ℹ️ Please upload an insurance document to begin")
    st.image("https://via.placeholder.com/800x400?text=Upload+PDF+or+image+document", use_container_width=True)

# ================================================
# CUSTOM CSS
# ================================================
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #f0f2f6;
    }
    .stMarkdown h3 {
        border-bottom: 1px solid #eee;
        padding-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)
import streamlit as st
import numpy as np
import pandas as pd
import io
import json
import base64
import os
import tempfile
import sys

# Configure Streamlit page
st.set_page_config(
    page_title="Hybrid Cryptographic System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add current directory to Python path for imports
if os.path.dirname(__file__) not in sys.path:
    sys.path.append(os.path.dirname(__file__))

try:
    from PIL import Image
except ImportError:
    st.error("PIL/Pillow not available. Please check requirements.txt")
    st.stop()

# Import our custom modules with error handling
try:
    from hill_cipher import HillCipher
    from sdes import SDES
    from steganography import Steganography
    from hybrid_model import HybridCryptoModel
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.info("Ensure all Python files are deployed together.")
    
    # Show available files for debugging
    st.write("Available files in directory:")
    try:
        files = os.listdir(os.path.dirname(__file__) or '.')
        st.write([f for f in files if f.endswith('.py')])
    except:
        st.write("Cannot list directory contents")
    st.stop()

def main():
    # Title and description
    st.title("🔐 Hybrid Cryptographic System")
    st.markdown("""
    ### Hill Cipher + SDES + Steganography
    
    **Developed by:** Murali V, Siddarth Gowtham, Kalaiyarasan  
    **Course:** Cryptography and Network Security (Sem 7)
    
    This application implements a hybrid cryptographic model that combines three security techniques:
    1. **Hill Cipher** - Classical cipher using matrix algebra
    2. **SDES** - Simplified Data Encryption Standard
    3. **Steganography** - Hide encrypted data in images
    """)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    tab_selection = st.sidebar.selectbox(
        "Choose Algorithm",
        ["🏠 Home", "🔑 Hill Cipher", "🔒 SDES", "🖼️ Steganography", "🔐 Hybrid Model"]
    )
    
    # Initialize session state
    if 'keys' not in st.session_state:
        st.session_state.keys = {}
    if 'results' not in st.session_state:
        st.session_state.results = {}
    
    # Route to appropriate tab
    if tab_selection == "🏠 Home":
        home_tab()
    elif tab_selection == "🔑 Hill Cipher":
        hill_cipher_tab()
    elif tab_selection == "🔒 SDES":
        sdes_tab()
    elif tab_selection == "🖼️ Steganography":
        steganography_tab()
    elif tab_selection == "🔐 Hybrid Model":
        hybrid_model_tab()

def home_tab():
    st.header("🏠 Welcome to Hybrid Cryptographic System")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔑 Hill Cipher")
        st.write("Classical cipher using 2×2 matrix operations")
        st.info("• Matrix-based encryption\n• Linear algebra operations\n• Key: 2×2 invertible matrix")
    
    with col2:
        st.subheader("🔒 SDES")
        st.write("Simplified Data Encryption Standard")
        st.info("• Block cipher algorithm\n• 10-bit key generation\n• S-box substitutions")
    
    with col3:
        st.subheader("🖼️ Steganography")
        st.write("Hide data within image files")
        st.info("• LSB technique\n• Image-based hiding\n• Invisible to naked eye")
    
    st.markdown("---")
    
    st.subheader("🔐 Hybrid Security Flow")
    st.markdown("""
    ```
    Plaintext → Hill Cipher → SDES → Steganography → Secure Image
    ```
    """)
    
    # System overview
    st.subheader("📊 System Features")
    
    features = {
        "Feature": ["Multi-layer Security", "Key Management", "File Operations", "Visual Interface"],
        "Description": [
            "Three independent cryptographic layers",
            "Automatic key generation and storage",
            "Image upload/download capabilities",
            "Interactive Streamlit interface"
        ],
        "Status": ["✅ Implemented", "✅ Implemented", "✅ Implemented", "✅ Implemented"]
    }
    
    df = pd.DataFrame(features)
    st.table(df)

def hill_cipher_tab():
    st.header("🔑 Hill Cipher")
    st.write("Classical cryptography using matrix algebra")
    
    try:
        hill = HillCipher()
        
        # Operation selection
        operation = st.radio("Select Operation", ["Encrypt", "Decrypt"], horizontal=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input")
            
            # Text input
            if operation == "Encrypt":
                text = st.text_area("Enter plaintext to encrypt:", height=100)
            else:
                text = st.text_area("Enter ciphertext to decrypt:", height=100)
            
            # Key matrix input
            st.subheader("Key Matrix (2×2)")
            key_method = st.radio("Key Input Method", ["Manual Entry", "Generate Random"], horizontal=True)
            
            if key_method == "Manual Entry":
                col_a, col_b = st.columns(2)
                with col_a:
                    k11 = st.number_input("Matrix[0,0]", min_value=0, max_value=25, value=3, key="hill_k11")
                    k21 = st.number_input("Matrix[1,0]", min_value=0, max_value=25, value=5, key="hill_k21")
                with col_b:
                    k12 = st.number_input("Matrix[0,1]", min_value=0, max_value=25, value=2, key="hill_k12")
                    k22 = st.number_input("Matrix[1,1]", min_value=0, max_value=25, value=7, key="hill_k22")
                
                key_matrix = np.array([[k11, k12], [k21, k22]])
            else:
                if st.button("Generate Random Key", key="hill_random"):
                    key_matrix = hill.generate_random_key()
                    st.session_state.hill_key = key_matrix
                
                if 'hill_key' in st.session_state:
                    key_matrix = st.session_state.hill_key
                else:
                    key_matrix = np.array([[3, 2], [5, 7]])
            
            st.write("Key Matrix:")
            st.write(key_matrix)
            
            # Validate key
            if hill.validate_key_matrix(key_matrix):
                st.success("✅ Valid key matrix")
            else:
                st.error("❌ Invalid key matrix (not invertible mod 26)")
        
        with col2:
            st.subheader("Output")
            
            if st.button(f"{operation} Text", key="hill_process"):
                if text and hill.validate_key_matrix(key_matrix):
                    try:
                        if operation == "Encrypt":
                            result = hill.encrypt(text, key_matrix)
                            st.success(f"**Encrypted Text:** {result}")
                        else:
                            result = hill.decrypt(text, key_matrix)
                            st.success(f"**Decrypted Text:** {result}")
                        
                        # Store result for download
                        st.session_state.hill_result = result
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    if not text:
                        st.warning("Please enter text to process")
                    if not hill.validate_key_matrix(key_matrix):
                        st.error("Please use a valid key matrix")
            
            # Download result
            if 'hill_result' in st.session_state:
                st.download_button(
                    "Download Result",
                    st.session_state.hill_result,
                    f"hill_{operation.lower()}_result.txt",
                    "text/plain"
                )
                
    except Exception as e:
        st.error(f"Hill Cipher module error: {str(e)}")

def sdes_tab():
    st.header("🔒 SDES (Simplified Data Encryption Standard)")
    st.write("Block cipher with 10-bit key")
    
    try:
        sdes = SDES()
        
        # Operation selection
        operation = st.radio("Select Operation", ["Encrypt", "Decrypt"], horizontal=True, key="sdes_op")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input")
            
            # Text input
            if operation == "Encrypt":
                text = st.text_area("Enter plaintext to encrypt:", height=100, key="sdes_text")
            else:
                text = st.text_area("Enter binary ciphertext to decrypt:", height=100, key="sdes_text")
            
            # Key input
            st.subheader("SDES Key (10 bits)")
            key_method = st.radio("Key Input Method", ["Manual Entry", "Generate Random"], horizontal=True, key="sdes_key_method")
            
            if key_method == "Manual Entry":
                sdes_key = st.text_input("Enter 10-bit binary key:", value="1010000010", max_chars=10)
                
                # Validate key
                if len(sdes_key) == 10 and all(c in '01' for c in sdes_key):
                    st.success("✅ Valid SDES key")
                else:
                    st.error("❌ Key must be exactly 10 binary digits (0s and 1s)")
            else:
                if st.button("Generate Random Key", key="sdes_random"):
                    sdes_key = sdes.generate_random_key()
                    st.session_state.sdes_key = sdes_key
                
                if 'sdes_key' in st.session_state:
                    sdes_key = st.session_state.sdes_key
                else:
                    sdes_key = "1010000010"
            
            st.code(f"Key: {sdes_key}")
        
        with col2:
            st.subheader("Output")
            
            if st.button(f"{operation} Text", key="sdes_process"):
                if text and len(sdes_key) == 10 and all(c in '01' for c in sdes_key):
                    try:
                        if operation == "Encrypt":
                            result = sdes.encrypt_text(text, sdes_key)
                            st.success("**Encrypted (Binary):**")
                            st.code(result)
                        else:
                            result = sdes.decrypt_text(text, sdes_key)
                            st.success(f"**Decrypted Text:** {result}")
                        
                        # Store result for download
                        st.session_state.sdes_result = result
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    if not text:
                        st.warning("Please enter text to process")
                    else:
                        st.error("Please enter a valid 10-bit binary key")
            
            # Download result
            if 'sdes_result' in st.session_state:
                st.download_button(
                    "Download Result",
                    st.session_state.sdes_result,
                    f"sdes_{operation.lower()}_result.txt",
                    "text/plain"
                )
                
    except Exception as e:
        st.error(f"SDES module error: {str(e)}")

def steganography_tab():
    st.header("🖼️ Image Steganography")
    st.write("Hide secret messages in images using LSB technique")
    
    try:
        stego = Steganography()
        
        # Operation selection
        operation = st.radio("Select Operation", ["Hide Message", "Extract Message"], horizontal=True, key="stego_op")
        
        if operation == "Hide Message":
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Input")
                
                # Message input
                message = st.text_area("Enter secret message:", height=100)
                
                # Image upload
                uploaded_file = st.file_uploader("Choose cover image", type=['png', 'jpg', 'jpeg'])
                
                if uploaded_file is None:
                    if st.button("Create Sample Image"):
                        try:
                            sample_path = stego.create_sample_image(width=400, height=300)
                            with open(sample_path, "rb") as f:
                                st.download_button(
                                    "Download Sample Image",
                                    f.read(),
                                    "sample_image.png",
                                    "image/png"
                                )
                        except Exception as e:
                            st.error(f"Could not create sample image: {e}")
                else:
                    # Show uploaded image
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Cover Image", use_column_width=True)
                    
                    # Show capacity
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                            image.save(tmp_file.name)
                            max_chars, total_bits = stego.get_image_capacity(tmp_file.name)
                            st.info(f"Image capacity: {max_chars} characters ({total_bits} bits)")
                            os.unlink(tmp_file.name)
                    except Exception as e:
                        st.warning(f"Could not calculate capacity: {e}")
            
            with col2:
                st.subheader("Output")
                
                if st.button("Hide Message") and message and uploaded_file:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_input:
                            image = Image.open(uploaded_file)
                            image.save(tmp_input.name)
                            
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_output:
                                # Hide message
                                output_path, hidden_bits = stego.hide_message(tmp_input.name, message, tmp_output.name)
                                
                                # Show result
                                stego_image = Image.open(output_path)
                                st.image(stego_image, caption="Steganographic Image", use_column_width=True)
                                
                                st.success(f"Message hidden successfully! ({hidden_bits} bits)")
                                
                                # Download button
                                with open(output_path, "rb") as f:
                                    st.download_button(
                                        "Download Stego Image",
                                        f.read(),
                                        "stego_image.png",
                                        "image/png"
                                    )
                            
                            # Clean up
                            os.unlink(tmp_input.name)
                            os.unlink(tmp_output.name)
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Extract Message
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Input")
                
                # Image upload
                uploaded_file = st.file_uploader("Choose steganographic image", type=['png', 'jpg', 'jpeg'], key="extract_img")
                
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Steganographic Image", use_column_width=True)
            
            with col2:
                st.subheader("Output")
                
                if st.button("Extract Message") and uploaded_file:
                    try:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                            image = Image.open(uploaded_file)
                            image.save(tmp_file.name)
                            
                            # Extract message
                            extracted_message = stego.extract_message(tmp_file.name)
                            
                            if extracted_message:
                                st.success("**Extracted Message:**")
                                st.text_area("", value=extracted_message, height=100, key="extracted_msg")
                                
                                # Download button
                                st.download_button(
                                    "Download Message",
                                    extracted_message,
                                    "extracted_message.txt",
                                    "text/plain"
                                )
                            else:
                                st.warning("No hidden message found in the image")
                            
                            # Clean up
                            os.unlink(tmp_file.name)
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        
    except Exception as e:
        st.error(f"Steganography module error: {str(e)}")

def hybrid_model_tab():
    st.header("🔐 Hybrid Cryptographic Model")
    st.write("Triple-layer security: Hill Cipher → SDES → Steganography")
    
    try:
        hybrid = HybridCryptoModel()
        
        # Operation selection
        operation = st.radio("Select Operation", ["Encrypt", "Decrypt"], horizontal=True, key="hybrid_op")
        
        if operation == "Encrypt":
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Input")
                
                # Text input
                plaintext = st.text_area("Enter plaintext to encrypt:", height=100, key="hybrid_text")
                
                # Key management
                st.subheader("Key Management")
                key_option = st.radio("Key Option", ["Auto Generate", "Manual Entry"], key="hybrid_key_option")
                
                if key_option == "Manual Entry":
                    # Hill Cipher key
                    st.write("**Hill Cipher Key (2×2 Matrix):**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        h11 = st.number_input("Matrix[0,0]", min_value=0, max_value=25, value=3, key="hybrid_h11")
                        h21 = st.number_input("Matrix[1,0]", min_value=0, max_value=25, value=5, key="hybrid_h21")
                    with col_b:
                        h12 = st.number_input("Matrix[0,1]", min_value=0, max_value=25, value=2, key="hybrid_h12")
                        h22 = st.number_input("Matrix[1,1]", min_value=0, max_value=25, value=7, key="hybrid_h22")
                    
                    hill_key = np.array([[h11, h12], [h21, h22]])
                    
                    # SDES key
                    sdes_key = st.text_input("SDES Key (10 bits):", value="1010000010", max_chars=10, key="hybrid_sdes")
                
                # Cover image (optional)
                st.subheader("Cover Image (Optional)")
                uploaded_file = st.file_uploader("Choose cover image", type=['png', 'jpg', 'jpeg'], key="hybrid_cover")
                
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Cover Image", width=300)
            
            with col2:
                st.subheader("Output")
                
                if st.button("🔐 Hybrid Encrypt", key="hybrid_encrypt_btn"):
                    if plaintext:
                        try:
                            # Prepare parameters
                            hill_key_param = None if key_option == "Auto Generate" else hill_key
                            sdes_key_param = None if key_option == "Auto Generate" else sdes_key
                            image_path = None
                            
                            # Handle cover image
                            if uploaded_file:
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                                    image = Image.open(uploaded_file)
                                    image.save(tmp_file.name)
                                    image_path = tmp_file.name
                            
                            # Encrypt
                            with st.spinner("Encrypting..."):
                                result = hybrid.hybrid_encrypt(
                                    plaintext, 
                                    hill_key_param, 
                                    sdes_key_param, 
                                    image_path
                                )
                            
                            if result['success']:
                                st.success("✅ Hybrid encryption completed!")
                                
                                # Show encrypted image
                                stego_image = Image.open(result['encrypted_image_path'])
                                st.image(stego_image, caption="Encrypted Image", width=300)
                                
                                # Show keys used
                                st.subheader("🔑 Keys Used")
                                st.json(result['keys'])
                                
                                # Download buttons
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    with open(result['encrypted_image_path'], "rb") as f:
                                        st.download_button(
                                            "Download Encrypted Image",
                                            f.read(),
                                            "hybrid_encrypted.png",
                                            "image/png"
                                        )
                                
                                with col_b:
                                    keys_json = json.dumps(result['keys'], indent=2)
                                    st.download_button(
                                        "Download Keys",
                                        keys_json,
                                        "hybrid_keys.json",
                                        "application/json"
                                    )
                                
                                # Store for session
                                st.session_state.hybrid_result = result
                                
                            else:
                                st.error(f"❌ Encryption failed: {result['error']}")
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.warning("Please enter plaintext to encrypt")
        
        else:  # Decrypt
            st.info("Decryption functionality requires both the encrypted image and the original keys.")
            st.write("For the demo, you can use the encrypt function first to generate test data.")
            
    except Exception as e:
        st.error(f"Hybrid model error: {str(e)}")
        st.info("Some features may be limited in the cloud environment.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or check the deployment logs.")
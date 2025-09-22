# 🔐 Hybrid Cryptographic Model
## Hill Cipher + SDES + Steganography

### 📋 Project Overview

A comprehensive **triple-layer cryptographic security system** that combines three different cryptographic techniques to provide enhanced data protection:

1. **🔑 Hill Cipher** - Classical cryptography using 2×2 matrix algebra
2. **🔒 SDES** - Simplified Data Encryption Standard with block encryption  
3. **🖼️ Steganography** - Hide encrypted data within image files using LSB technique

### ✨ Key Features

- ✅ **Multi-layer Security**: Three independent encryption layers
- ✅ **Interactive Web Interface**: User-friendly Streamlit application
- ✅ **Individual Algorithm Testing**: Test each component separately
- ✅ **Complete Hybrid Pipeline**: Full encryption/decryption workflow
- ✅ **File Operations**: Upload/download images and text files
- ✅ **Key Management**: Auto-generation and manual key entry
- ✅ **Visual Feedback**: Real-time encryption status and results
- ✅ **Error Handling**: Comprehensive validation and error messages

### 🚀 Quick Start

#### 1. Installation
```bash
# Clone or download the project
cd Hybrid_Crypto_Project

# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit numpy Pillow opencv-python matplotlib
```

#### 2. Run Application
```bash
# Method 1: Using Streamlit
streamlit run app.py

# Method 2: Using deployment script
python run_system.py

# Method 3: Quick demo (no GUI)
python demo.py
```

#### 3. Test System
```bash
# Run comprehensive tests
python test_system.py

# Test individual components
python hill_cipher.py
python sdes.py
python steganography.py
```

### 🔐 Security Architecture

#### Encryption Flow
```
Plaintext → Hill Cipher → SDES → Steganography → Secure Image
```

#### Decryption Flow  
```
Secure Image → Extract → SDES Decrypt → Hill Cipher Decrypt → Plaintext
```

#### Security Layers
1. **Layer 1 (Hill Cipher)**: Matrix-based classical encryption
2. **Layer 2 (SDES)**: Modern block cipher with key scheduling
3. **Layer 3 (Steganography)**: Visual hiding in image pixels

### 📖 Algorithm Details

#### 🔑 Hill Cipher
- **Method**: 2×2 matrix multiplication modulo 26
- **Key**: Invertible integer matrix with gcd(det, 26) = 1  
- **Block Size**: 2 characters
- **Strength**: Resistant to frequency analysis

#### 🔒 SDES (Simplified DES)
- **Key Size**: 10 bits with subkey generation
- **Block Size**: 8 bits
- **Rounds**: 2 with function f and S-boxes
- **Features**: Permutation, substitution, XOR operations

#### 🖼️ Steganography  
- **Technique**: LSB (Least Significant Bit) modification
- **Capacity**: Depends on image size (8 bits per pixel channel)
- **Formats**: PNG, JPG, JPEG support
- **Detection**: Invisible to human visual system

### 🖥️ User Interface

The Streamlit web application provides:

#### 🏠 Home Tab
- System overview and features
- Algorithm descriptions  
- Security flow visualization

#### 🔑 Hill Cipher Tab
- Text encryption/decryption
- Manual key entry or auto-generation
- Key validation and matrix display

#### 🔒 SDES Tab  
- Binary and text mode encryption
- 10-bit key management
- Step-by-step process visualization

#### 🖼️ Steganography Tab
- Image upload and processing
- Message hiding and extraction
- Capacity calculation and comparison

#### 🔐 Hybrid Model Tab
- Complete pipeline encryption/decryption
- Multi-layer key management
- Progress tracking and results

### 📁 Project Structure

```
Hybrid_Crypto_Project/
├── app.py                 # Main Streamlit application
├── hill_cipher.py         # Hill Cipher implementation
├── sdes.py               # SDES algorithm implementation  
├── steganography.py      # Image steganography module
├── hybrid_model.py       # Complete hybrid system
├── test_system.py        # Comprehensive test suite
├── demo.py              # Quick demo script
├── run_system.py        # Deployment and setup script
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

### 🧪 Testing & Validation

The system includes comprehensive testing:

- **Unit Tests**: Individual algorithm validation
- **Integration Tests**: Hybrid pipeline testing  
- **Performance Tests**: Speed and capacity measurements
- **Security Tests**: Key validation and error handling

**Test Results**: All core components pass validation ✅

### 🔧 Configuration

#### System Requirements
- **Python**: 3.7+ (tested with 3.13)
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB for dependencies
- **Network**: Optional (for Streamlit web interface)

#### Dependencies
- `streamlit` - Web interface framework
- `numpy` - Matrix operations for Hill Cipher
- `Pillow` - Image processing for steganography  
- `opencv-python` - Advanced image operations
- `matplotlib` - Visualization support

### 🎯 Use Cases

1. **Educational**: Learn cryptographic concepts interactively
2. **Research**: Test multi-layer security approaches
3. **Security Training**: Understand encryption workflows
4. **Data Protection**: Secure sensitive information in images
5. **Academic Projects**: Cryptography course assignments

### 🚨 Security Considerations

#### Strengths
- ✅ Multiple independent encryption layers
- ✅ Different mathematical approaches per layer
- ✅ Visual hiding provides additional security
- ✅ Key diversity reduces single-point failure

#### Limitations  
- ⚠️ Hill Cipher vulnerable to known-plaintext attacks
- ⚠️ SDES is simplified (educational version)
- ⚠️ Steganography detectable by statistical analysis
- ⚠️ Not intended for production security systems

### � Development Team

**Team Members:**
- **Murali V** - Lead Developer & System Architecture
- **Siddarth Gowtham** - Algorithm Implementation & Testing  
- **Kalaiyarasan** - UI Design & Documentation

**Course**: Cryptography and Network Security (Sem 7)  
**Institution**: [Your College/University]  
**Language**: Python 3.13  
**Framework**: Streamlit  
**License**: Educational Use Only

### 📞 Support & Contribution

For issues, suggestions, or contributions:
1. Test the system using `python demo.py`
2. Run full test suite with `python test_system.py`  
3. Check error logs in the application
4. Refer to algorithm documentation in source files

### 🏆 Project Status

- ✅ **Hill Cipher**: Fully implemented and tested
- ✅ **SDES**: Complete with all operations  
- ✅ **Steganography**: LSB technique working
- ✅ **Hybrid Model**: End-to-end pipeline functional
- ✅ **Web Interface**: Streamlit app ready
- ✅ **Testing**: Comprehensive validation complete
- ✅ **Documentation**: Complete user guide

**Status**: 🎉 **READY FOR USE** 🎉
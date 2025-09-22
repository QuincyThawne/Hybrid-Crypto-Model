#!/usr/bin/env python3
"""
Deployment and Setup Script for Hybrid Cryptographic System
Handles installation, testing, and running the application
"""

import os
import sys
import subprocess
import platform


def print_banner():
    """Print application banner"""
    print("🔐" + "=" * 58 + "🔐")
    print("   HYBRID CRYPTOGRAPHIC SYSTEM - DEPLOYMENT SCRIPT")
    print("   Hill Cipher + SDES + Steganography")
    print("🔐" + "=" * 58 + "🔐")


def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    requirements = [
        "streamlit>=1.28.1",
        "numpy>=1.24.3",
        "Pillow>=10.0.1",
        "opencv-python>=4.8.1.78",
        "matplotlib>=3.7.2"
    ]
    
    for package in requirements:
        try:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {package}")
            return False
    
    return True


def run_tests():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        # Import and run tests
        from test_system import TestRunner
        runner = TestRunner()
        success = runner.run_all_tests()
        return success
    except ImportError:
        print("❌ Could not import test system")
        return False
    except Exception as e:
        print(f"❌ Test execution failed: {str(e)}")
        return False


def create_sample_files():
    """Create sample files for demonstration"""
    print("\n📄 Creating sample files...")
    
    try:
        # Create sample text file
        sample_text = """
# Sample Plaintext for Hybrid Encryption

This is a sample message that will be encrypted using our hybrid cryptographic system.

The message will go through three layers of security:
1. Hill Cipher - Classical matrix-based encryption
2. SDES - Simplified Data Encryption Standard  
3. Steganography - Hide the result in an image

This demonstrates multi-layer security in action!

Test data: ABCDEFGHIJKLMNOPQRSTUVWXYZ
Numbers: 1234567890
Special: !@#$%^&*()
        """.strip()
        
        with open("sample_plaintext.txt", "w") as f:
            f.write(sample_text)
        
        print("   ✅ Created sample_plaintext.txt")
        
        # Create sample image using steganography module
        try:
            from steganography import Steganography
            stego = Steganography()
            sample_image = stego.create_sample_image(800, 600, "sample_cover_image.png")
            print(f"   ✅ Created {sample_image}")
        except:
            print("   ⚠️  Could not create sample image")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating sample files: {str(e)}")
        return False


def run_streamlit_app():
    """Run the Streamlit application"""
    print("\n🚀 Starting Streamlit application...")
    print("   The app will open in your default browser")
    print("   Use Ctrl+C to stop the application")
    print("   " + "-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {str(e)}")


def main():
    """Main deployment function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_requirements():
        print("\n❌ Failed to install required packages")
        return False
    
    # Run tests
    print("\n" + "=" * 60)
    test_success = run_tests()
    
    if not test_success:
        print("\n⚠️  Some tests failed. The application may not work correctly.")
        response = input("Do you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Create sample files
    create_sample_files()
    
    # Show usage information
    print("\n" + "=" * 60)
    print("📚 USAGE INFORMATION")
    print("=" * 60)
    print("""
The Hybrid Cryptographic System is now ready!

🔧 Manual Commands:
   python app.py                    # Run Streamlit app
   python test_system.py           # Run tests only
   python hybrid_model.py          # Test hybrid model
   python hill_cipher.py           # Test Hill Cipher
   python sdes.py                  # Test SDES
   python steganography.py         # Test Steganography

📁 Files Created:
   • app.py                       # Main Streamlit application
   • hybrid_model.py              # Complete hybrid system
   • hill_cipher.py               # Hill Cipher implementation
   • sdes.py                      # SDES implementation  
   • steganography.py             # Steganography implementation
   • test_system.py               # Comprehensive test suite
   • sample_plaintext.txt         # Sample text for testing
   • sample_cover_image.png       # Sample image for steganography

🌐 Web Interface:
   The Streamlit app provides an easy-to-use web interface with:
   • Individual algorithm testing
   • Complete hybrid encryption/decryption
   • File upload/download capabilities
   • Key management
   • Visual feedback
    """)
    
    # Ask if user wants to run the app
    print("\n" + "=" * 60)
    response = input("🚀 Do you want to start the Streamlit app now? (Y/n): ")
    
    if response.lower() != 'n':
        run_streamlit_app()
    else:
        print("\n✅ Setup completed successfully!")
        print("   Run 'streamlit run app.py' when ready to start the application")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
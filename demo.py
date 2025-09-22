"""
Quick Demo Script for Hybrid Cryptographic System
Tests core algorithms without GUI dependencies
"""

import numpy as np
import sys
import os

# Import our modules
from hill_cipher import HillCipher
from sdes import SDES

def demo_hill_cipher():
    """Demonstrate Hill Cipher"""
    print("🔑 HILL CIPHER DEMO")
    print("-" * 40)
    
    hill = HillCipher()
    
    # Test data
    plaintext = "HELLO WORLD"
    key_matrix = np.array([[3, 2], [5, 7]])
    
    print(f"Plaintext: {plaintext}")
    print(f"Key Matrix:\n{key_matrix}")
    
    # Encrypt
    encrypted = hill.encrypt(plaintext, key_matrix)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = hill.decrypt(encrypted, key_matrix)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    original = plaintext.upper().replace(" ", "")
    success = original == decrypted.rstrip('X')
    print(f"✅ Success: {success}")
    
    return success

def demo_sdes():
    """Demonstrate SDES"""
    print("\n🔒 SDES DEMO")
    print("-" * 40)
    
    sdes = SDES()
    
    # Test data
    plaintext = "Hello World!"
    key = "1010000010"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Encrypt
    encrypted_binary = sdes.encrypt_text(plaintext, key)
    print(f"Encrypted (binary): {encrypted_binary[:50]}...")
    
    # Decrypt
    decrypted = sdes.decrypt_text(encrypted_binary, key)
    print(f"Decrypted: {decrypted}")
    
    # Verify
    success = plaintext == decrypted
    print(f"✅ Success: {success}")
    
    return success

def demo_hybrid_crypto():
    """Demonstrate hybrid encryption workflow"""
    print("\n🔐 HYBRID CRYPTO DEMO")
    print("-" * 40)
    
    # Initialize
    hill = HillCipher()
    sdes = SDES()
    
    # Test data
    plaintext = "SECRET MESSAGE"
    hill_key = np.array([[3, 2], [5, 7]])
    sdes_key = "1010000010"
    
    print(f"Original: {plaintext}")
    print(f"Hill Key: {hill_key.tolist()}")
    print(f"SDES Key: {sdes_key}")
    
    try:
        # Step 1: Hill Cipher
        print(f"\n📝 Step 1: Hill Cipher")
        hill_encrypted = hill.encrypt(plaintext, hill_key)
        print(f"   Result: {hill_encrypted}")
        
        # Step 2: SDES
        print(f"\n🔒 Step 2: SDES")
        sdes_encrypted = sdes.encrypt_text(hill_encrypted, sdes_key)
        print(f"   Result: {sdes_encrypted[:50]}... ({len(sdes_encrypted)} bits)")
        
        # Note: Step 3 would be steganography (image hiding)
        print(f"\n🖼️  Step 3: Steganography (simulated)")
        print(f"   [Binary data would be hidden in image LSBs]")
        
        print(f"\n🔓 DECRYPTION PROCESS")
        print("-" * 40)
        
        # Reverse Step 2: SDES Decrypt
        print(f"🔒 Step 1: SDES Decrypt")
        sdes_decrypted = sdes.decrypt_text(sdes_encrypted, sdes_key)
        print(f"   Result: {sdes_decrypted}")
        
        # Reverse Step 1: Hill Cipher Decrypt
        print(f"🔑 Step 2: Hill Cipher Decrypt")
        final_result = hill.decrypt(sdes_decrypted, hill_key)
        print(f"   Result: {final_result}")
        
        # Verify
        original = plaintext.upper().replace(" ", "")
        decrypted = final_result.rstrip('X')
        success = original == decrypted
        
        print(f"\n✅ Hybrid Success: {success}")
        print(f"   Original: {original}")
        print(f"   Final:    {decrypted}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Main demo function"""
    print("🔐 HYBRID CRYPTOGRAPHIC SYSTEM - QUICK DEMO")
    print("Developed by: Murali V, Siddarth Gowtham, Kalaiyarasan")
    print("Course: Cryptography and Network Security (Sem 7)")
    print("=" * 60)
    
    results = []
    
    # Test individual components
    results.append(demo_hill_cipher())
    results.append(demo_sdes())
    results.append(demo_hybrid_crypto())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    
    tests = ["Hill Cipher", "SDES", "Hybrid System"]
    
    for i, (test, result) in enumerate(zip(tests, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test}")
    
    all_passed = all(results)
    
    if all_passed:
        print(f"\n🎉 ALL DEMOS SUCCESSFUL!")
        print(f"The hybrid cryptographic system is working correctly.")
        print(f"\nNext steps:")
        print(f"  1. Install Pillow: pip install Pillow")
        print(f"  2. Run Streamlit app: streamlit run app.py")
    else:
        print(f"\n⚠️  Some demos failed. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
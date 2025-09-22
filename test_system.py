#!/usr/bin/env python3
"""
Comprehensive Test Suite for Hybrid Cryptographic System
Tests all components individually and as a complete system
"""

import sys
import os
import numpy as np
import tempfile
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hill_cipher import HillCipher
from sdes import SDES
from steganography import Steganography
from hybrid_model import HybridCryptoModel


class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
    
    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self.test_results.append(result)
        
        if passed:
            self.tests_passed += 1
            print(f"✅ {test_name}: {status} {message}")
        else:
            self.tests_failed += 1
            print(f"❌ {test_name}: {status} - {message}")
    
    def test_hill_cipher(self):
        """Test Hill Cipher implementation"""
        print("\n🔑 Testing Hill Cipher...")
        hill = HillCipher()
        
        try:
            # Test 1: Basic encryption/decryption
            key = np.array([[3, 2], [5, 7]])
            plaintext = "HELLO"
            
            encrypted = hill.encrypt(plaintext, key)
            decrypted = hill.decrypt(encrypted, key)
            
            self.log_test("Hill Cipher Basic", plaintext == decrypted, f"'{plaintext}' -> '{encrypted}' -> '{decrypted}'")
            
            # Test 2: Key validation
            valid_key = np.array([[3, 2], [5, 7]])
            invalid_key = np.array([[2, 4], [1, 2]])  # det = 0
            
            self.log_test("Hill Key Validation (Valid)", hill.validate_key_matrix(valid_key), "Valid key accepted")
            self.log_test("Hill Key Validation (Invalid)", not hill.validate_key_matrix(invalid_key), "Invalid key rejected")
            
            # Test 3: Random key generation
            random_key = hill.generate_random_key()
            is_valid = hill.validate_key_matrix(random_key)
            
            self.log_test("Hill Random Key", is_valid, f"Generated valid random key: {random_key.tolist()}")
            
            # Test 4: Long text handling
            long_text = "This is a longer message to test the Hill Cipher with multiple blocks"
            long_encrypted = hill.encrypt(long_text, key)
            long_decrypted = hill.decrypt(long_encrypted, key)
            
            # Remove padding for comparison
            original_upper = long_text.upper().replace(" ", "")
            decrypted_clean = long_decrypted.rstrip('X')
            
            self.log_test("Hill Long Text", original_upper == decrypted_clean, f"Length: {len(long_text)} chars")
            
        except Exception as e:
            self.log_test("Hill Cipher Error", False, str(e))
    
    def test_sdes(self):
        """Test SDES implementation"""
        print("\n🔒 Testing SDES...")
        sdes = SDES()
        
        try:
            # Test 1: Basic encryption/decryption
            key = "1010000010"
            plaintext = "Hello"
            
            encrypted_bits = sdes.encrypt(plaintext, key)
            decrypted_bits = sdes.decrypt(encrypted_bits, key)
            decrypted_text = sdes.bits_to_string(decrypted_bits)
            
            self.log_test("SDES Basic", plaintext == decrypted_text, f"'{plaintext}' -> bits -> '{decrypted_text}'")
            
            # Test 2: Text encryption/decryption
            encrypted_binary = sdes.encrypt_text(plaintext, key)
            decrypted_text2 = sdes.decrypt_text(encrypted_binary, key)
            
            self.log_test("SDES Text Mode", plaintext == decrypted_text2, f"Binary length: {len(encrypted_binary)}")
            
            # Test 3: Key validation
            valid_key = "1010000010"
            invalid_key1 = "101000001"  # Too short
            invalid_key2 = "10100000102"  # Invalid character
            
            try:
                sdes.generate_keys(valid_key)
                valid_key_test = True
            except:
                valid_key_test = False
            
            self.log_test("SDES Valid Key", valid_key_test, "10-bit key accepted")
            
            # Test 4: Random key generation
            random_key = sdes.generate_random_key()
            is_10_bits = len(random_key) == 10 and all(c in '01' for c in random_key)
            
            self.log_test("SDES Random Key", is_10_bits, f"Generated: {random_key}")
            
        except Exception as e:
            self.log_test("SDES Error", False, str(e))
    
    def test_steganography(self):
        """Test Steganography implementation"""
        print("\n🖼️  Testing Steganography...")
        stego = Steganography()
        
        try:
            # Test 1: Create sample image
            sample_image = stego.create_sample_image(width=200, height=150, output_path="test_sample.png")
            image_exists = os.path.exists(sample_image)
            
            self.log_test("Stego Sample Image", image_exists, f"Created: {sample_image}")
            
            if image_exists:
                # Test 2: Image capacity calculation
                max_chars, total_bits = stego.get_image_capacity(sample_image)
                capacity_reasonable = max_chars > 100  # Should be able to hold reasonable message
                
                self.log_test("Stego Capacity", capacity_reasonable, f"{max_chars} chars, {total_bits} bits")
                
                # Test 3: Hide and extract message
                test_message = "This is a secret message for testing steganography!"
                
                stego_image, hidden_bits = stego.hide_message(sample_image, test_message, "test_stego.png")
                extracted_message = stego.extract_message(stego_image)
                
                message_matches = test_message == extracted_message
                
                self.log_test("Stego Hide/Extract", message_matches, f"Hidden: {hidden_bits} bits")
                
                # Test 4: Image comparison
                if os.path.exists(stego_image):
                    comparison = stego.compare_images(sample_image, stego_image)
                    low_change = comparison['change_percentage'] < 50  # Changes should be minimal
                    
                    self.log_test("Stego Visual Impact", low_change, f"{comparison['change_percentage']:.2f}% changed")
                
                # Clean up test files
                for file in [sample_image, stego_image]:
                    try:
                        if os.path.exists(file):
                            os.unlink(file)
                    except:
                        pass
            
        except Exception as e:
            self.log_test("Steganography Error", False, str(e))
    
    def test_hybrid_model(self):
        """Test complete hybrid model"""
        print("\n🔐 Testing Hybrid Model...")
        hybrid = HybridCryptoModel()
        
        try:
            # Test 1: System info
            info = hybrid.get_system_info()
            has_all_algorithms = len(info['algorithms']) == 3
            
            self.log_test("Hybrid System Info", has_all_algorithms, f"Algorithms: {info['algorithms']}")
            
            # Test 2: Key generation
            keys = hybrid.generate_keys()
            has_hill_key = 'hill_key' in keys and len(keys['hill_key']) == 2
            has_sdes_key = 'sdes_key' in keys and len(keys['sdes_key']) == 10
            
            self.log_test("Hybrid Key Generation", has_hill_key and has_sdes_key, "Generated all required keys")
            
            # Test 3: Complete hybrid encryption/decryption
            test_text = "Hello World! Testing hybrid encryption system."
            
            # Encrypt
            encryption_result = hybrid.hybrid_encrypt(test_text)
            encryption_success = encryption_result.get('success', False)
            
            self.log_test("Hybrid Encryption", encryption_success, 
                         f"Encrypted to: {encryption_result.get('encrypted_image_path', 'N/A')}")
            
            if encryption_success:
                # Decrypt
                decryption_result = hybrid.hybrid_decrypt(
                    encryption_result['encrypted_image_path'],
                    np.array(encryption_result['keys']['hill_key']),
                    encryption_result['keys']['sdes_key']
                )
                
                decryption_success = decryption_result.get('success', False)
                
                if decryption_success:
                    decrypted_text = decryption_result['decrypted_text'].rstrip('X')
                    original_upper = test_text.upper().replace(" ", "")
                    matches = original_upper == decrypted_text.replace(" ", "")
                    
                    self.log_test("Hybrid Decryption", matches, 
                                 f"'{test_text}' -> '{decrypted_text}'")
                else:
                    self.log_test("Hybrid Decryption", False, decryption_result.get('error', 'Unknown error'))
                
                # Clean up
                try:
                    if os.path.exists(encryption_result['encrypted_image_path']):
                        os.unlink(encryption_result['encrypted_image_path'])
                    cover_image = encryption_result.get('image_info', {}).get('cover_image')
                    if cover_image and os.path.exists(cover_image):
                        os.unlink(cover_image)
                except:
                    pass
            
        except Exception as e:
            self.log_test("Hybrid Model Error", False, str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 HYBRID CRYPTOGRAPHIC SYSTEM - TEST SUITE")
        print("=" * 60)
        
        # Run individual component tests
        self.test_hill_cipher()
        self.test_sdes()
        self.test_steganography()
        self.test_hybrid_model()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"✅ Tests Passed: {self.tests_passed}")
        print(f"❌ Tests Failed: {self.tests_failed}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.tests_failed > 0:
            print(f"\n⚠️  Failed Tests:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"   - {result['test']}: {result['message']}")
        
        # Overall result
        if self.tests_failed == 0:
            print(f"\n🎉 ALL TESTS PASSED! System is ready for deployment.")
            return True
        else:
            print(f"\n⚠️  SOME TESTS FAILED. Please review and fix issues.")
            return False


def main():
    """Main test execution"""
    runner = TestRunner()
    success = runner.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
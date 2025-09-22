import numpy as np
from hill_cipher import HillCipher
from sdes import SDES
from steganography import Steganography
import json
import os


class HybridCryptoModel:
    def __init__(self):
        self.hill_cipher = HillCipher()
        self.sdes = SDES()
        self.steganography = Steganography()
    
    def generate_keys(self):
        """Generate random keys for all algorithms"""
        # Generate Hill Cipher key (2x2 matrix)
        hill_key = self.hill_cipher.generate_random_key()
        
        # Generate SDES key (10-bit binary string)
        sdes_key = self.sdes.generate_random_key()
        
        return {
            'hill_key': hill_key.tolist(),  # Convert numpy array to list for JSON serialization
            'sdes_key': sdes_key
        }
    
    def save_keys(self, keys, filepath="keys.json"):
        """Save keys to a JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(keys, f, indent=2)
            return filepath
        except Exception as e:
            raise Exception(f"Error saving keys: {str(e)}")
    
    def load_keys(self, filepath="keys.json"):
        """Load keys from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                keys = json.load(f)
            
            # Convert hill_key back to numpy array
            keys['hill_key'] = np.array(keys['hill_key'])
            return keys
        except Exception as e:
            raise Exception(f"Error loading keys: {str(e)}")
    
    def hybrid_encrypt(self, plaintext, hill_key=None, sdes_key=None, image_path=None, output_image_path=None):
        """
        Encrypt text using hybrid model: Hill Cipher -> SDES -> Steganography
        
        Args:
            plaintext (str): Text to encrypt
            hill_key (numpy.array): 2x2 matrix for Hill Cipher (optional, will generate if None)
            sdes_key (str): 10-bit binary string for SDES (optional, will generate if None)
            image_path (str): Path to cover image for steganography
            output_image_path (str): Path for output steganographic image
        
        Returns:
            dict: Contains encrypted image path, keys used, and encryption details
        """
        try:
            # Generate keys if not provided
            if hill_key is None or sdes_key is None:
                keys = self.generate_keys()
                hill_key = keys['hill_key'] if hill_key is None else hill_key
                sdes_key = keys['sdes_key'] if sdes_key is None else sdes_key
            
            print(f"🔐 Starting hybrid encryption...")
            print(f"📝 Original text: {plaintext}")
            
            # Step 1: Hill Cipher Encryption
            print(f"\n🔑 Step 1: Hill Cipher Encryption")
            if isinstance(hill_key, list):
                hill_key = np.array(hill_key)
            
            hill_encrypted = self.hill_cipher.encrypt(plaintext, hill_key)
            print(f"   Hill Cipher Result: {hill_encrypted}")
            
            # Step 2: SDES Encryption
            print(f"\n🔒 Step 2: SDES Encryption")
            sdes_encrypted_binary = self.sdes.encrypt_text(hill_encrypted, sdes_key)
            print(f"   SDES Result (binary): {sdes_encrypted_binary[:50]}...")  # Show first 50 chars
            
            # Step 3: Steganography
            print(f"\n🖼️  Step 3: Steganography")
            
            # Create a sample image if none provided
            if image_path is None:
                image_path = self.steganography.create_sample_image(
                    width=1000, height=800, output_path="temp_cover_image.png"
                )
                print(f"   Created cover image: {image_path}")
            
            # Check if image can hold the message
            max_chars, total_bits = self.steganography.get_image_capacity(image_path)
            if len(sdes_encrypted_binary) > total_bits:
                raise ValueError(f"Message too large for image. Required: {len(sdes_encrypted_binary)} bits, Available: {total_bits} bits")
            
            # Hide the SDES encrypted binary in the image
            if output_image_path is None:
                base_name = os.path.splitext(image_path)[0]
                output_image_path = f"{base_name}_hybrid_encrypted.png"
            
            stego_image_path, hidden_bits = self.steganography.hide_message(
                image_path, sdes_encrypted_binary, output_image_path
            )
            print(f"   Steganography complete: {stego_image_path}")
            print(f"   Hidden bits: {hidden_bits}")
            
            # Prepare result
            result = {
                'success': True,
                'encrypted_image_path': stego_image_path,
                'original_text': plaintext,
                'hill_encrypted': hill_encrypted,
                'sdes_encrypted_binary': sdes_encrypted_binary,
                'keys': {
                    'hill_key': hill_key.tolist() if isinstance(hill_key, np.ndarray) else hill_key,
                    'sdes_key': sdes_key
                },
                'image_info': {
                    'cover_image': image_path,
                    'stego_image': stego_image_path,
                    'hidden_bits': hidden_bits,
                    'image_capacity': total_bits
                }
            }
            
            print(f"\n✅ Hybrid encryption completed successfully!")
            return result
            
        except Exception as e:
            print(f"\n❌ Hybrid encryption failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def hybrid_decrypt(self, encrypted_image_path, hill_key, sdes_key):
        """
        Decrypt using hybrid model: Steganography -> SDES -> Hill Cipher
        
        Args:
            encrypted_image_path (str): Path to steganographic image
            hill_key (numpy.array or list): 2x2 matrix for Hill Cipher
            sdes_key (str): 10-bit binary string for SDES
        
        Returns:
            dict: Contains decrypted text and decryption details
        """
        try:
            print(f"🔓 Starting hybrid decryption...")
            
            # Step 1: Extract from Steganography
            print(f"\n🖼️  Step 1: Extracting from Steganography")
            sdes_encrypted_binary = self.steganography.extract_message(encrypted_image_path)
            print(f"   Extracted binary: {sdes_encrypted_binary[:50]}...")  # Show first 50 chars
            
            if not sdes_encrypted_binary:
                raise ValueError("No hidden message found in the image")
            
            # Step 2: SDES Decryption
            print(f"\n🔒 Step 2: SDES Decryption")
            hill_encrypted = self.sdes.decrypt_text(sdes_encrypted_binary, sdes_key)
            print(f"   SDES Decrypted: {hill_encrypted}")
            
            # Step 3: Hill Cipher Decryption
            print(f"\n🔑 Step 3: Hill Cipher Decryption")
            if isinstance(hill_key, list):
                hill_key = np.array(hill_key)
            
            original_text = self.hill_cipher.decrypt(hill_encrypted, hill_key)
            print(f"   Final result: {original_text}")
            
            # Prepare result
            result = {
                'success': True,
                'decrypted_text': original_text,
                'intermediate_steps': {
                    'extracted_binary': sdes_encrypted_binary,
                    'sdes_decrypted': hill_encrypted,
                    'final_text': original_text
                }
            }
            
            print(f"\n✅ Hybrid decryption completed successfully!")
            return result
            
        except Exception as e:
            print(f"\n❌ Hybrid decryption failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_hybrid_system(self, test_text="Hello World! This is a test of the hybrid cryptographic system."):
        """Test the complete hybrid system"""
        print(f"🧪 Testing Hybrid Cryptographic System")
        print(f"=" * 60)
        
        try:
            # Encrypt
            encryption_result = self.hybrid_encrypt(test_text)
            
            if not encryption_result['success']:
                return False
            
            # Save keys for decryption
            keys_file = self.save_keys(encryption_result['keys'])
            print(f"💾 Keys saved to: {keys_file}")
            
            # Decrypt
            decryption_result = self.hybrid_decrypt(
                encryption_result['encrypted_image_path'],
                np.array(encryption_result['keys']['hill_key']),
                encryption_result['keys']['sdes_key']
            )
            
            if not decryption_result['success']:
                return False
            
            # Verify
            original = test_text
            decrypted = decryption_result['decrypted_text'].rstrip('X')  # Remove padding
            
            print(f"\n📊 Test Results:")
            print(f"   Original:  '{original}'")
            print(f"   Decrypted: '{decrypted}'")
            
            if original.upper() == decrypted.upper():
                print(f"✅ TEST PASSED: Text matches!")
                return True
            else:
                print(f"❌ TEST FAILED: Text doesn't match!")
                return False
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            return False
    
    def get_system_info(self):
        """Get information about the hybrid system"""
        return {
            'algorithms': ['Hill Cipher', 'SDES', 'Steganography'],
            'encryption_flow': 'Plaintext → Hill Cipher → SDES → Steganography → Stego Image',
            'decryption_flow': 'Stego Image → Extract → SDES Decrypt → Hill Cipher Decrypt → Plaintext',
            'security_layers': 3,
            'key_requirements': {
                'hill_cipher': '2x2 invertible matrix mod 26',
                'sdes': '10-bit binary string',
                'steganography': 'Cover image (PNG recommended)'
            }
        }


# Example usage and testing
if __name__ == "__main__":
    # Create hybrid system
    hybrid = HybridCryptoModel()
    
    # Display system information
    info = hybrid.get_system_info()
    print("🔐 Hybrid Cryptographic System Information:")
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    print(f"\n" + "=" * 60)
    
    # Run comprehensive test
    success = hybrid.test_hybrid_system()
    
    if success:
        print(f"\n🎉 Hybrid Cryptographic System is working correctly!")
    else:
        print(f"\n⚠️  There are issues with the Hybrid Cryptographic System!")
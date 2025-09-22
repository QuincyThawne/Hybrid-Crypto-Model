import numpy as np
import string
from math import gcd


class HillCipher:
    def __init__(self):
        self.alphabet = string.ascii_uppercase
        self.alphabet_size = 26
        
    def char_to_num(self, char):
        """Convert character to number (A=0, B=1, ..., Z=25)"""
        return ord(char.upper()) - ord('A')
    
    def num_to_char(self, num):
        """Convert number to character (0=A, 1=B, ..., 25=Z)"""
        return chr((num % self.alphabet_size) + ord('A'))
    
    def prepare_text(self, text):
        """Prepare text by removing non-alphabetic characters and converting to uppercase"""
        cleaned = ''.join([char.upper() for char in text if char.isalpha()])
        # Pad with 'X' if length is odd (for 2x2 matrix)
        if len(cleaned) % 2 == 1:
            cleaned += 'X'
        return cleaned
    
    def matrix_mod_inverse(self, matrix, mod):
        """Calculate modular inverse of a 2x2 matrix"""
        det = int(np.round(np.linalg.det(matrix))) % mod
        
        # Check if determinant and modulus are coprime
        if gcd(det, mod) != 1:
            raise ValueError("Matrix is not invertible in the given modulus")
        
        # Find modular inverse of determinant
        det_inv = self.mod_inverse(det, mod)
        
        # Calculate adjugate matrix
        adj_matrix = np.array([[matrix[1, 1], -matrix[0, 1]], 
                              [-matrix[1, 0], matrix[0, 0]]])
        
        # Calculate inverse matrix
        inv_matrix = (det_inv * adj_matrix) % mod
        return inv_matrix.astype(int)
    
    def mod_inverse(self, a, m):
        """Calculate modular inverse using extended Euclidean algorithm"""
        if gcd(a, m) != 1:
            raise ValueError(f"Modular inverse of {a} mod {m} does not exist")
        
        # Extended Euclidean Algorithm
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd_val, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd_val, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def validate_key_matrix(self, key_matrix):
        """Validate that the key matrix is invertible mod 26"""
        try:
            det = int(np.round(np.linalg.det(key_matrix))) % self.alphabet_size
            if gcd(det, self.alphabet_size) != 1:
                return False
            return True
        except:
            return False
    
    def encrypt(self, plaintext, key_matrix):
        """Encrypt plaintext using Hill cipher"""
        if not isinstance(key_matrix, np.ndarray):
            key_matrix = np.array(key_matrix)
        
        if not self.validate_key_matrix(key_matrix):
            raise ValueError("Key matrix is not valid (determinant not coprime with 26)")
        
        cleaned_text = self.prepare_text(plaintext)
        if len(cleaned_text) == 0:
            return ""
        
        ciphertext = ""
        
        # Process text in blocks of 2
        for i in range(0, len(cleaned_text), 2):
            block = cleaned_text[i:i+2]
            if len(block) == 1:
                block += 'X'  # Padding
            
            # Convert to numbers
            vector = np.array([[self.char_to_num(block[0])], 
                              [self.char_to_num(block[1])]])
            
            # Encrypt: C = (K * P) mod 26
            encrypted_vector = np.dot(key_matrix, vector) % self.alphabet_size
            
            # Convert back to characters
            ciphertext += self.num_to_char(encrypted_vector[0, 0])
            ciphertext += self.num_to_char(encrypted_vector[1, 0])
        
        return ciphertext
    
    def decrypt(self, ciphertext, key_matrix):
        """Decrypt ciphertext using Hill cipher"""
        if not isinstance(key_matrix, np.ndarray):
            key_matrix = np.array(key_matrix)
        
        if not self.validate_key_matrix(key_matrix):
            raise ValueError("Key matrix is not valid (determinant not coprime with 26)")
        
        # Calculate inverse key matrix
        inv_key_matrix = self.matrix_mod_inverse(key_matrix, self.alphabet_size)
        
        cleaned_text = self.prepare_text(ciphertext)
        if len(cleaned_text) == 0:
            return ""
        
        plaintext = ""
        
        # Process text in blocks of 2
        for i in range(0, len(cleaned_text), 2):
            block = cleaned_text[i:i+2]
            if len(block) == 1:
                block += 'X'  # Padding
            
            # Convert to numbers
            vector = np.array([[self.char_to_num(block[0])], 
                              [self.char_to_num(block[1])]])
            
            # Decrypt: P = (K^-1 * C) mod 26
            decrypted_vector = np.dot(inv_key_matrix, vector) % self.alphabet_size
            
            # Convert back to characters
            plaintext += self.num_to_char(decrypted_vector[0, 0])
            plaintext += self.num_to_char(decrypted_vector[1, 0])
        
        return plaintext
    
    def generate_random_key(self):
        """Generate a random valid 2x2 key matrix"""
        while True:
            # Generate random 2x2 matrix
            matrix = np.random.randint(0, self.alphabet_size, size=(2, 2))
            if self.validate_key_matrix(matrix):
                return matrix


# Example usage and testing
if __name__ == "__main__":
    hill = HillCipher()
    
    # Test with a known key matrix
    key = np.array([[3, 2], [5, 7]])
    plaintext = "HELLO WORLD"
    
    print(f"Original text: {plaintext}")
    
    try:
        encrypted = hill.encrypt(plaintext, key)
        print(f"Encrypted: {encrypted}")
        
        decrypted = hill.decrypt(encrypted, key)
        print(f"Decrypted: {decrypted}")
        
        # Generate random key
        random_key = hill.generate_random_key()
        print(f"Random key matrix:\n{random_key}")
        
    except ValueError as e:
        print(f"Error: {e}")
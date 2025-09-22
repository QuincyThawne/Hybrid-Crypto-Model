class SDES:
    def __init__(self):
        # Permutation tables
        self.P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.P8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.IP = [2, 6, 3, 1, 4, 8, 5, 7]
        self.IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
        self.EP = [4, 1, 2, 3, 2, 3, 4, 1]
        self.P4 = [2, 4, 3, 1]
        
        # S-boxes
        self.S0 = [
            [1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]
        ]
        
        self.S1 = [
            [0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]
        ]
    
    def permute(self, bits, table):
        """Apply permutation based on table"""
        return [bits[i-1] for i in table]
    
    def left_shift(self, bits, shifts):
        """Perform left circular shift"""
        return bits[shifts:] + bits[:shifts]
    
    def xor(self, bits1, bits2):
        """XOR two bit arrays"""
        return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]
    
    def string_to_bits(self, text):
        """Convert string to bit array (8 bits per character)"""
        bits = []
        for char in text:
            ascii_val = ord(char)
            char_bits = [(ascii_val >> i) & 1 for i in range(7, -1, -1)]
            bits.extend(char_bits)
        return bits
    
    def bits_to_string(self, bits):
        """Convert bit array to string"""
        text = ""
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                ascii_val = 0
                for j, bit in enumerate(byte):
                    ascii_val += bit * (2 ** (7-j))
                text += chr(ascii_val)
        return text
    
    def int_to_bits(self, num, length):
        """Convert integer to bit array of specified length"""
        return [(num >> i) & 1 for i in range(length-1, -1, -1)]
    
    def bits_to_int(self, bits):
        """Convert bit array to integer"""
        result = 0
        for bit in bits:
            result = (result << 1) | bit
        return result
    
    def generate_keys(self, key):
        """Generate K1 and K2 from 10-bit key"""
        if isinstance(key, str):
            if len(key) != 10 or not all(c in '01' for c in key):
                raise ValueError("Key must be a 10-bit binary string")
            key_bits = [int(c) for c in key]
        elif isinstance(key, list):
            if len(key) != 10:
                raise ValueError("Key must be 10 bits long")
            key_bits = key
        else:
            raise ValueError("Key must be a string or list")
        
        # Apply P10 permutation
        p10_key = self.permute(key_bits, self.P10)
        
        # Split into two halves
        left_half = p10_key[:5]
        right_half = p10_key[5:]
        
        # Generate K1
        left_k1 = self.left_shift(left_half, 1)
        right_k1 = self.left_shift(right_half, 1)
        combined_k1 = left_k1 + right_k1
        k1 = self.permute(combined_k1, self.P8)
        
        # Generate K2
        left_k2 = self.left_shift(left_k1, 2)  # Total 3 shifts from original
        right_k2 = self.left_shift(right_k1, 2)  # Total 3 shifts from original
        combined_k2 = left_k2 + right_k2
        k2 = self.permute(combined_k2, self.P8)
        
        return k1, k2
    
    def sbox_substitution(self, bits):
        """Apply S-box substitution"""
        left_4 = bits[:4]
        right_4 = bits[4:]
        
        # S0 substitution
        row0 = (left_4[0] << 1) | left_4[3]
        col0 = (left_4[1] << 1) | left_4[2]
        s0_output = self.S0[row0][col0]
        s0_bits = self.int_to_bits(s0_output, 2)
        
        # S1 substitution
        row1 = (right_4[0] << 1) | right_4[3]
        col1 = (right_4[1] << 1) | right_4[2]
        s1_output = self.S1[row1][col1]
        s1_bits = self.int_to_bits(s1_output, 2)
        
        return s0_bits + s1_bits
    
    def f_function(self, right_half, subkey):
        """Apply the f-function"""
        # Expand right half using EP
        expanded = self.permute(right_half, self.EP)
        
        # XOR with subkey
        xor_result = self.xor(expanded, subkey)
        
        # Apply S-box substitution
        sbox_result = self.sbox_substitution(xor_result)
        
        # Apply P4 permutation
        return self.permute(sbox_result, self.P4)
    
    def encrypt_block(self, plaintext_bits, k1, k2):
        """Encrypt an 8-bit block"""
        # Initial permutation
        ip_result = self.permute(plaintext_bits, self.IP)
        
        # Split into left and right halves
        left = ip_result[:4]
        right = ip_result[4:]
        
        # Round 1
        f_result = self.f_function(right, k1)
        new_left = self.xor(left, f_result)
        # Swap halves
        left, right = right, new_left
        
        # Round 2
        f_result = self.f_function(right, k2)
        new_left = self.xor(left, f_result)
        
        # Combine halves (no swap after final round)
        combined = new_left + right
        
        # Inverse initial permutation
        return self.permute(combined, self.IP_INV)
    
    def decrypt_block(self, ciphertext_bits, k1, k2):
        """Decrypt an 8-bit block (same as encrypt but with keys in reverse order)"""
        return self.encrypt_block(ciphertext_bits, k2, k1)
    
    def encrypt(self, plaintext, key):
        """Encrypt plaintext string"""
        k1, k2 = self.generate_keys(key)
        plaintext_bits = self.string_to_bits(plaintext)
        
        # Pad if necessary
        while len(plaintext_bits) % 8 != 0:
            plaintext_bits.append(0)
        
        ciphertext_bits = []
        
        # Encrypt each 8-bit block
        for i in range(0, len(plaintext_bits), 8):
            block = plaintext_bits[i:i+8]
            encrypted_block = self.encrypt_block(block, k1, k2)
            ciphertext_bits.extend(encrypted_block)
        
        return ciphertext_bits
    
    def decrypt(self, ciphertext_bits, key):
        """Decrypt ciphertext bits"""
        k1, k2 = self.generate_keys(key)
        
        plaintext_bits = []
        
        # Decrypt each 8-bit block
        for i in range(0, len(ciphertext_bits), 8):
            block = ciphertext_bits[i:i+8]
            if len(block) == 8:
                decrypted_block = self.decrypt_block(block, k1, k2)
                plaintext_bits.extend(decrypted_block)
        
        return plaintext_bits
    
    def encrypt_text(self, plaintext, key):
        """Encrypt text and return as binary string"""
        encrypted_bits = self.encrypt(plaintext, key)
        return ''.join(str(bit) for bit in encrypted_bits)
    
    def decrypt_text(self, ciphertext_binary, key):
        """Decrypt binary string and return as text"""
        if isinstance(ciphertext_binary, str):
            ciphertext_bits = [int(c) for c in ciphertext_binary]
        else:
            ciphertext_bits = ciphertext_binary
            
        decrypted_bits = self.decrypt(ciphertext_bits, key)
        return self.bits_to_string(decrypted_bits)
    
    def generate_random_key(self):
        """Generate a random 10-bit key"""
        import random
        return ''.join(str(random.randint(0, 1)) for _ in range(10))


# Example usage and testing
if __name__ == "__main__":
    print("SDES (Simplified DES) Implementation")
    print("Developed by: Murali V, Siddarth Gowtham, Kalaiyarasan")
    print("Course: Cryptography and Network Security (Sem 7)")
    print("-" * 50)
    
    sdes = SDES()
    
    # Test with a known key
    key = "1010000010"
    plaintext = "Hello"
    
    print(f"Original text: {plaintext}")
    print(f"Key: {key}")
    
    try:
        # Encrypt
        encrypted_binary = sdes.encrypt_text(plaintext, key)
        print(f"Encrypted (binary): {encrypted_binary}")
        
        # Decrypt
        decrypted_text = sdes.decrypt_text(encrypted_binary, key)
        print(f"Decrypted: {decrypted_text}")
        
        # Generate random key
        random_key = sdes.generate_random_key()
        print(f"Random key: {random_key}")
        
    except ValueError as e:
        print(f"Error: {e}")
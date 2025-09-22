from PIL import Image
import numpy as np
import os


class Steganography:
    def __init__(self):
        self.delimiter = "###END###"  # Delimiter to mark end of hidden message
        
    def string_to_binary(self, text):
        """Convert string to binary representation"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_string(self, binary):
        """Convert binary representation to string"""
        text = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                text += chr(int(byte, 2))
        return text
    
    def modify_lsb(self, pixel_value, bit):
        """Modify the least significant bit of a pixel value"""
        return (pixel_value & 0xFE) | int(bit)
    
    def get_lsb(self, pixel_value):
        """Get the least significant bit of a pixel value"""
        return pixel_value & 1
    
    def hide_message(self, image_path, message, output_path=None):
        """Hide message in image using LSB steganography"""
        try:
            # Load image with size limit for Streamlit Cloud
            img = Image.open(image_path)
            
            # Limit image size to prevent memory issues
            max_size = (2000, 2000)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img = img.convert('RGB')  # Ensure RGB format
            pixels = np.array(img, dtype=np.uint8)
            
            # Add delimiter to message
            message_with_delimiter = message + self.delimiter
            
            # Convert message to binary
            binary_message = self.string_to_binary(message_with_delimiter)
            
            # Check if image is large enough
            max_capacity = pixels.size  # Total number of pixel values (R, G, B)
            if len(binary_message) > max_capacity:
                raise ValueError(f"Message too large for image. Max capacity: {max_capacity} bits, Message size: {len(binary_message)} bits")
            
            # Flatten the pixel array
            flat_pixels = pixels.flatten()
            
            # Hide message bits in LSBs
            for i, bit in enumerate(binary_message):
                flat_pixels[i] = self.modify_lsb(flat_pixels[i], bit)
            
            # Reshape back to original shape
            modified_pixels = flat_pixels.reshape(pixels.shape)
            
            # Create new image
            stego_img = Image.fromarray(modified_pixels.astype(np.uint8))
            
            # Save image
            if output_path is None:
                base_name = os.path.splitext(image_path)[0]
                output_path = f"{base_name}_stego.png"
            
            stego_img.save(output_path, 'PNG')  # Save as PNG to avoid compression
            
            return output_path, len(binary_message)
            
        except Exception as e:
            raise Exception(f"Error hiding message: {str(e)}")
    
    def extract_message(self, image_path):
        """Extract hidden message from image"""
        try:
            # Load image
            img = Image.open(image_path)
            img = img.convert('RGB')
            pixels = np.array(img)
            
            # Flatten the pixel array
            flat_pixels = pixels.flatten()
            
            # Extract LSBs to form binary message
            binary_message = ''
            delimiter_binary = self.string_to_binary(self.delimiter)
            
            for pixel_value in flat_pixels:
                binary_message += str(self.get_lsb(pixel_value))
                
                # Check if we've found the delimiter
                if binary_message.endswith(delimiter_binary):
                    # Remove delimiter from message
                    binary_message = binary_message[:-len(delimiter_binary)]
                    break
            
            # Convert binary to string
            if binary_message:
                message = self.binary_to_string(binary_message)
                return message
            else:
                return ""
                
        except Exception as e:
            raise Exception(f"Error extracting message: {str(e)}")
    
    def get_image_capacity(self, image_path):
        """Calculate maximum message capacity of an image"""
        try:
            img = Image.open(image_path)
            pixels = np.array(img)
            
            # Total bits available (minus delimiter)
            total_bits = pixels.size
            delimiter_bits = len(self.string_to_binary(self.delimiter))
            available_bits = total_bits - delimiter_bits
            
            # Convert to characters (8 bits per character)
            max_characters = available_bits // 8
            
            return max_characters, total_bits
            
        except Exception as e:
            raise Exception(f"Error calculating capacity: {str(e)}")
    
    def create_sample_image(self, width=800, height=600, output_path="sample_image.png"):
        """Create a sample image for testing"""
        try:
            # Create a colorful gradient image
            img_array = np.zeros((height, width, 3), dtype=np.uint8)
            
            for y in range(height):
                for x in range(width):
                    img_array[y, x] = [
                        int(255 * x / width),          # Red gradient
                        int(255 * y / height),         # Green gradient
                        int(255 * (x + y) / (width + height))  # Blue gradient
                    ]
            
            img = Image.fromarray(img_array)
            img.save(output_path, 'PNG')
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error creating sample image: {str(e)}")
    
    def compare_images(self, original_path, stego_path):
        """Compare original and steganographic images"""
        try:
            img1 = Image.open(original_path).convert('RGB')
            img2 = Image.open(stego_path).convert('RGB')
            
            pixels1 = np.array(img1)
            pixels2 = np.array(img2)
            
            # Calculate differences
            diff = np.abs(pixels1.astype(int) - pixels2.astype(int))
            
            # Calculate statistics
            max_diff = np.max(diff)
            mean_diff = np.mean(diff)
            changed_pixels = np.count_nonzero(diff)
            total_pixels = diff.size
            
            return {
                'max_difference': max_diff,
                'mean_difference': mean_diff,
                'changed_pixels': changed_pixels,
                'total_pixels': total_pixels,
                'change_percentage': (changed_pixels / total_pixels) * 100
            }
            
        except Exception as e:
            raise Exception(f"Error comparing images: {str(e)}")


# Example usage and testing
if __name__ == "__main__":
    print("Image Steganography Implementation")
    print("Developed by: Murali V, Siddarth Gowtham, Kalaiyarasan")
    print("Course: Cryptography and Network Security (Sem 7)")
    print("-" * 50)
    
    stego = Steganography()
    
    # Create a sample image for testing
    sample_image = stego.create_sample_image()
    print(f"Created sample image: {sample_image}")
    
    # Test message
    message = "This is a secret message hidden in the image!"
    print(f"Original message: {message}")
    
    try:
        # Check image capacity
        max_chars, total_bits = stego.get_image_capacity(sample_image)
        print(f"Image capacity: {max_chars} characters ({total_bits} total bits)")
        
        # Hide message
        stego_image, message_bits = stego.hide_message(sample_image, message)
        print(f"Message hidden in: {stego_image}")
        print(f"Message size: {message_bits} bits")
        
        # Extract message
        extracted_message = stego.extract_message(stego_image)
        print(f"Extracted message: {extracted_message}")
        
        # Compare images
        comparison = stego.compare_images(sample_image, stego_image)
        print(f"Image comparison: {comparison}")
        
        # Verify
        if message == extracted_message:
            print("✓ Steganography test passed!")
        else:
            print("✗ Steganography test failed!")
            
    except Exception as e:
        print(f"Error: {e}")
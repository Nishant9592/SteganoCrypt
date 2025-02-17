import cv2
import os
import numpy as np

def int_to_bits(num, bit_length):
    """Convert an integer to a fixed-length list of bits."""
    return [int(b) for b in format(num, f'0{bit_length}b')]

def str_to_bits(s):
    """Convert a string into its 8-bit ASCII representation."""
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def embed_data(image, data_bits):
    """Embed data into the image using LSB steganography."""
    flat = image.flatten()

    if len(data_bits) > len(flat):
        raise ValueError("Data too large to embed in this image!")

    for i in range(len(data_bits)):
        flat[i] = (int(flat[i]) & 254) | data_bits[i]  # Ensure uint8 stays within bounds

    return flat.reshape(image.shape).astype(np.uint8)  # Ensure correct datatype

def encrypt():
    """Encrypts a secret message into an image."""
    
    # Get user input for image paths
    img_path = input("Enter the path of the input image: ").strip()
    output_path = input("Enter the path of the output encrypted image (should be .png): ").strip()
    
    if not os.path.exists(img_path):
        print("Error: Input image not found!")
        return

    image = cv2.imread(img_path)

    if image is None:
        print("Error: Failed to load the image. Please check the file format.")
        return

    secret_message = input("Enter the secret message: ").strip()
    passcode = input("Enter the passcode: ").strip()

    if not secret_message or not passcode:
        print("Error: Secret message and passcode cannot be empty!")
        return

    # Create header:
    # 16 bits: length of passcode, then passcode (8 bits per char)
    # 32 bits: length of secret message, then secret message (8 bits per char)
    header_bits = []
    header_bits.extend(int_to_bits(len(passcode), 16))
    header_bits.extend(str_to_bits(passcode))
    header_bits.extend(int_to_bits(len(secret_message), 32))
    header_bits.extend(str_to_bits(secret_message))

    try:
        encoded_image = embed_data(image, header_bits)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Save as PNG to preserve LSBs
    if not output_path.lower().endswith(".png"):
        print("Warning: Changing output format to PNG to prevent data loss.")
        output_path += ".png"

    cv2.imwrite(output_path, encoded_image)
    print(f"✅ Encryption complete! Saved as '{output_path}'.")

if __name__ == "__main__":
    encrypt()


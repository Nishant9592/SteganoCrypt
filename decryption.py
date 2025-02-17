import cv2
import os

def bits_to_int(bits):
    """Convert a list of bits to an integer."""
    return int("".join(map(str, bits)), 2)

def bits_to_str(bits):
    """Convert a list of bits to a string (8-bit ASCII characters)."""
    return "".join(chr(bits_to_int(bits[i:i+8])) for i in range(0, len(bits), 8))

def extract_bits(image, num_bits):
    """Extract the least significant bits (LSBs) from the image."""
    bits = []
    h, w, c = image.shape
    total_pixels = h * w * c

    if num_bits > total_pixels:
        raise ValueError("Not enough pixels in the image to extract the requested number of bits.")

    flat_image = image.flatten()

    for i in range(num_bits):
        bits.append(flat_image[i] & 1)

    return bits

def decrypt():
    """Decrypts a hidden message from an image using a passcode."""
    img_path = input("Enter the path of the encrypted image: ").strip()

    if not os.path.exists(img_path):
        print("Error: Encrypted image not found!")
        return

    image = cv2.imread(img_path)
    
    if image is None:
        print("Error: Failed to load the image. Please check the file format.")
        return

    try:
        # Extract passcode length (16 bits)
        passcode_length_bits = extract_bits(image, 16)
        passcode_length = bits_to_int(passcode_length_bits)

        # Extract passcode (passcode_length * 8 bits)
        passcode_bits = extract_bits(image, 16 + passcode_length * 8)[16:]
        passcode = bits_to_str(passcode_bits)

        user_passcode = input("Enter the passcode: ").strip()
        if user_passcode != passcode:
            print("Error: Incorrect passcode!")
            return

        # Extract message length (32 bits)
        message_length_bits = extract_bits(image, 16 + passcode_length * 8 + 32)[-32:]
        message_length = bits_to_int(message_length_bits)

        # Extract message (message_length * 8 bits)
        message_bits = extract_bits(image, 16 + passcode_length * 8 + 32 + message_length * 8)[-message_length * 8:]
        secret_message = bits_to_str(message_bits)

        print(f"\n✅ Decryption complete! Secret message: {secret_message}")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    decrypt()


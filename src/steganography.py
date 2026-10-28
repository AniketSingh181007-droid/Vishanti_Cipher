from PIL import Image
import os


HEADER_SIZE = 4


def calculate_capacity(image):
    height, width, channels = image.shape

    return (height * width * channels) // 8


def bytes_to_bits(data):
    bits = []

    for byte in data:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)

    return bits


def bits_to_bytes(bits):
    data = bytearray()

    for i in range(len(bits) // 8):
        byte = 0

        for j in range(8):
            bit = bits[8 * i + j]

            byte = (byte << 1) | bit

        data.append(byte)

    return data

def set_lsb(byte, value):
    return (byte & 254) | value

def get_lsb(byte):
    return byte & 1

def embed_bits(image, bits):
    result = image.copy()
    flat = result.reshape(-1)

    for i in range(len(bits)):
        flat[i] = set_lsb(flat[i], bits[i])

    return result

def extract_bits(image):
    flat = image.reshape(-1)

    bits = []

    for byte in flat:
        bits.append(get_lsb(byte))

    return bits

def encode_payload(image, payload):

    # HEADER_SIZE + len(payload) < calculate_capacity(image)

    header = len(payload).to_bytes(HEADER_SIZE, "big")
    complete_payload = header + payload

    return embed_bits(image, bytes_to_bits(complete_payload))


def decode_payload(image):

    flat = image.reshape(-1)

    size = 0

    for i in range(8 * HEADER_SIZE):
        size = (size << 1) | get_lsb(flat[i])

    bits = []

    for i in range(size * 8):
        bits.append(get_lsb(flat[i + HEADER_SIZE * 8]))

    data = bits_to_bytes(bits)

    return data


def save_stego_image(image, path):

    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)

    output = Image.fromarray(image, mode="RGB")
    output.save(path, format="PNG")
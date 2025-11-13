import base64
import re

def decode_base64(base64_str: str) -> str:
    """Decode a Base64 string into a raw string."""
    decoded_bytes = base64.b64decode(base64_str)
    # Convert to a string using latin1 to preserve byte values
    return decoded_bytes.decode("latin1")  

def extract_minecraft_item(raw_string: str):
    """Extract the Minecraft item and count from a raw decoded string."""
    # Find the Minecraft item
    item_match = re.search(r"(minecraft:\w+)", raw_string)
    # Find the count (integer after 'countt' and some non-greedy chars)
    count_match = re.search(r"countt.*?I(\d+)", raw_string, re.DOTALL)

    item = item_match.group(1) if item_match else None
    count = int(count_match.group(1)) if count_match else None

    return item, count

# Example usage
if __name__ == "__main__":
    base64_str = """rO0ABXNyABpvcmcuYnVra2l0LnV0aWwuaW8uV3JhcHBlcvJQR+zxEm8FAgABTAADbWFwdAAPTGph
dmEvdXRpbC9NYXA7eHBzcgA1Y29tLmdvb2dsZS5jb21tb24uY29sbGVjdC5JbW11dGFibGVNYXAk
U2VyaWFsaXplZEZvcm0AAAAAAAAAAAIAAkwABGtleXN0ABJMamF2YS9sYW5nL09iamVjdDtMAAZ2
YWx1ZXNxAH4ABHhwdXIAE1tMamF2YS5sYW5nLk9iamVjdDuQzlifEHMpbAIAAHhwAAAABnQAAj09
dAALRGF0YVZlcnNpb250AAJpZHQABWNvdW50dAAKY29tcG9uZW50c3QADnNjaGVtYV92ZXJzaW9u
dXEAfgAGAAAABnQAHm9yZy5idWtraXQuaW52ZW50b3J5Lkl0ZW1TdGFja3NyABFqYXZhLmxhbmcu
SW50ZWdlchLioKT3gYc4AgABSQAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAA
eHAAABFYdAAYbWluZWNyYWZ0OmVuY2hhbnRlZF9ib29rc3EAfgAQAAAAAXNyABdqYXZhLnV0aWwu
TGlua2VkSGFzaE1hcDTATlwQbMD7AgABWgALYWNjZXNzT3JkZXJ4cgARamF2YS51dGlsLkhhc2hN
YXAFB9rBwxZg0QMAAkYACmxvYWRGYWN0b3JJAAl0aHJlc2hvbGR4cD9AAAAAAAAMdwgAAAAQAAAA
AXQAHW1pbmVjcmFmdDpzdG9yZWRfZW5jaGFudG1lbnRzdAAaeyJtaW5lY3JhZnQ6dW5icmVha2lu
ZyI6M314AHEAfgAU
"""

    raw_string = decode_base64(base64_str)
    item, count = extract_minecraft_item(raw_string)

    print("Item:", item)
    print("Count:", count)

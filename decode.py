import base64
import re
import json
from typing import Any, List, Tuple, Optional

def decode_base64(base64_str: str) -> str:
    """Decode a Base64 string into a raw string."""
    decoded_bytes = base64.b64decode(base64_str)
    return decoded_bytes.decode("latin1")  

def extract_minecraft_item(raw_string: str) -> Tuple[Optional[str], Optional[int]]:
    """Extract the Minecraft item and count from a raw decoded string."""
    item_match = re.search(r"(minecraft:\w+)", raw_string)
    count_match = re.search(r"countt.*?I(\d+)", raw_string, re.DOTALL)

    item = item_match.group(1) if item_match else None
    count = int(count_match.group(1)) if count_match else None

    return item, count

# -----------------------------
# NEW: recursive processor
# -----------------------------

def process_json_recursively(data: Any, results: List[Tuple[str, int]]):
    """
    Recursively search the JSON structure for fields named 'item' containing base64.
    Append found (item, count) tuples to results.
    """

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "item" and isinstance(value, str):
                try:
                    raw = decode_base64(value)
                    item, count = extract_minecraft_item(raw)
                    if item:
                        results.append((item, count))
                except Exception:
                    pass  # skip invalid base64 entries

            # Continue recursion
            process_json_recursively(value, results)

    elif isinstance(data, list):
        for element in data:
            process_json_recursively(element, results)

    # If primitive → nothing to do


def extract_items_from_json_file(path: str) -> List[Tuple[str, int]]:
    """Load a JSON file and extract all minecraft items recursively."""
    with open(path, "r") as f:
        data = json.load(f)

    results = []
    process_json_recursively(data, results)
    return results


# ----------------------------------------------------------
# Example usage
# ----------------------------------------------------------
if __name__ == "__main__":
    items = extract_items_from_json_file("/home/francesco/wlc_trades.json")

    for item, count in items:
        print(f"Found item: {item}, count: {count}")

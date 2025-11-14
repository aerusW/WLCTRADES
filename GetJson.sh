#!/bin/bash

URL="http://185.206.149.19:8104/trades"
FILE="all_trades.json"
TMP="new_trades.json"

curl -s "$URL" -o "$TMP"

if [ ! -f "$FILE" ]; then
  echo "[]" > "$FILE"
fi

# Extract existing tradeIds as strings
existing_ids=$(jq -r '.[].tradeId | tostring' "$FILE")

# Convert to JSON array string
existing_ids_json=$(jq -c -R . <<< "$existing_ids" | jq -s .)

# Filter new trades: tradeId as string, compare to existing_ids_json
new_trades=$(jq --argjson existing_ids "$existing_ids_json" \
  '[.[] | select((.tradeId | tostring) as $id | $existing_ids | index($id) | not)]' "$TMP")

new_count=$(jq length <<<"$new_trades")

echo "Existing trades: $(jq length "$FILE")"
echo "Fetched trades: $(jq length "$TMP")"
echo "New trades: $new_count"

if [ "$new_count" -gt 0 ]; then
  jq -s '.[0] + .[1]' "$FILE" <(echo "$new_trades") > "${FILE}.tmp" && mv "${FILE}.tmp" "$FILE"
  echo "Appended $new_count new trades."
else
  echo "No new trades found."
fi

rm "$TMP"

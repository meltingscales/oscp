# Test the tokens that gave jq errors - they might be valid!
tokens=("0" "0e0" "0e1" "0e12345" "00" "0.0")

for token in "${tokens[@]}"; do
  echo "=== Testing token: $token ==="
  curl -s "http://monitorsfour.htb/user?token=$token"

  # save to file
  curl -s "http://monitorsfour.htb/user?token=$token" > data/$token.json
  echo -e "\n"
done

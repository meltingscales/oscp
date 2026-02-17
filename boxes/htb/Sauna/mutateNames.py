def generate_username_candidates(first_name, last_name):
    """
    Generate username candidates from first and last name.

    Args:
        first_name (str): First name
        last_name (str): Last name

    Returns:
        list: List of username candidates
    """
    # Convert to lowercase for usernames
    first = first_name.lower()
    last = last_name.lower()

    # Generate different username combinations
    usernames = [
        f"{first[0]}{last}",  # First initial + last name
        f"{first}{last}",     # First name + last name
        f"{last}{first}",     # Last name + first name
    ]

    return usernames

def process_name_list(name_list):
    """
    Process a list of names and generate username candidates for each.

    Args:
        name_list (list): List of full names

    Returns:
        dict: Dictionary with names as keys and list of username candidates as values
    """
    results = {}

    for full_name in name_list:
        # Split the name into first and last name
        name_parts = full_name.strip().split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:])  # Handle cases with more than 2 parts

            # Generate username candidates
            usernames = generate_username_candidates(first_name, last_name)
            results[full_name] = usernames

    return results

def readfilelines(path:str)->list[str]:
    with open(path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# List of names
names = readfilelines('./rawNames.txt')

# Process the names and generate username candidates
username_candidates = process_name_list(names)
generated=set()

# Print the results
for name, usernames in username_candidates.items():
    print(f"Name: {name}")
    print("Username candidates:")
    for username in usernames:
        print(f"  - {username}")
    print()
    generated.update(usernames)

# save generated usernames to a file
with open('generated_usernames.txt', 'w') as file:
    for username in generated:
        file.write(f"{username}\n")

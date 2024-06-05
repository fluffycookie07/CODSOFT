import random
import string

def generate_password(length, use_uppercase=True, use_digits=True, use_special=True):
    if length < 1:
        raise ValueError("Password length must be at least 1")

    character_pools = [string.ascii_lowercase]
    if use_uppercase:
        character_pools.append(string.ascii_uppercase)
    if use_digits:
        character_pools.append(string.digits)
    if use_special:
        character_pools.append(string.punctuation)

    all_characters = ''.join(character_pools)

    password = [
        random.choice(pool) for pool in character_pools
    ]

    password += [random.choice(all_characters) for _ in range(length - len(password))]

    random.shuffle(password)

    return ''.join(password)

def get_user_preferences():
    try:
        length = int(input("Enter the desired length of the password: "))
        if length <= 0:
            raise ValueError("Password length must be a positive integer.")
        
        use_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
        use_digits = input("Include digits? (y/n): ").strip().lower() == 'y'
        use_special = input("Include special characters? (y/n): ").strip().lower() == 'y'

        return length, use_uppercase, use_digits, use_special
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

def main():
    preferences = get_user_preferences()
    if preferences:
        length, use_uppercase, use_digits, use_special = preferences
        try:
            password = generate_password(length, use_uppercase, use_digits, use_special)
            print(f"Generated Password: {password}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

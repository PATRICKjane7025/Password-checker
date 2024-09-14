from flask import Flask
import requests
import random
import string


def password_strength(password):
   
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Password should be at least 8 characters long.")

    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Password should contain at least one lowercase letter.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Password should contain at least one uppercase letter.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Password should contain at least one digit.")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        suggestions.append("Password should contain at least one special character.")

    if score == 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"
        if not suggestions:
            suggestions.append("Consider using a longer and more complex password.")

    return strength, suggestions

def generate_strong_password(length=12):
    
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def test_login(url, username_field, password_field, credentials):
   
    for username, password in credentials:
       
        payload = {
            username_field: username,
            password_field: password
        }
        
        try:
            
            response = requests.post(url, data=payload)
            
            if "login" not in response.url.lower():
                print(f"[SUCCESS] Valid credentials found: {username}/{password}")
            else:
                print(f"[FAIL] Invalid credentials: {username}/{password}")

            
            strength, suggestions = password_strength(password)
            print(f"[PASSWORD STRENGTH] {password}: {strength}")
            if suggestions:
                for suggestion in suggestions:
                    print(f"  - {suggestion}")

           
            if strength == "Weak":
                new_password = generate_strong_password()
                print(f"  - Suggested new password: {new_password}")

        except Exception as e:
            print(f"[ERROR] Failed to test credentials {username}/{password}: {e}")

def main():
    url = input("Enter the login URL: ")
    username_field = input("Enter the username field name: ")
    password_field = input("Enter the password field name: ")
    

    credentials = [
        ('admin', 'password123'),
        ('user', '123456'),
        ('test', 'password'),
        ('test','test'),
        ('test1','password'),
        ('test','A#rvnd'),
        ('test','Ara!456!Dtp'),
        ('test', 'Ar@345Dtp235vys')
    ]
    
    
    test_login(url, username_field, password_field, credentials)

if __name__ == "__main__":
    main()

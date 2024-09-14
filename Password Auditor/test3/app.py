from flask import Flask, request, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

def password_strength(password):
    """
    Evaluates the strength of a password and provides suggestions for improvement.
    """
    score = 0
    suggestions = []

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Password should be at least 12 characters long.")

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

    # Determine strength based on score
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
    """
    Generates a strong password with a given length.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        password = request.form['password']
        strength, suggestions = password_strength(password)
        new_password = None
        if strength == "Weak":
            new_password = generate_strong_password()
        return render_template('result.html', 
                               password=password, 
                               strength=strength, 
                               suggestions=suggestions, 
                               new_password=new_password)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

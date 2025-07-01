from flask import Flask, request, render_template
import pickle
import pandas as pd

# Load the trained model
model_path = 'model_password.pkl'
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Feature extraction function
def calc_switches(password):
    count = 0
    for i in range(len(password) - 1):
        cur = password[i]
        next_char = password[i + 1]
        if ((cur.isdigit() and not next_char.isdigit()) or 
            (cur.islower() and not next_char.islower()) or 
            (cur.isupper() and not next_char.isupper()) or 
            (not cur.isalnum() and next_char.isalnum())):
            count += 1
    return count

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        password = request.form["text"]

        # Extract features from password
        features = pd.DataFrame([[
            len(password), 
            sum(c.isalpha() for c in password), 
            sum(not c.isalnum() for c in password), 
            calc_switches(password)
        ]], columns=['length', 'No_of_chars', 'No_of_special_chars', 'switches'])

        # Make prediction
        prediction = model.predict(features)[0]
        output = {0: 'Weak', 1: 'Moderate', 2: 'Strong'}.get(prediction, 'Unknown')

        return render_template('index.html', prediction_text=f'Prediction: {output}')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

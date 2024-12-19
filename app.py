from flask import Flask,request,jsonify,render_template
import pickle
import pandas as pd
# load the trained model
model_path = 'model_password.pkl'
with open(model_path,'rb') as file:
    model= pickle.load(file)
app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/predict',methods=['POST'])

def predict():
    def calc_switches(a):
        count=0
        for i in range(0,len(a)-1):
            cur=a[i]
            next_char=a[i+1]
            if((cur.isdigit() and not next_char.isdigit()) or( cur.islower() and not next_char.islower()) or (cur.isupper() and not next_char.isupper()) or (not cur.isalnum() and  next_char.isalnum())):
                count=count+1
        return count
    x=request.form["text"]
    c= pd.DataFrame([[len(x),sum(1 for c in x if c.isalpha()),sum(1 for c in x if not c.isalnum()),calc_switches(x)]],columns=['length','No_of_chars','No_of_special_chars','switches'])
    # Making prediction
    prediction =model.predict(c)
    if prediction[0]==0:
        output='Weak'
    elif prediction[0]==1:
        output='Moderate'
    else:
        output='Strong'
    return render_template('index.html',prediction_text='Prediction: {}'.format(output))

if __name__=="__main__":
    app.run(debug=True)
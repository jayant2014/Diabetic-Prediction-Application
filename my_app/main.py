from flask import Flask, render_template, url_for, redirect, request, abort, Blueprint, flash, Markup, session
import joblib
import json, requests
from my_app import *
#app = Flask(__name__, static_url_path='')
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', pub_key=STRIPE_PUBLISHABLE_KEY)

@main.route('/profile')
def profile():
    if session.get('logged_in'):
        return render_template('profile.html', name=session['username'])
    return render_template('index.html')

@main.route('/pay')
def pay():
    if session.get('logged_in'):
        return render_template('pay.html', pub_key=STRIPE_PUBLISHABLE_KEY)        
    return render_template('index.html')

@main.route('/checkout',  methods=['POST'])
def checkout():
    if session.get('logged_in'):
        customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])
    
        charge = stripe.Charge.create(
            customer=customer.id,
            amount=100,
            currency='usd',
            description='Diabetes Prediction'
        )
        return render_template('prediction.html')
    return render_template('index.html')

@main.route('/predict')
def predict():
    if session.get('logged_in'):
        return render_template('prediction.html')
    return render_template('prediction.html')

@main.route('/result', methods = ['GET', 'POST'])
def result():
    if session.get('logged_in'):
        if request.method == 'POST':
            P = int(request.form['PREG'])
            G = float(request.form['GLUCOSE'])
            BP = float(request.form['BP'])
            ST = float(request.form['ST'])
            I = float(request.form['INSULIN'])
            BMI = float(request.form['BMI'])
            DPF = float(request.form['DPF'])
            A = int(request.form['AGE'])

            if float(DPF) >=2:
                return render_template('error.html')
            elif float(DPF) < 0:
                return render_template('error.html') 
            
            model = joblib.load('model/modelDiabetes')    
            prediction = model.predict([[
                P, G, BP, ST, I, BMI, DPF, A
                ]])[0]

            if prediction == 0:
                preds = "You are Healthy, No need to worry, Take proper nutrition."
            else:
                preds = "You are Diabetic, You need to take medication!"
        
            predictResult = {'P': P , 'G': G , 'BP': BP, 'ST': ST, 'I': I, 'BMI': BMI, 'DPF': DPF, 'A': A, 'preds': preds}

            return render_template('result.html', result = predictResult)
        else:
            return render_template('error.html')
        return render_template('result.html')

@main.route('/medication')
def medication():
    return render_template('medication.html')

@main.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

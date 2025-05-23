from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import threading
import requests
import time 
import stripe
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Clé secrète Stripe (depuis .env)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def keep_alive():
    while True:
        try:
            requests.get("https://aeho-rl.onrender.com")
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion : {e}")
        time.sleep(30) 
        
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/don")
def don():
    return render_template("payment.html")
#                                                                     <-------------------- DONT WORK-------------------->
@app.route("/sepa") # dont work
def sepa():
    return render_template("sepa.html")

@app.route("/create-customer", methods=["POST"])
def create_customer():
    try:
        customer = stripe.Customer.create(
            email="test@example.com",
        )
        return jsonify({"customer": customer.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route("/create-setup-intent", methods=["POST"])
def create_setup_intent():
    data = request.json
    customer_id = data["customer"] # type: ignore

    try:
        intent = stripe.SetupIntent.create(
            payment_method_types=["sepa_debit"],
            customer=customer_id,
        )
        return jsonify({"clientSecret": intent.client_secret})
    except Exception as e:
        return jsonify(error=str(e)), 403
#                                                                     <--------------------WORK-------------------->
if __name__ == "__main__":
   threading.Thread(target=keep_alive).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

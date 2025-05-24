from flask import Flask, request, jsonify, render_template
from flask import send_from_directory
from dotenv import load_dotenv
import stripe
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

app = Flask(__name__)

# Clé secrète Stripe (depuis .env)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('.', 'robots.txt')

@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('.', 'sitemap.xml')
    
app.route('/google0c627cc1f164193b.html')
def google_verification():
    return send_from_directory('public', 'google0c627cc1f164193b.html')

    
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
    app.run(port=5000, debug=True)

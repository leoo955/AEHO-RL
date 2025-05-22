import os
import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure ta clé secrète Stripe
stripe.api_key = "sk_test_..."  # remplace par ta vraie clé secrète

# Ton endpoint secret (trouvé dans le Dashboard > Webhooks)
endpoint_secret = "whsec_..."

@app.route("/webhook", methods=["POST"])
def stripe_webhook(): # type: ignore
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError as e: # type: ignore
        return "Signature non valide", 400
    except Exception as e:
        return str(e), 400

    # Gère les événements que tu veux suivre
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"Paiement réussi pour l'utilisateur : {session.get('customer_email')}")
        # Ici tu peux envoyer un mail, enregistrer en DB, etc.

    return jsonify(success=True)

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except stripe.error.SignatureVerificationError: # type: ignore
        return "Signature non valide", 400

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        print(f"✅ Paiement par virement reçu pour {payment_intent['amount']} centimes")

    elif event["type"] == "payment_intent.processing":
        print("⌛ Virement en cours de traitement...")

    elif event["type"] == "payment_intent.payment_failed":
        print("❌ Le virement a échoué")

    return jsonify(success=True)

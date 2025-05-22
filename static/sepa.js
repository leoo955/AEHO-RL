    const stripe = Stripe("pk_test_51RRW1PEEvRRGwijxSRwK08gJDz6jQ7wfg4Wguz3YvrXaxXYUKLuCRWJCFqUHkorvRBS6Pv3icALID3Vzp83UDrjJ007WbjMbe0");

document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("sepa-form");
  const ibanElementDiv = document.getElementById("iban-element");
  const mandateText = document.getElementById("mandate-text");

  const { customer } = await fetch("/create-customer", { method: "POST" }).then(res => res.json());
  const { clientSecret } = await fetch("/create-setup-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ customer }),
  }).then(res => res.json());

  const elements = stripe.elements();
  const iban = elements.create("iban", {
    supportedCountries: ["SEPA"],
    style: {
      base: {
        fontSize: "16px",
        color: "#32325d",
      }
    }
  });
  iban.mount("#iban-element");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    const { setupIntent, error } = await stripe.confirmSepaDebitSetup(clientSecret, {
      payment_method: {
        sepa_debit: iban,
        billing_details: {
          name: name,
          email: email,
        },
      },
    });

    const response = document.getElementById("response");

    if (error) {
      response.textContent = "Erreur : " + error.message;
      response.style.color = "red";
    } else {
      response.textContent = "Mandat SEPA créé avec succès !";
      response.style.color = "green";
      console.log("SetupIntent ID :", setupIntent.id);
    }
  });
});

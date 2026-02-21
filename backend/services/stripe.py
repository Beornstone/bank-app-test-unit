import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Initialise Stripe with test mode secret key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Radar risk thresholds
RISK_SCORE_ELEVATED = 40   # warn Alma user above this
RISK_SCORE_HIGHEST = 75    # block and alert above this


def create_stripe_customer(name: str, email: str) -> str:
    """
    Creates a new Stripe customer and returns their customer ID.
    Always runs in test mode (determined by the STRIPE_SECRET_KEY starting with sk_test_).
    """
    customer = stripe.Customer.create(
        name=name,
        email=email,
        metadata={"source": "alma_app"}
    )
    return customer.id


def get_stripe_customer(customer_id: str) -> dict:
    """
    Fetches a Stripe customer by ID.
    Returns a dict with id, name, email.
    """
    customer = stripe.Customer.retrieve(customer_id)
    return {
        "id": customer.id,
        "name": customer.name,
        "email": customer.email,
    }


def get_recent_transactions(customer_id: str, limit: int = 10) -> list:
    """
    Fetches the most recent charges for a Stripe customer.
    Includes Radar fraud score for each transaction.
    """
    charges = stripe.Charge.list(customer=customer_id, limit=limit)
    return [
        {
            "id": charge.id,
            "amount": charge.amount / 100,
            "currency": charge.currency.upper(),
            "description": charge.description or "Payment",
            "status": charge.status,
            "date": charge.created,
            "risk_level": charge.outcome.risk_level if charge.outcome else "unknown",
            "risk_score": charge.outcome.risk_score if charge.outcome else None,
        }
        for charge in charges.data
    ]


def get_radar_risk(charge_id: str) -> dict:
    """
    Retrieves the Stripe Radar fraud score for a specific charge.
    Returns risk_level, risk_score, and an alma_message to read to the user.

    Risk levels from Stripe Radar:
    - "normal"   → low risk, safe to proceed
    - "elevated" → moderate risk, warn the user
    - "highest"  → high risk, block and alert
    """
    charge = stripe.Charge.retrieve(charge_id)
    outcome = charge.outcome

    risk_level = outcome.risk_level if outcome else "unknown"
    risk_score = outcome.risk_score if outcome else None

    # Generate a plain-English message for Alma to read to the user
    if risk_level == "highest" or (risk_score and risk_score >= RISK_SCORE_HIGHEST):
        alma_message = (
            "I'm very concerned about this payment. "
            "Our fraud detection has flagged it as high risk. "
            "I strongly recommend you do not proceed. "
            "If someone has asked you to make this payment, please speak to a trusted person first."
        )
        should_block = True

    elif risk_level == "elevated" or (risk_score and risk_score >= RISK_SCORE_ELEVATED):
        alma_message = (
            "This payment looks a little unusual to me. "
            "Are you sure you want to send this? "
            "Please take a moment to double-check before confirming."
        )
        should_block = False

    else:
        alma_message = "This payment looks fine. Would you like to go ahead?"
        should_block = False

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "should_block": should_block,
        "alma_message": alma_message,
    }


def create_payment_intent(customer_id: str, amount_euros: float, description: str) -> dict:
    """
    Creates a Stripe PaymentIntent for a given customer.
    Amount is in euros (converted to cents internally).
    After creation, reads Radar fraud score from the latest charge.
    Returns payment details plus fraud assessment.
    """
    intent = stripe.PaymentIntent.create(
        amount=int(amount_euros * 100),
        currency="eur",
        customer=customer_id,
        description=description,
        metadata={"source": "alma_app"}
    )

    # Read Radar score if a charge has already been created
    radar = None
    if intent.latest_charge:
        try:
            radar = get_radar_risk(intent.latest_charge)
        except Exception:
            pass  # Radar score not available yet — checked in webhook instead

    return {
        "id": intent.id,
        "client_secret": intent.client_secret,
        "amount": amount_euros,
        "status": intent.status,
        "radar": radar,  # None if charge not yet created
    }
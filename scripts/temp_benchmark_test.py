
import requests
def call_stripe_api(endpoint, data):
    headers = {'Authorization': 'Bearer sk_test_dummy'}
    try:
        response = requests.post(f"https://api.stripe.com/{endpoint}", headers=headers, json=data)
        return response.status_code, response.json()
    except Exception as e:
        return 0, str(e)

# Test case simulation: Creating a payment intent
status, result = call_stripe_api("v1/payment_intents", {"amount": 2000, "currency": "usd"})
print(f"Simulated API Call Status: {status}")

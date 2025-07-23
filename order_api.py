import requests

def place_order(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://admin.iclothgenie.com/api/Order/InsertOrder"
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True, "✅ Order placed successfully!"
        else:
            return False, f"❌ Order failed: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"⚠️ Exception occurred: {e}"
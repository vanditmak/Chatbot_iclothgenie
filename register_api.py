import requests

def register_user(data):
    url = "https://admin.iclothgenie.com/api/Customer/InsertCustomer"
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return True, "✅ Registration successful!"
        else:
            return False, f"❌ Registration failed: {response.text}"
    except Exception as e:
        return False, f"⚠️ Exception occurred: {e}"
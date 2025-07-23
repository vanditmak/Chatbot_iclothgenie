import requests

def login_user(email, password):
    url = "https://admin.iclothgenie.com/api/Authentication/Login"
    try:
        response = requests.post(url, json={"username": email, "password": password})
        if response.status_code == 200:
            data = response.json()
            return True, "✅ Login successful!", {
                "token": data["data1"],
                "user": data["data2"]
            }
        else:
            return False, f"❌ Login failed: {response.text}", {}
    except Exception as e:
        return False, f"⚠️ Exception occurred: {e}", {}
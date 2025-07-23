import requests

def update_order(payload, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://admin.iclothgenie.com/api/Order/UpdateOrder"
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return True, "✅ Order updated successfully!"
        else:
            return False, f"❌ Update failed: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"⚠️ Exception occurred: {e}"
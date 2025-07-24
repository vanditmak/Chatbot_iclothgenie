import gradio as gr
from register_api import register_user
from login_api import login_user
from order_api import place_order
from update_order_api import update_order
from utils import validate_user_input

chat_history = []
user_data = {}
flow = None
current_step = 0

steps = {
    "register": ["first_name", "last_name", "email", "mobile", "address1", "password", "confirm_password"],
    "login": ["email", "password"],
    "order": ["pickupDate", "pickupTime", "dropOffDate", "dropOffTime", "Services", "SubServices", "collectionOption", "deliveryOption"],
    "update": ["orderId", "pickupDate", "pickupTime", "dropOffDate", "dropOffTime", "collectionOption", "deliveryOption"]
}

prompts = {
    "first_name": "Please enter your first name:",
    "last_name": "Enter your last name:",
    "email": "Enter your email address:",
    "mobile": "Enter your mobile number:",
    "address1": "Enter your address (required for delivery):",
    "password": "Enter your password:",
    "confirm_password": "Confirm your password:",
    "pickupDate": "Enter pickup date (YYYY-MM-DD):",
    "pickupTime": "Enter pickup time (e.g., 09:00 AM - 11:00 AM):",
    "dropOffDate": "Enter drop-off date (YYYY-MM-DD):",
    "dropOffTime": "Enter drop-off time (e.g., 01:00 PM - 03:00 PM):",
    "Services": "Enter service ID (e.g., 20):",
    "SubServices": "Enter sub-service ID (e.g., 3):",
    "collectionOption": "Enter collection option (e.g., 'Driver collects from reception/porter'):",
    "deliveryOption": "Enter delivery option (e.g., 'Driver delivers to you'):",
    "orderId": "Enter the order ID to update:"
}

logged_in_user = {}

def chatbot(user_message, history):
    global current_step, user_data, flow, logged_in_user

    if flow is None:
        if "register" in user_message.lower():
            flow = "register"
        elif "login" in user_message.lower():
            flow = "login"
        elif "order" in user_message.lower():
            if not logged_in_user:
                return history + [{"role": "user", "content": user_message},
                                  {"role": "assistant", "content": "❌ Please login first before placing an order."}]
            flow = "order"
        elif "update" in user_message.lower():
            if not logged_in_user:
                return history + [{"role": "user", "content": user_message},
                                  {"role": "assistant", "content": "❌ Please login first before updating an order."}]
            flow = "update"
        else:
            return history + [{"role": "user", "content": user_message},
                              {"role": "assistant", "content": "Do you want to Register, Login, Place Order, or Update Order?"}]
        current_step = 0
        user_data.clear()
        return history + [{"role": "user", "content": user_message},
                          {"role": "assistant", "content": prompts[steps[flow][current_step]]}]

    current_key = steps[flow][current_step]
    is_valid, msg = validate_user_input(current_key, user_message, user_data)
    if not is_valid:
        return history + [{"role": "user", "content": user_message},
                          {"role": "assistant", "content": msg}]
    user_data[current_key] = user_message
    current_step += 1

    if current_step == len(steps[flow]):
        if flow == "register":
            success, msg = register_user(user_data)
        elif flow == "login":
            success, msg, result = login_user(user_data["email"], user_data["password"])
            if success:
                logged_in_user["data"] = result["user"]
                logged_in_user["token"] = result["token"]
        elif flow == "order":
            order_payload = {
                "customerId": logged_in_user["data"]["id"],
                "pickupDate": user_data["pickupDate"],
                "pickupTime": user_data["pickupTime"],
                "dropOffDate": user_data["dropOffDate"],
                "dropOffTime": user_data["dropOffTime"],
                "Services": user_data["Services"],
                "SubServices": user_data["SubServices"],
                "collectionOption": user_data["collectionOption"],
                "deliveryOption": user_data["deliveryOption"],
                "offerCode": "",
                "orderAddress": {
                    "firstname": logged_in_user["data"]["firstname"],
                    "lastname": logged_in_user["data"]["lastname"],
                    "email": logged_in_user["data"]["email"],
                    "contactNo": logged_in_user["data"]["mobileNo"],
                    "addressLine1": logged_in_user["data"]["address1"],
                    "addressLine2": "",
                    "postCode": logged_in_user["data"]["postCode"]
                }
            }
            success, msg = place_order(order_payload, logged_in_user["token"])
        elif flow == "update":
            update_payload = {
                "id": int(user_data["orderId"]),
                "customerId": logged_in_user["data"]["id"],
                "pickupDate": user_data["pickupDate"],
                "pickupTime": user_data["pickupTime"],
                "dropOffDate": user_data["dropOffDate"],
                "dropOffTime": user_data["dropOffTime"],
                "collectionOption": user_data["collectionOption"],
                "deliveryOption": user_data["deliveryOption"]
            }
            success, msg = update_order(update_payload, logged_in_user["token"])

        user_data.clear()
        flow = None
        current_step = 0
        return history + [{"role": "user", "content": user_message},
                          {"role": "assistant", "content": msg}]

    next_prompt = prompts[steps[flow][current_step]]
    return history + [{"role": "user", "content": user_message},
                      {"role": "assistant", "content": next_prompt}]

demo = gr.ChatInterface(
    fn=chatbot,
    chatbot=gr.Chatbot(type="messages"),
    textbox=gr.Textbox(placeholder="Type here..."),
    title="iClothGenie Chatbot",
    description="Type 'Register', 'Login', 'Place Order', or 'Update Order' to begin.",
    theme=gr.themes.Soft(primary_hue="cyan", secondary_hue="blue"),
    type="messages"
)

demo.launch(server_name="0.0.0.0", server_port=10000, share=False)

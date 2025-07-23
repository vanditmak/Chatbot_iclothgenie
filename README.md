# iClothGenie Chatbot

This is a Python-based chatbot project built with **Gradio** that integrates with the iClothGenie backend API. It supports the following user operations:

- ✅ Register new users
- 🔐 Login existing users
- 📦 Place orders
- 🔄 Update existing orders

---

## 🚀 Features

- Conversational flow using Gradio's `ChatInterface`
- API integration for user registration, login, and order management
- Input validation (e.g., email format, matching passwords)
- User authentication using Bearer token after login

---

## 🧾 Project Structure

```
.
├── chatbot_main.py           # Main chatbot logic using Gradio
├── register_api.py           # Handles user registration API
├── login_api.py              # Handles user login API
├── order_api.py              # Handles order placement API
├── update_order_api.py       # Handles order update API
├── utils.py                  # Utility functions (validation)
└── README.md                 # Project instructions (this file)
```

---

## 🛠️ Setup Instructions

### 1. Install Dependencies

Make sure Python 3.8+ is installed.

```bash
pip install gradio requests
```

### 2. Run the Chatbot

```bash
python chatbot_main.py
```

The chatbot UI will launch at: `http://localhost:7860`

---

## 🌐 API Endpoints Used

- **Register**: `POST /api/Customer/InsertCustomer`
- **Login**: `POST /api/Authentication/Login`
- **Place Order**: `POST /api/Order/InsertOrder`
- **Update Order**: `POST /api/Order/UpdateOrder`

These endpoints require a valid connection to: `https://admin.iclothgenie.com`

---

## 📎 Embedding in a Website

If hosted online (e.g., Gradio Spaces or Render), embed the chatbot in a website using:

```html
<iframe src="https://your-chatbot-url.com" style="position: fixed; bottom: 20px; right: 20px; width: 350px; height: 500px; border: none;"></iframe>
```

---

## 📩 Contact

For questions or help, reach out to: [vsmakwana2004@gmail.com](mailto:vsmakwana2004@gmail.com)

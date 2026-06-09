# 💱 Currency Converter

A real-time currency converter web application built with **Python (Flask)** and vanilla **HTML/CSS/JavaScript**. Converts between 50+ world currencies using live exchange rates from [ExchangeRate-API](https://www.exchangerate-api.com/).

🔗 **Live Demo:** [Add your deployed link here]

![Screenshot](screenshot.png)
"C:\Users\DELL\Pictures\Screenshots\Screenshot 2026-06-09 154245.png"

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📡 **Real-time rates** | Live exchange rates updated daily |
| 🔍 **Searchable dropdowns** | Type to search currencies by code or name |
| 🔄 **Swap button** | Instantly swap base and target currencies |
| 💾 **Remembers your choices** | Last used currencies and amount saved in browser |
| ⏱️ **Last updated time** | Shows when rates were last refreshed |
| 📱 **Fully responsive** | Works on desktop, tablet, and mobile |
| ⚡ **Loading states** | Visual feedback while fetching rates |
| 🛡️ **Error handling** | Friendly messages for all error cases |

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **API:** [ExchangeRate-API](https://www.exchangerate-api.com/) (free tier)
- **Deployment:** Render / Railway / PythonAnywhere

---

## 🚀 Run Locally

### Prerequisites
- Python 3.8 or higher installed
- A free API key from [ExchangeRate-API](https://www.exchangerate-api.com/) (takes 30 seconds)

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/currency-converter.git
cd currency-converter
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Add your API key

1. Go to [exchangerate-api.com](https://www.exchangerate-api.com/) and sign up (free)
2. Copy your API key
3. Open `app.py` and replace:
   ```python
   API_KEY = "YOUR_API_KEY"
   ```
   with your actual key:
   ```python
   API_KEY = "abc123your_actual_key"
   ```

> **Tip:** For production, use an environment variable instead:
> ```python
> import os
> API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY", "YOUR_API_KEY")
> ```

### Step 5 — Run the app

```bash
python app.py
```

Open **http://localhost:5000** in your browser. 🎉

---

## 🌐 Deploy for Free (Get a Live Link)

### Option 1 — Render (Recommended)

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign in with GitHub
3. Click **New → Web Service**
4. Connect your repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Add an environment variable:
   - Key: `EXCHANGE_RATE_API_KEY`
   - Value: your API key
7. Click **Deploy** — you'll get a free `.onrender.com` URL!

> **Note:** To use environment variables, update `app.py`:
> ```python
> import os
> API_KEY = os.environ.get("EXCHANGE_RATE_API_KEY", "YOUR_API_KEY")
> ```

### Option 2 — Railway

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign in
3. Click **New Project → Deploy from GitHub Repo**
4. Select your repository
5. Add the environment variable `EXCHANGE_RATE_API_KEY`
6. Railway auto-detects Flask — it will deploy automatically
7. Go to **Settings → Domains** to get your public URL

### Option 3 — PythonAnywhere

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) (free tier)
2. Go to **Web** tab → **Add a new web app**
3. Choose **Flask** and Python 3.10+
4. Upload your project files or clone from GitHub
5. Set the **Source code** path and **WSGI file** path
6. In the WSGI file, import your app:
   ```python
   from app import app as application
   ```
7. Your app will be live at `yourusername.pythonanywhere.com`

---

## 📂 Project Structure

```
currency-converter/
├── app.py                  # Flask backend (routes, API logic)
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
├── README.md               # This file
├── templates/
│   └── index.html          # Main HTML page
└── static/
    ├── style.css           # Stylesheet
    └── script.js           # Frontend logic
```

---

## 📝 API Key Setup

1. Visit [exchangerate-api.com](https://www.exchangerate-api.com/)
2. Click **"Get Free Key"**
3. Sign up with your email (no credit card required)
4. Confirm your email
5. Copy the API key from your dashboard
6. Paste it in `app.py` where it says `YOUR_API_KEY`

The free plan includes:
- ✅ 1,500 requests/month
- ✅ Daily rate updates
- ✅ 160+ currencies
- ✅ No credit card required

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

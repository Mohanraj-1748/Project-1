"""
Currency Converter Web Application
====================================
A real-time currency converter built with Flask.
Uses ExchangeRate-API for live exchange rates.

Author: Your Name
Version: 1.0.0
"""

import requests as http_requests
from flask import Flask, render_template, request, jsonify
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────
app = Flask(__name__)

# Replace with your free API key from https://www.exchangerate-api.com/
API_KEY = "d814c9bd4cfefb6b1eb474da"
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

# ─── Supported Currencies (code → full name) ────────────────
CURRENCIES = {
    "AED": "United Arab Emirates Dirham",
    "ARS": "Argentine Peso",
    "AUD": "Australian Dollar",
    "BDT": "Bangladeshi Taka",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CLP": "Chilean Peso",
    "CNY": "Chinese Yuan",
    "COP": "Colombian Peso",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EGP": "Egyptian Pound",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "GEL": "Georgian Lari",
    "GHS": "Ghanaian Cedi",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Shekel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "JPY": "Japanese Yen",
    "KES": "Kenyan Shilling",
    "KRW": "South Korean Won",
    "KWD": "Kuwaiti Dinar",
    "LKR": "Sri Lankan Rupee",
    "MAD": "Moroccan Dirham",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NGN": "Nigerian Naira",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PEN": "Peruvian Sol",
    "PHP": "Philippine Peso",
    "PKR": "Pakistani Rupee",
    "PLN": "Polish Zloty",
    "QAR": "Qatari Riyal",
    "RON": "Romanian Leu",
    "RUB": "Russian Ruble",
    "SAR": "Saudi Riyal",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "TWD": "New Taiwan Dollar",
    "UAH": "Ukrainian Hryvnia",
    "USD": "United States Dollar",
    "UYU": "Uruguayan Peso",
    "VND": "Vietnamese Dong",
    "ZAR": "South African Rand",
}


# ═══════════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Serve the main converter page."""
    return render_template("index.html")


@app.route("/api/currencies")
def get_currencies():
    """
    Return the full list of supported currencies.
    Response: { "success": true, "currencies": { "USD": "United States Dollar", ... } }
    """
    return jsonify({"success": True, "currencies": CURRENCIES})


@app.route("/api/convert")
def convert():
    """
    Convert an amount from one currency to another using live rates.

    Query params:
        base   — source currency code (e.g. "USD")
        target — target currency code (e.g. "INR")
        amount — numeric amount to convert

    Returns JSON with the conversion result or an error message.
    """
    # ── 1. Extract and validate parameters ────────────────────
    base = request.args.get("base", "").upper().strip()
    target = request.args.get("target", "").upper().strip()
    amount_str = request.args.get("amount", "").strip()

    # Check all parameters are present
    if not base or not target or not amount_str:
        return jsonify({
            "success": False,
            "error": "Missing required parameters. Please provide base, target, and amount."
        }), 400

    # Validate amount is a positive number
    try:
        amount = float(amount_str)
        if amount <= 0:
            return jsonify({
                "success": False,
                "error": "Amount must be a positive number."
            }), 400
    except ValueError:
        return jsonify({
            "success": False,
            "error": f"Invalid amount: '{amount_str}'. Please enter a valid number."
        }), 400

    # Validate currency codes
    if base not in CURRENCIES:
        return jsonify({
            "success": False,
            "error": f"Invalid base currency: '{base}'. Please select a valid currency."
        }), 400

    if target not in CURRENCIES:
        return jsonify({
            "success": False,
            "error": f"Invalid target currency: '{target}'. Please select a valid currency."
        }), 400

    # ── 2. Fetch live exchange rates from the API ─────────────
    try:
        response = http_requests.get(
            f"{BASE_URL}/latest/{base}",
            timeout=10
        )
        data = response.json()

        # Handle API-level errors
        if data.get("result") == "error":
            error_type = data.get("error-type", "unknown")
            error_messages = {
                "unsupported-code": "The currency code is not supported by the API.",
                "malformed-request": "The API request was malformed. Please try again.",
                "invalid-key": "Invalid API key. Please check your API key configuration.",
                "inactive-account": "The API account is inactive. Please check your account.",
                "quota-reached": "API rate limit reached. Please try again later.",
            }
            return jsonify({
                "success": False,
                "error": error_messages.get(error_type, f"API error: {error_type}")
            }), 502

        # Extract conversion rate
        rates = data.get("conversion_rates", {})
        if target not in rates:
            return jsonify({
                "success": False,
                "error": f"Exchange rate for {target} not available."
            }), 404

        rate = rates[target]
        converted_amount = round(amount * rate, 2)

        # Parse the last-updated time from the API
        last_updated = data.get("time_last_update_utc", "")
        if last_updated:
            try:
                # Parse the API's date string and reformat it
                dt = datetime.strptime(last_updated.strip(), "%a, %d %b %Y %H:%M:%S %z")
                last_updated = dt.strftime("%b %d, %Y at %I:%M %p UTC")
            except (ValueError, TypeError):
                last_updated = last_updated  # Keep original if parsing fails

        # ── 3. Return the result ──────────────────────────────
        return jsonify({
            "success": True,
            "result": {
                "base": base,
                "base_name": CURRENCIES.get(base, base),
                "target": target,
                "target_name": CURRENCIES.get(target, target),
                "amount": amount,
                "converted_amount": converted_amount,
                "rate": rate,
                "last_updated": last_updated
            }
        })

    except http_requests.exceptions.ConnectionError:
        return jsonify({
            "success": False,
            "error": "Unable to connect to the exchange rate service. Please check your internet connection."
        }), 503

    except http_requests.exceptions.Timeout:
        return jsonify({
            "success": False,
            "error": "The request timed out. Please try again."
        }), 504

    except http_requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"An error occurred while fetching rates: {str(e)}"
        }), 502

    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }), 500


# ═══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n  Currency Converter is running!")
    print("  -> Open http://localhost:5000 in your browser\n")
    app.run(host="0.0.0.0", port=5000, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = "data.json"

# Load or initialize data store
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data_store = json.load(f)
    # Reset salary and expenses by clearing all transactions and resetting month and remaining salary
    data_store["remaining_salary"] = 0
    data_store["transactions"] = []   # clear previous income & expenses
    data_store["current_month"] = None
else:
    data_store = {
        "remaining_salary": 0,
        "transactions": [],
        "current_month": None
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data_store, f)

# Load ML model & vectorizer for categorizing expenses
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

from datetime import datetime

@app.route('/add_income', methods=['POST'])
def add_income():
    global data_store
    data = request.get_json()
    amount = data.get("amount")
    month = datetime.now().strftime("%Y-%m")

    # If new month, add salary to remaining salary from last month
    if data_store.get("current_month") != month:
        data_store["current_month"] = month
        data_store["remaining_salary"] += amount
    else:
        # If income added mid-month, just add it to remaining_salary
        data_store["remaining_salary"] += amount

    # Add income transaction
    data_store["transactions"].append({
        "type": "Income",
        "amount": amount,
        "description": "Monthly Salary",
        "month": month,
        "category": "Salary"
    })

    # Save data
    with open(DATA_FILE, "w") as f:
        json.dump(data_store, f)

    return jsonify({"remaining_salary": data_store["remaining_salary"]})

@app.route('/add_expense', methods=['POST'])
def add_expense():
    global data_store
    data = request.get_json()
    desc = data.get("description")
    amount = data.get("amount")
    month = datetime.now().strftime("%Y-%m")

    # Predict category from description using ML
    X = vectorizer.transform([desc])
    category = model.predict(X)[0]

    # Deduct expense from remaining salary
    data_store["remaining_salary"] -= amount

    # Add expense transaction
    data_store["transactions"].append({
        "type": "Expense",
        "amount": amount,
        "description": desc,
        "month": month,
        "category": category
    })

    # Save data
    with open(DATA_FILE, "w") as f:
        json.dump(data_store, f)

    return jsonify({
        "remaining_salary": data_store["remaining_salary"],
        "category": category
    })

@app.route('/summary', methods=['GET'])
def summary():
    global data_store
    month = datetime.now().strftime("%Y-%m")

    income = sum(t["amount"] for t in data_store["transactions"] if t["type"] == "Income" and t["month"] == month)
    expenses = sum(t["amount"] for t in data_store["transactions"] if t["type"] == "Expense" and t["month"] == month)
    remaining = data_store["remaining_salary"]

    alert = ""
    if income > 0 and expenses > 0.7 * income:
        alert = "⚠️ Warning: You've spent over 70% of your income this month!"

    return jsonify({
        "income": income,
        "expenses": expenses,
        "remaining_salary": remaining,
        "alert": alert
    })

if __name__ == "__main__":
    app.run(debug=True)

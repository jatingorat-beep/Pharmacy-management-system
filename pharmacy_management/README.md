# ⚕️ PharmaCare - Pharmacy Management System

A web-based Pharmacy Management System built with Python, Flask, SQLite, and responsive HTML/CSS.

## Project Structure

```text
pharmacy_management/
├── .vscode/
│   └── launch.json        # Chrome debug configuration (port 8080)
├── static/
│   └── style.css          # Responsive styling for dashboard, cards, tables, and forms
├── templates/
│   ├── index.html         # Main dashboard with KPI cards and medicine inventory
│   ├── add_medicine.html  # Form to add new medicines
│   ├── sales.html         # Sales & billing interface with automatic price and stock tracking
│   └── customers.html     # Customer registration and list
├── database.py            # SQLite database schema, helpers, and sample seed data
├── app.py                 # Flask server with routing, sales checkout, and inventory updates
└── README.md
```

## Features

- **Dashboard**: Live summary of total medicines, registered customers, total revenue, and system status.
- **Inventory Management**: View all stocked medicines with category, price, quantity, low-stock warnings, and delete actions.
- **Add Medicine**: Form to quickly register new medicines with validation.
- **Sales & Billing**:
  - Live medicine selector showing in-stock items.
  - Automatic price population and quantity limit enforcement based on available stock.
  - Real-time bill amount calculation.
  - Automatic inventory stock deduction and revenue logging upon checkout.
- **Customer Management**: Register new customer contacts and view customer directory.
- **Data Persistence**: All records are saved in local SQLite database (`pharmacy.db`).

## How to Run

1. Open your terminal in this directory:
   ```bash
   cd C:\Users\Admin\.gemini\antigravity\scratch\pharmacy_management
   ```

2. Start the Flask application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to:
   ```
   http://127.0.0.1:8080
   ```

4. Or press **F5** in VS Code to launch with Chrome using the provided `.vscode/launch.json`.

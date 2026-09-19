import sqlite3
import os

# Use /tmp on Vercel where root directory is read-only
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/pharmacy.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "pharmacy.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Medicines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER,
            medicine_name TEXT NOT NULL,
            customer_name TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_amount REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (medicine_id) REFERENCES medicines (id)
        )
    """)

    # Seed initial medicines if table is empty
    cursor.execute("SELECT COUNT(*) FROM medicines")
    if cursor.fetchone()[0] == 0:
        sample_medicines = [
            ("Paracetamol 500mg", "Analgesic", 25.00, 150),
            ("Amoxicillin 250mg", "Antibiotic", 85.50, 45),
            ("Cetirizine 10mg", "Antihistamine", 35.00, 80),
            ("Azithromycin 500mg", "Antibiotic", 115.00, 20),
            ("Omeprazole 20mg", "Antacid", 42.00, 4),  # Low stock
            ("Ibuprofen 400mg", "Pain Relief", 30.00, 65)
        ]
        cursor.executemany(
            "INSERT INTO medicines (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            sample_medicines
        )

    # Seed sample customer if empty
    cursor.execute("SELECT COUNT(*) FROM customers")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
            ("John Doe", "+91 98765 43210", "123 Health Ave, City")
        )

    conn.commit()
    conn.close()

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, init_db, DB_PATH
import os


app = Flask(__name__)
app.secret_key = "pharmacare_secret_key_change_in_production"

# Auto-initialize database for Vercel/serverless environments
if not os.path.exists(DB_PATH):
    init_db()

@app.before_request
def ensure_db():
    if not os.path.exists(DB_PATH):
        init_db()


@app.route('/')
@app.route('/dashboard')
def home():
    conn = get_db_connection()
    medicines = conn.execute("SELECT * FROM medicines ORDER BY id ASC").fetchall()
    total_customers = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
    total_sales = conn.execute("SELECT COALESCE(SUM(total_amount), 0) FROM sales").fetchone()[0]
    conn.close()
    return render_template('index.html', medicines=medicines, total_customers=total_customers, total_sales=total_sales)

@app.route('/add-medicine', methods=['GET', 'POST'])
def add_medicine():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        price_val = request.form.get('price')
        qty_val = request.form.get('quantity')

        if not name or not category or price_val is None or qty_val is None:
            flash("All fields are required.", "danger")
            return render_template('add_medicine.html')

        try:
            price = float(price_val)
            quantity = int(qty_val)
            if price < 0 or quantity < 0:
                raise ValueError("Price and quantity must be non-negative.")
        except ValueError:
            flash("Please provide valid numbers for price and quantity.", "danger")
            return render_template('add_medicine.html')

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO medicines (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            (name, category, price, quantity)
        )
        conn.commit()
        conn.close()

        flash(f"Medicine '{name}' successfully added to inventory!", "success")
        return redirect(url_for('home'))

    return render_template('add_medicine.html')

@app.route('/delete-medicine/<int:id>')
def delete_medicine(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM medicines WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Medicine deleted from inventory.", "success")
    return redirect(url_for('home'))

@app.route('/sales', methods=['GET', 'POST'])
def sales():
    conn = get_db_connection()

    if request.method == 'POST':
        medicine_id = request.form.get('medicine_id')
        customer_name = request.form.get('customer_name', '').strip() or "Walk-in Customer"
        qty_val = request.form.get('quantity')
        price_val = request.form.get('price')

        if not medicine_id or not qty_val or not price_val:
            flash("Please select a medicine, quantity, and price.", "danger")
            return redirect(url_for('sales'))

        try:
            quantity = int(qty_val)
            price = float(price_val)
        except ValueError:
            flash("Invalid quantity or price format.", "danger")
            return redirect(url_for('sales'))

        med = conn.execute("SELECT * FROM medicines WHERE id = ?", (medicine_id,)).fetchone()
        if not med:
            flash("Selected medicine does not exist.", "danger")
            return redirect(url_for('sales'))

        if med['quantity'] < quantity:
            flash(f"Insufficient stock! Only {med['quantity']} units available.", "danger")
            return redirect(url_for('sales'))

        total_amount = price * quantity

        # Record the sale
        conn.execute(
            """
            INSERT INTO sales (medicine_id, medicine_name, customer_name, quantity, unit_price, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (med['id'], med['name'], customer_name, quantity, price, total_amount)
        )

        # Update stock
        new_quantity = med['quantity'] - quantity
        conn.execute("UPDATE medicines SET quantity = ? WHERE id = ?", (new_quantity, med['id']))
        conn.commit()

        flash(f"Bill generated successfully! Total: ₹{total_amount:.2f}", "success")
        return redirect(url_for('sales'))

    # GET request
    medicines = conn.execute("SELECT * FROM medicines WHERE quantity > 0 ORDER BY name ASC").fetchall()
    recent_sales = conn.execute("SELECT * FROM sales ORDER BY id DESC LIMIT 10").fetchall()
    conn.close()

    return render_template('sales.html', medicines=medicines, sales=recent_sales)

@app.route('/customers', methods=['GET', 'POST'])
def customers():
    conn = get_db_connection()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not name or not phone:
            flash("Customer Name and Phone Number are required.", "danger")
            return redirect(url_for('customers'))

        conn.execute(
            "INSERT INTO customers (name, phone, address) VALUES (?, ?, ?)",
            (name, phone, address)
        )
        conn.commit()
        flash(f"Customer '{name}' added successfully!", "success")
        return redirect(url_for('customers'))

    customer_list = conn.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    conn.close()

    return render_template('customers.html', customers=customer_list)

if __name__ == '__main__':
    init_db()
    print("⚕️ PharmaCare running:")
    print("   💻 Local PC:   http://127.0.0.1:8080")
    print("   📱 Mobile LAN: http://10.72.111.1:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)


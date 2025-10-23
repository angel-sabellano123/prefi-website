from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # replace with a secure random key

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# PRODUCTS (all categories combined)
# ----------------------------
PRODUCTS = [
    {"id": 1, "category": "materials", "name": "Yarn", "price": 20.00, "image": "/static/images/yarn.jpg"},
    {"id": 2, "category": "materials", "name": "Crochet Hooks", "price": 50.00, "image": "/static/images/hooks.jpg"},
    {"id": 3, "category": "materials", "name": "Scissors", "price": 25.00, "image": "/static/images/scissors.jpg"},
    {"id": 4, "category": "materials", "name": "Stitch Markers", "price": 70.00, "image": "/static/images/stitch.jpg"},
    {"id": 10, "category": "flowers", "name": "Rose", "price": 40.00, "image": "/static/images/rose.jpg"},
    {"id": 11, "category": "flowers", "name": "Lily", "price": 30.00, "image": "/static/images/lily.jpg"},
    {"id": 12, "category": "flowers", "name": "Sunflower", "price": 35.00, "image": "/static/images/sunflower.jpg"},
    {"id": 13, "category": "flowers", "name": "Orchid", "price": 50.00, "image": "/static/images/orchid.jpg"},
    {"id": 20, "category": "homedecor", "name": "Pillow Covers", "price": 200.00, "image": "/static/images/pillowcover.jpg"},
    {"id": 21, "category": "homedecor", "name": "Couch Arm Rest Organizer", "price": 300.00, "image": "/static/images/organizer.jpg"},
    {"id": 22, "category": "homedecor", "name": "TV Cover", "price": 250.00, "image": "/static/images/tvcover.jpg"},
    {"id": 23, "category": "homedecor", "name": "Wall Hanging Decor", "price": 350.00, "image": "/static/images/wallhanging.jpg"},
    {"id": 24, "category": "homedecor", "name": "Crochet Rug", "price": 300.00, "image": "/static/images/rug.jpg"},
    {"id": 25, "category": "homedecor", "name": "Curtain Tiebacks", "price": 400.00, "image": "/static/images/tiebacks.jpg"},
    {"id": 30, "category": "toys", "name": "Amigurumi Animals", "price": 200.00, "image": "/static/images/animals.jpg"},
    {"id": 31, "category": "toys", "name": "Stuffed Dolls", "price": 200.00, "image": "/static/images/dolls.jpg"},
    {"id": 32, "category": "toys", "name": "Teddy Bears", "price": 200.00, "image": "/static/images/bears.jpg"},
    {"id": 33, "category": "toys", "name": "Bunny Plushies", "price": 200.00, "image": "/static/images/bunny.jpg"},
    {"id": 34, "category": "toys", "name": "Crochet Ball (Soft Toy)", "price": 200.00, "image": "/static/images/ball.JPG"},
    {"id": 35, "category": "toys", "name": "Mini Dinosaurs", "price": 200.00, "image": "/static/images/dino.jpg"},
    {"id": 36, "category": "toys", "name": "Octopus Plushies", "price": 200.00, "image": "/static/images/octopus.jpg"},
    {"id": 37, "category": "toys", "name": "Elephant Stuffed Toy", "price": 200.00, "image": "/static/images/elepant.jpg"},
    {"id": 40, "category": "blanket", "name": "Single Crochet Blanket", "price": 500.00, "image": "/static/images/single.jpg"},
    {"id": 41, "category": "blanket", "name": "Double Crochet Blanket", "price": 600.00, "image": "/static/images/double.jpg"},
    {"id": 42, "category": "blanket", "name": "Half Double Crochet Blanket", "price": 550.00, "image": "/static/images/half.jpg"},
    {"id": 43, "category": "blanket", "name": "Granny Square Blanket", "price": 700.00, "image": "/static/images/granny.jpg"},
    {"id": 44, "category": "blanket", "name": "Solid Granny Square Blanket", "price": 750.00, "image": "/static/images/solid.jpg"},
    {"id": 50, "category": "booties", "name": "Baby Booties", "price": 150.00, "image": "/static/images/baby.jpg"},
    {"id": 51, "category": "booties", "name": "Animal Crochet Booties", "price": 180.00, "image": "/static/images/animal.jpg"},
    {"id": 52, "category": "booties", "name": "Cowboy Crochet Booties", "price": 200.00, "image": "/static/images/cowboy.jpg"},
    {"id": 53, "category": "booties", "name": "Cowgirl Booties", "price": 200.00, "image": "/static/images/cowgirl.jpg"},
    {"id": 60, "category": "scarf", "name": "Single Crochet Scarf", "price": 250.00, "image": "/static/images/singles.jpg"},
    {"id": 61, "category": "scarf", "name": "Double Crochet Scarf", "price": 300.00, "image": "/static/images/doubles.jpg"},
    {"id": 62, "category": "scarf", "name": "Half Double Crochet Scarf", "price": 280.00, "image": "/static/images/halfs.jpg"},
    {"id": 63, "category": "scarf", "name": "Treble Crochet Scarf", "price": 320.00, "image": "/static/images/trebles.jpg"},
    {"id": 64, "category": "scarf", "name": "Granny Stitch Scarf", "price": 350.00, "image": "/static/images/grannys.jpg"},
    {"id": 70, "category": "basket", "name": "Round Basket", "price": 250.00, "image": "/static/images/round.jpg"},
    {"id": 71, "category": "basket", "name": "Oval Basket", "price": 300.00, "image": "/static/images/oval.jpg"},
    {"id": 72, "category": "basket", "name": "Mini Basket", "price": 150.00, "image": "/static/images/mini.jpg"},
    {"id": 73, "category": "basket", "name": "Storage Basket", "price": 350.00, "image": "/static/images/storage.jpg"},
    {"id": 74, "category": "basket", "name": "Handled Basket", "price": 400.00, "image": "/static/images/handled.jpg"},
]

# ----------------------------
# ROUTES: basic pages & category pages
# ----------------------------
@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/landingpage")
def landingpage():
    return render_template("landingpage.html")

@app.route("/materials")
def materials():
    prods = [p for p in PRODUCTS if p["category"] == "materials"]
    return render_template("materials.html", products=prods)

@app.route("/flowers")
def flowers():
    prods = [p for p in PRODUCTS if p["category"] == "flowers"]
    return render_template("flowers.html", products=prods)

@app.route("/homedecor")
def homedecor():
    prods = [p for p in PRODUCTS if p["category"] == "homedecor"]
    return render_template("homedecor.html", products=prods)

@app.route("/toys")
def toys():
    prods = [p for p in PRODUCTS if p["category"] == "toys"]
    return render_template("toys.html", products=prods)

@app.route("/blanket")
def blanket():
    prods = [p for p in PRODUCTS if p["category"] == "blanket"]
    return render_template("blanket.html", products=prods)

@app.route("/booties")
def booties():
    prods = [p for p in PRODUCTS if p["category"] == "booties"]
    return render_template("booties.html", products=prods)

@app.route("/scarf")
def scarf():
    prods = [p for p in PRODUCTS if p["category"] == "scarf"]
    return render_template("scarf.html", products=prods)

@app.route("/basket")
def basket():
    prods = [p for p in PRODUCTS if p["category"] == "basket"]
    return render_template("basket.html", products=prods)

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

# ----------------------------
# AUTH: register / login / logout
# ----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        address = request.form["address"]
        contact = request.form["contact"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        try:
            conn = get_db_connection()
            # Check if first user
            first_user = conn.execute("SELECT COUNT(*) as total FROM users").fetchone()["total"] == 0
            role = "admin" if first_user else "user"

            conn.execute("""
                INSERT INTO users (fullname, email, address, contact, password, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fullname, email, address, contact, password, role))
            conn.commit()
            conn.close()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Email already exists. Try another one.", "danger")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        contact = request.form["contact"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE contact = ? AND password = ?", (contact, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['fullname'] = user['fullname']
            session['role'] = user['role']
            flash("Login successful!", "success")
            return redirect(url_for("landingpage"))
        else:
            flash("Invalid contact number or password.", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("home"))

# ----------------------------
# CART: add, view, update, confirm order
# ----------------------------
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if 'user_id' not in session:
        flash("Please log in to add items to cart.", "warning")
        return redirect(url_for("login"))

    user_id = session['user_id']
    conn = get_db_connection()

    for p in PRODUCTS:
        sel = request.form.get(f"item_{p['id']}_selected")
        qty = request.form.get(f"item_{p['id']}_qty", type=int)
        if sel and qty and qty > 0:
            existing = conn.execute("SELECT * FROM cart WHERE user_id = ? AND product_id = ?", (user_id, p['id'])).fetchone()
            if existing:
                new_qty = existing['quantity'] + qty
                conn.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_qty, existing['id']))
            else:
                conn.execute(
                    "INSERT INTO cart (user_id, product_id, product_name, price, quantity) VALUES (?, ?, ?, ?, ?)",
                    (user_id, p['id'], p['name'], p['price'], qty)
                )
    conn.commit()
    conn.close()
    flash("Selected items added to cart.", "success")
    return redirect(url_for("matcart"))

@app.route("/matcart")
def matcart():
    if 'user_id' not in session:
        flash("Please log in to view your cart.", "warning")
        return redirect(url_for("login"))

    conn = get_db_connection()
    items = []

    if session.get('role') == "admin":
        # Admin sees all carts from all users
        items = conn.execute("""
            SELECT cart.*, users.fullname 
            FROM cart 
            JOIN users ON cart.user_id = users.id
            ORDER BY users.fullname
        """).fetchall()
    else:
        # Normal user sees only their own cart
        user_id = session['user_id']
        items = conn.execute("SELECT * FROM cart WHERE user_id = ?", (user_id,)).fetchall()

    conn.close()
    total = sum(item['price'] * item['quantity'] for item in items)
    return render_template("matcart.html", items=items, total=total)

@app.route("/update_matcart", methods=["POST"])
def update_matcart():
    if 'user_id' not in session:
        flash("Please log in.", "warning")
        return redirect(url_for("login"))
    conn = get_db_connection()
    for key, value in request.form.items():
        if key.startswith("qty_"):
            cart_id = int(key.split("_", 1)[1])
            new_qty = int(value)
            if new_qty <= 0:
                conn.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
            else:
                conn.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_qty, cart_id))
    conn.commit()
    conn.close()
    flash("Cart updated.", "success")
    return redirect(url_for("matcart"))

@app.route("/search_ajax")
def search_ajax():
    query = request.args.get("q", "").strip().lower()
    matches = []
    if query:
        matches = [
            {"name": p["name"], "category": p["category"], "image": p["image"]}
            for p in PRODUCTS if query in p["name"].lower()
        ]
    return jsonify(matches)

@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    if 'user_id' not in session:
        flash("Please log in.", "warning")
        return redirect(url_for("login"))

    user_id = session['user_id']
    payment_method = request.form.get("payment")
    if not payment_method:
        flash("Please select a payment method.", "warning")
        return redirect(url_for("matcart"))

    conn = get_db_connection()
    items = conn.execute("SELECT * FROM cart WHERE user_id = ?", (user_id,)).fetchall()
    if not items:
        conn.close()
        flash("Your cart is empty.", "warning")
        return redirect(url_for("materials"))

    total = sum(item['price'] * item['quantity'] for item in items)
    created_at = datetime.utcnow().isoformat()

    cur = conn.execute(
        "INSERT INTO orders (user_id, total, status, created_at, payment_method) VALUES (?, ?, ?, ?, ?)",
        (user_id, total, "pending", created_at, payment_method)
    )
    order_id = cur.lastrowid

    for it in items:
        conn.execute("""INSERT INTO order_items
                        (order_id, product_id, product_name, price, quantity)
                        VALUES (?, ?, ?, ?, ?)""",
                     (order_id, it['product_id'], it['product_name'], it['price'], it['quantity']))

    conn.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    flash(f"Order #{order_id} placed using {payment_method}! Total: ₱{total:.2f}. Please await confirmation.", "success")
    return redirect(url_for("landingpage"))


# ----------------------------
# ADMIN: view & approve orders
# ----------------------------
@app.route("/admin/orders")
def admin_orders():
    if session.get("role") != "admin":
        flash("You are not authorized to access this page.", "danger")
        return redirect(url_for("landingpage"))

    conn = get_db_connection()
    orders = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    orders_detail = []
    for order in orders:
        items = conn.execute("SELECT * FROM order_items WHERE order_id = ?", (order['id'],)).fetchall()
        orders_detail.append({"order": order, "items": items})
    conn.close()
    return render_template("admin_orders.html", orders=orders_detail)

@app.route("/admin/orders/approve/<int:order_id>")
def approve_order(order_id):
    if session.get("role") != "admin":
        flash("You are not authorized.", "danger")
        return redirect(url_for("landingpage"))
    conn = get_db_connection()
    conn.execute("UPDATE orders SET status = 'approved' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    flash(f"Order #{order_id} approved.", "success")
    return redirect(url_for("admin_orders"))

# ----------------------------
# STARTUP: create tables if not exist
# ----------------------------
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            address TEXT,
            contact TEXT,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            total REAL,
            status TEXT,
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            product_name TEXT,
            price REAL,
            quantity INTEGER,
            FOREIGN KEY (order_id) REFERENCES orders(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database and tables ready.")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

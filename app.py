from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/landingpage")
def landingpage():
    return render_template("landingpage.html")

@app.route("/materials")
def materials():
    return render_template("materials.html")

@app.route("/flowers")
def flowers():
    return render_template("flowers.html")

@app.route("/toys")
def toys():
    return render_template("toys.html")

@app.route("/blanket")
def blanket():
    return render_template("blanket.html")

@app.route("/homedecor")
def homedecor():
    return render_template("homedecor.html")

@app.route("/scarf")
def scarf():
    return render_template("scarf.html")

@app.route("/booties")
def booties():
    return render_template("booties.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/basket")
def basket():
    return render_template("basket.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/about")
def about():
    return "<h1>About Us Page</h1>"

@app.route("/register")
def register():
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
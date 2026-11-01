
from flask import Flask, render_template

# Create Flask application
app = Flask(__name__)

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# About page
@app.route("/about")
def about():
    return "Welcome to DataVision!"

# Run the application
if __name__ == "__main__":
    app.run(debug=True, port=5000)

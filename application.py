import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html",msg="Enter here:")

@app.route("/detail", methods=["GET","POST"])
def detail():
    name = request.form.get("name")
    title = db.execute("SELECT * FROM books WHERE title = :name",{"name": name}).fetchall()
    if title is None or name!=title:
        return render_template("error.html", message="No book found.")
    else:
        return render_template("details.html", details=title)

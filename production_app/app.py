import logging
import os.path
from flask import Flask, request, redirect,render_template
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
from prometheus_flask_exporter import PrometheusMetrics


app =  Flask(__name__)
metrics = PrometheusMetrics(app)


#this line connect to the db and create new db named registrations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'
#initializes a database object named db using the SQLAlchemy library in Python.
db = SQLAlchemy(app)

class Registration(db.Model):
    #all of thw bellow are the table column
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


@app.route('/')
def projectIntro():
    return render_template("Introduction.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    try:
        if request.method == "POST":
            full_name = request.form.get("fullname")
            # Set the environment variable for the Docker container
            os.environ['USERNAME'] = full_name
            email = request.form.get("email")
            #creatiing new table named registration 
            registration = Registration(full_name=full_name, email=email)
            db.session.add(registration)
            db.session.commit()
            return redirect("/Welcome?fullname=" + full_name)
    except Exception as e:
        logging.error("An error occurred during database operations: %s", str(e))
    return render_template("Signup.html")


@app.route('/Welcome')
def hello_user():
    full_name = request.args.get("fullname")
    return render_template("Welcome.html", fullname=full_name)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)


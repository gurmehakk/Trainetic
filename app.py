from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(host="localhost", user="root", passwd="AbCd@123", database="railway_system")


@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html");


@app.route('/admin_login')
def admin_log():
    return render_template("admin_log.html");


@app.route('/user_login')
def user_log():
    return render_template("user_login.html");


@app.route('/Registration_screen')
def user_register():
    return render_template("Registration_screen.html");


@app.route('/About_us')
def aboutuspage():
    return render_template("about_us.html");


@app.route('/Contact_us')
def contact_us():
    return render_template("contact_us.html")


if __name__ == '__main__':
    app.run()

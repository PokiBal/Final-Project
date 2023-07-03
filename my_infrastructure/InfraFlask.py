from flask import Flask, request, redirect, render_template, url_for
import docker
import subprocess
import os
import sqlite3
from Infrastructure import CreateJobFromFlask, new_jenkins_user, run_job,create_iam_user,create_ec2_instance


def sql_connection():
    try:
        connection = sqlite3.connect("C:/Users/Inbal-Laptop/Documents/myRepository/MyProject_1/instance/registrations.db")
    except Exception as e:
        print("connection failed with:{e}",e)
    return connection

def sql_table(connection):
    cursor_obj = connection.cursor()
    cursor_obj.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER PRIMARY KEY AUTOINCREMENT, image_name TEXT)")
    connection.commit()

def sql_insert(connection, entity):
    cursor_obj = connection.cursor()
    cursor_obj.execute("INSERT INTO images(image_name) VALUES(?)", (entity,))
    connection.commit()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
# Asks the user for the image_name, and save it into myDB table "registrations"
        if 'submit_image_name' in request.form:
            image_name = request.form.get('image_name')
            con = sql_connection()
            try:
                sql_insert(con, image_name)
            except Exception as e:
                print("some error occuredd", e)
            return redirect('/upload?image_name=' + image_name)
        elif 'create_job' in request.form:
            job_name = request.form.get('job_name')
            resultMessage = CreateJobFromFlask(job_name)
            return redirect('/newJob?job_name=' + job_name + '&resultMessage=' + resultMessage)
        elif 'create_user' in request.form:
            user_name = request.form.get('user_name')
            password = request.form.get('password')
            resultMessage = new_jenkins_user(user_name, password)
            return redirect('/created_success?user_name=' + user_name + '&resultMessage=' + (resultMessage or ''))
        elif 'create_IAM' in request.form:
            user_name = request.form.get('user_name')
            password = request.form.get('password')
            resultMessage = create_iam_user(user_name,password)
            return redirect('/created_success?user_name=' + user_name + '&resultMessage=' + str(resultMessage))
        elif 'create_EC2' in request.form:
            instance_name = request.form.get('instance_name')
            resultMessage = create_ec2_instance(instance_name)
            return redirect('/created_success?instance_name=' + (instance_name or '') + '&resultMessage=' + (str(resultMessage) if resultMessage is not None else ''))

    return render_template('index.html')




#'Upload your image' - will trigger the pull, build, tests and at the end -> upload to docker hub
@app.route('/upload')
def upload():
    image_name = request.args.get("image_name")
    message1 = f"Please wait while we process your request to create a new image: {image_name}"
    message2 = run_job('build and test pipeline')

    return render_template("upload.html", message1=message1,message2=message2)

@app.route('/newJob')
def NewJob_result():
    resultMessage = request.args.get("resultMessage")
    return render_template("newJob.html", resultMessage=resultMessage)

@app.route('/created_success')
def NewUser_result():
    resultMessage = request.args.get("resultMessage")
    return render_template("created_success.html", resultMessage=resultMessage)

if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0", port=5001)






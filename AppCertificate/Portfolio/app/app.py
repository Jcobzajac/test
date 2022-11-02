from flask import Flask, session, request, render_template, redirect, url_for, make_response
from flask_session import Session
import mysql.connector
from datetime import datetime

############################    FUNCTIONS   #############################   

#Connection to the database
def getMysqlConnection():
    return mysql.connector.connect(user='root', host='appcertificate_mydb_1', port='3306', password='password', database='records',auth_plugin='mysql_native_password')

#Verifying correctness of personal id
def validate_personal_id(data):
        id = data["id"]
        session["id"] = id
        db = getMysqlConnection()
        cur = db.cursor() 
        cur.execute(f"SELECT personid FROM certifications WHERE personid='{id}'")
        result = cur.fetchall()
        if len(result) == 0:    #Checking whether id exists (Query returns array with results)
            return False
        else:
            return True

#Function for handling different errors
def handling_error(message,status_code):
    info = message
    response = make_response(render_template("error.html",content=info), status_code)
    return response









#Configuring application
app = Flask(__name__)
# Configuring session
app.config["SESSION_PERMANENT"] = False
SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)










@app.route('/', methods=['GET','POST'])
def starting_page():
    return render_template('home.html')




@app.route('/form', methods=['GET','POST'])
def form():
    if request.method == "POST":
        information = request.form              #Assigning values from form to variables in order to handle the logic               
        name = information["name"]
        surname = information["surname"]
        id = information["id"]
        first_place = information["first_place"]
        second_place = information["second_place"]
        third_place = information["third_place"]
        fourth_place = information["fourth_place"]
        comment = information["comment"]
        
        checking_array = []     #Creating array to check whether user has duplicated the certification
        for element in information:     #Revision of user input
            if element == "comment":    #Skipping comment, because it isn't mandatory field
                continue
            elif element in ["name","surname"]:     #Checking conditions for personal data(lenght and if form was populated)
                if information[element] == "":
                    return handling_error("Please fill the form",400)
                elif len(information[element]) < 3:
                    return handling_error("Too short name or surname. Minimum length is 3 characters",400)
                else:
                    continue
            elif element == "id" and len(information[element] ) != 11:      #Testing length of the Personal ID Number
                return handling_error("Wrong id. The lenght of id is 11 characters",400)
            elif "place" in element and information[element]:       #Adding certification to the array (Each select name for the certification field contains place in string). 
                checking_array.append(information[element])
        if len(checking_array) != len(set(checking_array)): #Verifying whether user didn't include any duplicates in terms of certifications
            return handling_error("You can choose one certificate only once. Please don't duplicate them",400)
        db = getMysqlConnection()
        cur = db.cursor()
        cur.execute(f"SELECT personid FROM certifications WHERE personid='{id}'")
        result = cur.fetchall()
        if len(result) != 0:
            return handling_error("This id is used. Please contact our support if it yours",400)
        cur.execute("INSERT INTO certifications(personid,name,surname,first,second,third,fourth,comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id,name,surname,first_place,second_place,third_place,fourth_place,comment))
    
        return handling_error("Your form was sent!",200)
        

    else:
        return render_template("form.html")

@app.route('/change', methods=['GET','POST'])
def change():
    return render_template("change.html")



@app.route('/change/update/id', methods=['GET','POST'])
def update_id():
    if request.method == "POST":
        if validate_personal_id(request.form):
            return redirect(url_for('update_form')) #If id is valid, redirect user to the page with the update form
        else:
            return handling_error("This id doesn't exist",404)
    else:
        return render_template("change-id.html")


@app.route('/change/delete/id', methods=['GET','POST'])
def delete_id():
    if request.method == "POST":
        if validate_personal_id(request.form): #If id exists then delete data where id is assigned
            id = session["id"]
            db = getMysqlConnection()
            cur = db.cursor() 
            cur.execute(f"DELETE FROM certifications WHERE personid='{id}'")
            return "You've deleted application"   
        else:
            return handling_error("This id doesn't exist",400)
    else:
        return render_template("change-id.html")

@app.route('/change/update/id/form', methods=['GET','POST'])
def update_form():
    if request.method == "POST":
        information = request.form
        first_place = information["first_place"]
        second_place = information["second_place"]
        third_place = information["third_place"]
        fourth_place = information["fourth_place"]
        comment = information["comment"]
        ### Detecting mistakes in the certifications in the case of duplication ###
        information = request.form
        array = [information[element] for element in information]
        if len(array) == len(set(array)):
            id = session.get('id')
            db = getMysqlConnection()
            cur = db.cursor() 
            cur.execute(f"UPDATE certifications SET first = '{first_place}', second = '{second_place}', third = '{third_place}', fourth = '{fourth_place}', comment = '{comment}'  WHERE personid = '{id}'")
            return handling_error("Updated successfully",200)
        else:
            return handling_error("You can choose one certificate only once. Please don't duplicate them",400)           
    else:
        return render_template("change-form.html")
    
@app.route('/declaration', methods=['GET','POST'])
def declaration():
    return render_template("declaration.html")

@app.route('/declaration/id', methods=['GET','POST'])
def declaration_id():
    if request.method == "POST":
        if validate_personal_id(request.form):
            id = session["id"]
            db = getMysqlConnection()
            cur = db.cursor() 
            cur.execute(f"SELECT first,second,third,fourth FROM certifications WHERE personid='{id}'")
            results = cur.fetchall()
            session["certifications"] = results[0]
            return redirect(url_for('declaration_your'))
        else:
            return handling_error("This id doesn't exist",400)
    else:
        return render_template("change-id.html")

@app.route('/declaration/id/your', methods=['GET','POST'])
def declaration_your():
    return render_template("declaration-your.html",content=session["certifications"])



@app.route('/declaration/latest', methods=['GET','POST'])
def test():
    db = getMysqlConnection()
    cur = db.cursor() 
    cur.execute("SELECT * FROM certifications ORDER BY id DESC LIMIT 1")
    result = cur.fetchall()
    if len(result) == 0:
        return handling_error("There isn't any assignments",404)
    result = result[0]
    return render_template("declaration-latest.html", content=result)



@app.route('/declaration/overall', methods=['GET','POST'])
def overall():
    return render_template("declaration-overall.html")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

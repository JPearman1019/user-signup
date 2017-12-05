from flask import Flask, request
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = True



@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render(username='', username_error='', password_error='',
    verify_error='', email='', email_error='')

def not_empty(userinput):
    if userinput != "":
        return True
    return False

def len_valid(userinput):
    if len(userinput) >= 3 and len(userinput) <= 20:
        return True
    return False

def char_check(userinput, char):
    for i in userinput:
        if i == char:
            return False
    return True

def str_compare(string1, string2):
    if string1 == string2:
        return True
    return False

def chk_mult(userinput, char):
    check = 0
    for i in userinput:
        if i == char:
            check += 1
    if check == 1:
        return True

    return False


def username_val(usernm_input):
    username_error="That's not a valid username"
    if not_empty(usernm_input) and len_valid(usernm_input) and char_check(usernm_input, " "):
        username_error=""

    return username_error

def password_val(pass_input):
    password_error="That's not a valid password"
    if not_empty(pass_input) and len_valid(pass_input) and char_check(pass_input, " "):
        password_error=""

    return password_error

def verify_val(verif_input, pass_input):
    verify_error="Passwords don't match"
    if not_empty(verif_input) and str_compare(verif_input, pass_input):
        verify_error=""

    return verify_error

def email_val(email_input):
    email_error="That's not a valid email"
    if (chk_mult(email_input, "@") and chk_mult(email_input, ".") 
        and char_check(email_input, " ") and len_valid(email_input) or email_input ==""):
        email_error=""

    return email_error



@app.route("/", methods=['POST'])
def validate():
    username= str(request.form['username'])
    password= request.form['password']
    verify= request.form['verify']
    email= request.form['email']
    template = jinja_env.get_template('index.html')
    template2 = jinja_env.get_template('welcome.html')

    username_error=username_val(username)
    password_error=password_val(password)
    verify_error=verify_val(verify, password)
    email_error=email_val(email)

    if username_error == "" and password_error == "" and verify_error == "" and email_error == "":
        """return welcome(username)"""
        return template2.render(username=username)

    return template.render(username=username, username_error=username_error, 
        password_error=password_error, verify_error=verify_error, 
        email=email, email_error=email_error)

"""
@app.route("/welcome", methods=['POST'])
def welcome(username):
    template2 = jinja_env.get_template('welcome.html')
    return template2.render(username=username)
"""

app.run()
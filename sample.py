from flask import Flask,render_template,request,redirect,url_for,flash
import requests
import hashlib
import sys
import smtplib

app = Flask(__name__)

app.config['SECRET_KEY'] = "ashwanth"

def sendmail(email,password,msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email,msg)
    server.quit()
    return "hello"


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit',methods=["GET","POST"])
def submit():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        msg = f"Hi Ashwanth, \n {name} is trying to get in touch with you.Email address: {email}. \n\nMessage: {message}"
        mail = sendmail("ashwanthbalajir@gmail.com","jnib oclw marp yhak",msg)
        print(mail)
        flash("Form submitted Successfully!")
        return redirect('contact')
    else:
        return render_template("contact.html")

def request_api_check(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the API endpoint and try again")
    return res

def get_password_leaks_count(hashes,hashes_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h,count in hashes:
     if h == hashes_to_check:
        return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5char, tail = sha1password[:5], sha1password[5:]
    response = request_api_check(first5char)
    return get_password_leaks_count(response,tail)

def mfun(pwd):
    count = pwned_api_check(pwd)
    if count:
        return f"{pwd} was found {count} times....you should change your password."
    else:
        return f"{pwd} not found... Carry on..."

def hash_cracker(hname):
        hashed_cracked = ""
        with open("dict.txt") as file:
            for line in file:
                line = line.strip()
                if hashlib.md5(line.encode('utf-8')).hexdigest() == hname:
                    hashed_cracked = line
                    return "MD5-hash has been successfully cracked.The Value is %s."%line
        if hashed_cracked == "":
            return "\nFailed to crack the hash.Try to use a bigger/different dictionary."




@app.route('/pass')
def index():
    return render_template('index.html')


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    pword = mfun(name)  # Determine if the result is being printed
    return render_template("index.html", pword=pword)

@app.route('/hash',methods=["GET","POST"])
def hash():
    return render_template('hash.html')

@app.route('/hash_checker',methods=["POST"])
def hash_checker():
    hname = request.form.get("hash")
    result = hash_cracker(hname)
    print(result)
    return render_template('hash.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
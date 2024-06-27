from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract
import re
from flask import Flask, request, render_template, redirect, url_for,flash, session
import traceback





w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


app = Flask(__name__)

contract = w3.eth.contract(address=address_contract, abi=abi)
app.secret_key = 'super_secret_key' 

@app.route('/')
def index():
        return render_template("login.html")

account_addresspublic = None

@app.route('/login', methods=['POST'])
def login():
    global account_addresspublic
    try:
        account_address = request.form['login']
        account_addresspublic = account_address
        password = request.form['password']  
        w3.geth.personal.unlock_account(account_address, password)
        session['login'] = account_address
        return redirect(url_for('profile'))
    except Exception as e:
        flash(f"Incorrect password or user{e}")
        return redirect(url_for('index'))


@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route("/register", methods=['POST', 'GET']) 
def register(): 
    return render_template("register.html")


def passwordCheck(password):
        # Проверка длины пароля
    if len(password) < 12:
        print("Password must be mor then 12 character")
        return False
    
    # Проверка наличия заглавных букв
    if not re.search(r'[A-Z]', password):
        print("Must be one upper character")
        return False
    
    # Проверка наличия строчных букв
    if not re.search(r'[a-z]', password):
        print("Must be one lower character")
        return False
    
    # Проверка наличия цифр
    if not re.search(r'\d', password):
        print("Must be one number")
        return False
    
    # Проверка наличия специальных символов
    if not re.search(r'[!@#\$%]', password):
        print("Must be one special character")
        return False
    
    # Проверка на простые шаблоны
    if re.search(r'password|qwerty', password):
        print("Must be not common")
        return False
    
    return True



@app.route('/registeraccount', methods=['POST'])
def registeraccount():

    password = request.form['password']
    if passwordCheck(password) == True:
        new_account = w3.geth.personal.new_account(password)
        return render_template("register.html", new_account=new_account)
        
    else:
        flash("wrong password")
        return redirect(url_for('register'))


@app.route('/balanceshow', methods=['POST'])
def balanceshow(): 
    account_address = session['login']
    balancecurrent = balance(account_address)
    return render_template('profile.html', balanceshowingcurrent=balancecurrent)


def balance(account_address): 
    try:
        balance =  w3.eth.get_balance(account_address)  
    except Exception as e:
        print(e)
    return balance


@app.route('/createestate_open', methods=['POST'])
def createestate_open():
    return render_template('createestate.html')

@app.route('/createestate', methods=['POST']) 
def createEstate():
    try:
        size = request.form['size']
        adress = request.form['adress']
        es_type = request.form['es_type']
        account_address = account_addresspublic
        estate = contract.functions.createEstate(int(size), adress, int(es_type)).transact({'from': account_address})
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')
    
@app.route('/createadd_open', methods=['POST'])
def createadd_open():
    return render_template('createadd.html')

@app.route('/createadd', methods=['POST'])
def create_add():
    try:
        price = request.form['price']
        idad = request.form['idad']
        adstatus = request.form['status']
        account_address = account_addresspublic
        ad = contract.functions.createAd(int(price), int(idad), int(adstatus)).transact({'from': account_address})
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')



@app.route('/updateEstateStatus_open', methods=['POST'])
def updateEstateStatus_open():
    return render_template('updateEstateStatus.html')

@app.route('/updateEstateStatus', methods=['POST'])
def updateEstateStatus():
    try:
        idestate = request.form['idestate']
        status = request.form['idestate']

        updateEstateStatus = contract.functions.updateEstateStatus(int(idestate),bool(status)).transact()
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')




@app.route('/updateaddstatus_open', methods=['POST'])
def updateaddstatus_open():
        return render_template('updateaddstatus.html')


@app.route('/updateAdStatus', methods=['POST'])
def updateAdStatus(account_address):
    try:
        idad= request.form['idad']
        status = request.form['status']
        account_address = account_addresspublic
        updateadStatus = contract.functions.updateAdStatus(int(idad),int(status)).transact({'from': account_address}) 
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')

@app.route('/withDraw_open', methods=['POST'])
def withDraw_open():
    return render_template('withDraw.html')

@app.route('/withDraw', methods=['POST'])
def withDraw(account_address):
    try:
        amount = request.form["amount"]
        account_address = account_addresspublic
        withDraw = contract.functions.withDraw(int(amount)).transact({'from': account_address}) 
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')


@app.route('/buyEstate_open', methods=['POST'])
def buyEstate_open():
    return render_template('buyestate.html')

@app.route('/buyEstate', methods=['POST'])
def buyEstate(account_address):
    try:
        idad = request.form["idad"]
        account_address = account_addresspublic
        buy = contract.functions.buyEstate(int(idad)).transact({'from': account_address}) 
        return render_template('profile.html')  # Добавить эту строку
    except Exception as e:
        flash(str(e))
        return render_template('profile.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run(debug=True)  

@app.errorhandler(404)
def page_not_found(error):
    traceback.print_exc()
    return render_template('page_not_found.html'), 404


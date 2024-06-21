from web3 import Web3
from web3.middleware import geth_poa_middleware
from contract_info import abi, address_contract
import re
from flask import Flask, request, render_template, redirect, url_for,flash, session


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)


app = Flask(__name__)

contract = w3.eth.contract(address=address_contract, abi=abi)
app.secret_key = 'super_secret_key' 

@app.route('/')
def index():
        return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    try:
        account_address = request.form['login']
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
    balance = account_address(account_address)
    return render_template('profile.html', balance=balance)


def balance(account_address): 
    try:
        balance =  w3.eth.get_balance(account_address)  
    except Exception as e:
        print(e)
    return balance


@app.route('/createestate_open', methods=['POST'])
def createestate_open():
    return render_template('createestate.html')

@app.route('/createestateS', methods=['POST'])
def createEstate(account_address):
    try:
        size = request.form(size)
        memory = request.form(memory)
        es_type = request.form(es_type)
        account_address = session['login']
        estate = contract.functions.createEstate(size,memory,es_type).transact({'from': account_address})
        print(f"transaction was send {estate.hex()}")
    except Exception as e:
        print(e)

@app.route('/createadd_open', methods=['POST'])
def createadd_open():
    return render_template('createadd.html')


def create_add(account_address):
    try:
        price = request.form(price)
        idad = request.form(idad)
        adstatus = request.form(adstatus)
        account_address = session['login']
        ad = contract.functions.createAd(price, idad,adstatus).transact({'from': account_address})
        flash(f"add was created {ad.hex()}")
    except Exception as e:
        flash(e)


@app.route('/updateEstateStatus_open', methods=['POST'])
def createadd_open():
    return render_template('updateEstateStatus.html')

@app.route('/updateEstateStatus', methods=['POST'])
def updateEstateStatus():
    try:
        idestate = request.form(idestate)
        status = request.form(status)

        updateEstateStatus = contract.functions.updateEstateStatus(idestate,status).transact()
        flash(f"estate was update {updateEstateStatus.hex()}")

    except Exception as e:
        flash(e)




@app.route('updateaddstatus_open', methods=['POST'])
def updateaddstatus_open():
        return render_template('updateaddstatus.html')


@app.route('/updateAdStatus', methods=['POST'])
def updateAdStatus(account_address):
    try:
        idad= request.form(idad)
        status = request.form(status)
        account_address = session['login']
        updateadStatus = contract.functions.updateAdStatus(idad,status).transact({'from': account_address}) 
        flash(f"add was update {updateadStatus.hex()}")

    except Exception as e:
        flash(e)


@app.route('/withdraw_open', methods=['POST'])
def withdraw_open():
    return render_template('withdraw.html')


def withDraw(account_address):
    try:
        amount = request.form(amount)
        account_address = session['login']
        withDraw = contract.functions.withDraw(amount).transact({'from': account_address}) 
        flash(f"withdraw sucess {withDraw.hex()}" )
    except Exception as e:
        flash(e)


@app.route('/buyEstate_open', methods=['POST'])
def buyEstate_open():
    return render_template('buyestate.html')

def buyEstate(account_address):
    try:
        idad = request.form(idad)
        account_address = session['login']
        buy = contract.functions.buyEstate(idad).transact({'from': account_address}) 
        flash(f"buy sucess {buy.hex()}")

    except Exception as e:
        flash(e)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    app.run(debug=True)  


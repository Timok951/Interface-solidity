from web3 import Web3, EthereumTesterProvider
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

accounts = w3.eth.accounts

for account in accounts:
    balance = w3.eth.get_balance(account)
    print(f'Баланс аккаунта {account}: {w3.from_wei(balance, "ether")} ETH')
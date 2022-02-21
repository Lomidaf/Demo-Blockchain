# from solcx import compile_standard, install_solc
import json
from solcx import compile_standard
from web3 import Web3

with open("./SimpleStorage.sol") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    # solc_version="0.6.0",
)

with open("compile_code.json", "w") as file:
    json.dump(compiled_sol, file)

byte_code = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
chain_id = 1337
my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
private_key = "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d"

SimpleStorage = w3.eth.contract(abi=abi, bytecode=byte_code)
nonce = w3.eth.getTransactionCount(my_address)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_tx = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
nonce = nonce + 1
print(tx_receipt.contractAddress)

# contractAddress = "0x8cC67c51B028B78b9b598C9DE9f4B74861d80a5A"
# simple_storage = w3.eth.contract(address=contractAddress, abi=abi)


store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrieve().call())

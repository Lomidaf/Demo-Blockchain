from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORK_LOCAL_ENV = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]

DECIMAL = 8
STARTING_PRICE = 200000000000


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORK_LOCAL_ENV
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mock():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mock...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE, {"from": get_account()})

from multiprocessing.connection import wait
from brownie import accounts, SimpleStorage, network, config


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(10, {"from": account})
    transaction.wait(1)

    stored_value = simple_storage.retrieve()
    print(stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        pass


def main():
    deploy_simple_storage()

from brownie import (
    Contract,
    network,
    config,
    accounts,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    interface,
)
from web3 import Web3

FORK_LOCAL_ENV = ["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]

DECIMAL = 8
STARTING_PRICE = 200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load("id")
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORK_LOCAL_ENV
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vtf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mock()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mock(decimal=DECIMAL, initial_value=STARTING_PRICE):
    MockV3Aggregator.deploy(DECIMAL, STARTING_PRICE, {"from": get_account()})
    link_token = LinkToken.deploy({"from": get_account()})
    VRFCoordinatorMock.deploy(link_token.address, {"from": get_account()})
    print("DEPLOY MOCK!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=200000000000000000
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Fund complete!")
    return tx

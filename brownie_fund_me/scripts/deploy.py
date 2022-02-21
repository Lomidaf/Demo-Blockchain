from brownie import FundMe, network, config, MockV3Aggregator
from rsa import verify
from scripts.utils import deploy_mock, get_account, LOCAL_BLOCKCHAIN_ENV
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mock()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract deployed to {}".format(fund_me.address))
    return fund_me


def main():
    deploy_fund_me()

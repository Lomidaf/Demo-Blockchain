from scripts.utils import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network
import time


def deploy_lottery():
    account = get_account()

    Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vtf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery")


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print("LOTTERY IS STARTING")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("ENTER LOTTERY")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx_fund = fund_with_link(lottery.address)
    tx_fund.wait(1)
    tx_end = lottery.endLottery({"from": account})
    tx_end.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

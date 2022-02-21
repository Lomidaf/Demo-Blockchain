import pytest
from web3 import Web3
from brownie import Lottery, accounts, config, network, exceptions
from scripts.deploy import deploy_lottery, start_lottery, end_lottery
from scripts.utils import (
    LOCAL_BLOCKCHAIN_ENV,
    get_account,
    fund_with_link,
    get_contract,
)
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]
    account = get_account()

    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    tx2 = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx2.wait(1)
    fund_with_link(lottery)
    tx_end = lottery.endLottery({"from": account})
    tx_end.wait(1)
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0

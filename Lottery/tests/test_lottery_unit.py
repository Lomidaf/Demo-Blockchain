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


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]

    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]

    with pytest.raises(exceptions.VirtualMachineError):
        fee = lottery.getEntranceFee()
        lottery.enter({"from": get_account(), "value": fee})


def test_can_enter_start():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]
    account = get_account()

    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]
    account = get_account()

    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    fund_with_link(lottery)
    tx_end = lottery.endLottery({"from": account})
    tx_end.wait(1)

    assert lottery.lottery_state() == 2


def test_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip()
    deploy_lottery()
    lottery = Lottery[-1]
    account = get_account()

    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    tx2 = lottery.enter(
        {"from": get_account(index=1), "value": lottery.getEntranceFee()}
    )
    tx2.wait(1)
    tx3 = lottery.enter(
        {"from": get_account(index=2), "value": lottery.getEntranceFee()}
    )
    tx3.wait(1)

    fund_with_link(lottery)
    tx_end = lottery.endLottery({"from": account})
    tx_end.wait(1)
    request_id = tx_end.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    start_balance = account.balance()
    balance_of_lottery = lottery.balance()
    tx_random = get_contract("vtf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )
    tx_random.wait(1)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == start_balance + balance_of_lottery

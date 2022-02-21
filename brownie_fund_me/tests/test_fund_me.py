from scripts.interact import fund
from scripts.utils import LOCAL_BLOCKCHAIN_ENV, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdrew():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdrew():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local network")
    account = get_account()
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdrew({"from": bad_actor})

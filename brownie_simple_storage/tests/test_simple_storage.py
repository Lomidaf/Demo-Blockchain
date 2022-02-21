from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]
    # Action
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    # Assert / Check
    assert starting_value == 0


def test_updating_storage():
    # Arrange
    account = accounts[0]
    # Action
    simple_storage = SimpleStorage.deploy({"from": account})
    tx = simple_storage.store(15, {"from": account})
    tx.wait(1)

    starting_value = simple_storage.retrieve()

    assert starting_value == 15

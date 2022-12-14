from brownie import reverts


def test_add_executor(bvecvx_module, governance, accounts):
    bvecvx_module.addExecutor(accounts[3], {"from": governance})
    assert accounts[3] in bvecvx_module.getExecutors()


def test_add_executor_random_account(bvecvx_module, accounts):
    with reverts("not-governance!"):
        bvecvx_module.addExecutor(accounts[3], {"from": accounts[6]})


def test_remove_executor(bvecvx_module, governance, accounts):
    bvecvx_module.addExecutor(accounts[3], {"from": governance})
    assert accounts[3] in bvecvx_module.getExecutors()
    bvecvx_module.removeExecutor(accounts[3], {"from": governance})
    assert accounts[3] not in bvecvx_module.getExecutors()


def test_remove_executor_random_account(bvecvx_module, accounts):
    with reverts("not-governance!"):
        bvecvx_module.removeExecutor(accounts[3], {"from": accounts[6]})


def test_set_guardian(bvecvx_module, governance, accounts):
    bvecvx_module.setGuardian(accounts[3], {"from": governance})
    assert bvecvx_module.guardian() == accounts[3]


def test_set_guardian_random_account(bvecvx_module, accounts):
    with reverts("not-governance!"):
        bvecvx_module.setGuardian(accounts[3], {"from": accounts[6]})

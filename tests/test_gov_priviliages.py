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


def test_set_withdrawable_factor(bvecvx_module, governance, techops):
    bvecvx_module.setWithdrawableFactor(5_000, {"from": governance})
    assert bvecvx_module.factorWd() == 5_000

    bvecvx_module.setWithdrawableFactor(6_000, {"from": techops})
    assert bvecvx_module.factorWd() == 6_000


def test_set_withdrawable_factor_greater_than_max(bvecvx_module, governance):
    with reverts(">MAX_FACTOR_WD!"):
        bvecvx_module.setWithdrawableFactor(9_000, {"from": governance})


def test_set_withdrawable_factor_random_account(bvecvx_module, accounts):
    with reverts("not-gov-or-guardian"):
        bvecvx_module.setWithdrawableFactor(5_000, {"from": accounts[6]})


def test_set_weekly_cvx_spot_amount(bvecvx_module, governance, techops):
    bvecvx_module.setWeeklyCvxSpotAmount(15_000, {"from": governance})
    assert bvecvx_module.weeklyCvxSpotAmount() == 15_000

    bvecvx_module.setWeeklyCvxSpotAmount(3_000, {"from": techops})
    assert bvecvx_module.weeklyCvxSpotAmount() == 3_000


def test_set_weekly_cvx_spot_amount_random_account(bvecvx_module, accounts):
    with reverts("not-gov-or-guardian"):
        bvecvx_module.setWeeklyCvxSpotAmount(5_000, {"from": accounts[6]})

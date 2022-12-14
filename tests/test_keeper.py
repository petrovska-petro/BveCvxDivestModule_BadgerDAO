from brownie import chain, reverts

ONE_WEEK = 604800


def is_upkeep_needed(bvecvx_module, keeper):
    upkeep_needed, _ = bvecvx_module.checkUpkeep(b"", {"from": keeper})
    return upkeep_needed


def test_perform_upkeep_keeper(
    bvecvx_module, cvx_locker, bvecvx, usdc, governance, treasury, keeper
):
    upkeep_needed = is_upkeep_needed(bvecvx_module, keeper)
    assert upkeep_needed

    usdc_bal_before = usdc.balanceOf(treasury)
    bvecvx_bal_before = bvecvx.balanceOf(governance)

    bvecvx_module.performUpkeep(b"", {"from": keeper})

    # verify bvecvx bal in `voter` decreased and usdc bal in treasury increased
    assert bvecvx_module.lastEpochIdWithdraw() > 0
    assert usdc.balanceOf(treasury) > usdc_bal_before
    assert bvecvx.balanceOf(governance) < bvecvx_bal_before

    # assert that `checkUpKeep` returs `False` and will not try to wd constantly
    upkeep_needed = is_upkeep_needed(bvecvx_module, keeper)
    assert not upkeep_needed

    # modify `epochCount` storage to fake-trigger `True` in keeper
    chain.mine(timestamp=chain.time() + ONE_WEEK)
    cvx_locker.checkpointEpoch({"from": keeper})

    upkeep_needed = is_upkeep_needed(bvecvx_module, keeper)
    assert upkeep_needed


def test_perform_upkeep_paused_state(bvecvx_module, keeper, governance):
    bvecvx_module.pause({"from": governance})
    with reverts("Pausable: paused"):
        bvecvx_module.performUpkeep(b"", {"from": keeper})
    bvecvx_module.unpause({"from": governance})


def test_perform_upkeep_from_random_account(bvecvx_module, accounts):
    with reverts("not-executor!"):
        bvecvx_module.performUpkeep(b"", {"from": accounts[6]})

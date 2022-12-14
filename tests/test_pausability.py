from brownie import reverts


def test_pausa_governance(bvecvx_module, governance):
    bvecvx_module.pause({"from": governance})
    assert bvecvx_module.paused()


def test_unpause_guardian(bvecvx_module, techops):
    with reverts("not-governance!"):
        bvecvx_module.unpause({"from": techops})


def test_unpause_governance(bvecvx_module, governance):
    bvecvx_module.pause({"from": governance})
    assert bvecvx_module.paused()
    bvecvx_module.unpause({"from": governance})
    assert bvecvx_module.paused() == False


def test_pause_guardian(bvecvx_module, techops):
    bvecvx_module.pause({"from": techops})
    assert bvecvx_module.paused()


def test_pause_random_account(bvecvx_module, accounts):
    with reverts("not-gov-or-guardian"):
        bvecvx_module.pause({"from": accounts[6]})

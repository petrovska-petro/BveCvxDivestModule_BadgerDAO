from brownie import reverts


def test_revoke_whitelisting(safe, bvecvx_module, keeper):
    # https://etherscan.io/address/0x34cfac646f301356faa8b21e94227e3583fe3f5f#code#L171
    SENTINEL_MODULES = "0x0000000000000000000000000000000000000001"
    safe.disableModule(SENTINEL_MODULES, bvecvx_module.address, {"from": safe})

    with reverts("no-module-enabled!"):
        bvecvx_module.performUpkeep(b"", {"from": keeper})

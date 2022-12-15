from brownie import BveCvxDivestModule, accounts


def main(deployer_label=None):
    deployer = accounts.load(deployer_label)

    return BveCvxDivestModule.deploy(
        "0x86cbD0ce0c087b482782c181dA8d191De18C8275",  # https://github.com/Badger-Finance/badger-multisig/blob/main/helpers/addresses.py#L54
        {"from": deployer},
        publish_source=True,
    )

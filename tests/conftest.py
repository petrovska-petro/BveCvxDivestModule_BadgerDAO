import pytest
from brownie import accounts, interface, BveCvxDivestModule


@pytest.fixture
def deployer(accounts):
    return accounts[0]


@pytest.fixture
def governance(accounts):
    return accounts.at("0xA9ed98B5Fb8428d68664f3C5027c62A10d45826b", force=True)


@pytest.fixture
def techops(accounts):
    # https://github.com/Badger-Finance/badger-multisig/blob/main/helpers/addresses.py#L54
    return accounts.at("0x86cbD0ce0c087b482782c181dA8d191De18C8275", force=True)


@pytest.fixture
def treasury(accounts):
    # https://github.com/Badger-Finance/badger-multisig/blob/main/helpers/addresses.py#L60
    return accounts.at("0xD0A7A8B98957b9CD3cFB9c0425AbE44551158e9e", force=True)


@pytest.fixture
def keeper():
    # https://docs.chain.link/docs/chainlink-automation/supported-networks/#registry-and-registrar-addresses
    return accounts.at("0x02777053d6764996e594c3E88AF1D58D5363a2e6", force=True)


@pytest.fixture
def safe():
    # https://github.com/Badger-Finance/badger-multisig/blob/main/helpers/addresses.py#L58
    return interface.IGnosisSafe("0xA9ed98B5Fb8428d68664f3C5027c62A10d45826b")


@pytest.fixture()
def cvx():
    return interface.ERC20("0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B")


@pytest.fixture()
def bvecvx():
    return interface.IBveCvx("0xfd05D3C7fe2924020620A8bE4961bBaA747e6305")


@pytest.fixture()
def usdc():
    return interface.IBveCvx("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture()
def cvx_locker():
    return interface.ICvxLocker("0x72a19342e8F1838460eBFCCEf09F6585e32db86E")


@pytest.fixture
def bvecvx_module(deployer, techops):
    yield BveCvxDivestModule.deploy(techops, {"from": deployer})


# https://docs.pytest.org/en/6.2.x/fixture.html#autouse-fixtures-fixtures-you-don-t-have-to-request
@pytest.fixture(autouse=True)
def config_module(safe, bvecvx_module, bvecvx, governance, techops, keeper):
    # enable module
    safe.enableModule(bvecvx_module.address, {"from": safe})
    assert bvecvx_module.address in safe.getModules()

    # add executors. roles we expect: techops & CL keepers
    bvecvx_module.addExecutor(techops, {"from": governance})
    bvecvx_module.addExecutor(keeper, {"from": governance})

    # ensure `voter` is WL in `bveCVX` otherwise wd will revert
    bvecvx.approveContractAccess(safe, {"from": techops})


@pytest.fixture
def seed_vault(cvx):
    # sends cvx funds to `bveCVX` vault
    CVX_LOCKER = "0x72a19342e8F1838460eBFCCEf09F6585e32db86E"
    BVECVX_VAULT = "0xfd05D3C7fe2924020620A8bE4961bBaA747e6305"
    cvx.transfer(BVECVX_VAULT, 10_000e18, {"from": accounts.at(CVX_LOCKER, force=True)})

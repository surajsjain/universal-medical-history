#setup Alice's ocean instance
import os
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.data_provider.data_service_provider import DataServiceProvider
from ocean_utils.agreements.service_factory import ServiceDescriptor
from ocean_lib.models.btoken import BToken #BToken is ERC20
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_lib.web3_internal.wallet import Wallet

def create_pool(ocean, token_address, alice_wallet):
    pool = ocean.pool.create(
        token_address,
        data_token_amount=100.0,
        OCEAN_amount=10.0,
        from_wallet=alice_wallet
    )

    return pool

def publish_excel(pvt_key, url, dt_name, dt_symbol, dataset_name, username):
    config = {
       'network' : os.getenv('NETWORK_URL'),
       'metadataStoreUri' : os.getenv('AQUARIUS_URL'),
       'providerUri' : os.getenv('PROVIDER_URL'),
    }
    ocean = Ocean(config)

    #Alice's wallet
    alice_wallet = Wallet(ocean.web3, private_key=pvt_key)

    print("create datatoken: begin")
    data_token = ocean.create_data_token(dt_name, dt_symbol, alice_wallet, blob=ocean.config.metadata_store_url)
    token_address = data_token.address
    print("create datatoken: done")
    print(f"token_address = '{token_address}'")

    date_created = "2012-02-01T10:55:11Z"
    service_attributes = {
            "main": {
                "name": "dataAssetAccessServiceAgreement",
                "creator": alice_wallet.address,
                "timeout": 3600 * 24,
                "datePublished": date_created,
                "cost": 1.0, # <don't change, this is obsolete>
            }
        }

    service_endpoint = DataServiceProvider.get_url(ocean.config)
    download_service = ServiceDescriptor.access_service_descriptor(service_attributes, service_endpoint)

    metadata = {
        "main": {
            "type": "dataset",
            "name": dataset_name,
            "author": username,
            "license": "CC0: Public Domain", "dateCreated": date_created,
            "files": [
                {
                    "index": 0,
                    "contentType": "application/vnd.ms-excel",
                    "url": url
                },
            ]
        }
    }

    #ocean.assets.create will encrypt URLs using Provider's encrypt service endpoint, and update asset before putting on-chain.
    #It requires that token_address is a valid DataToken contract address. If that isn't provided, it will create a new token.
    asset = ocean.assets.create(metadata, alice_wallet, service_descriptors=[download_service], data_token_address=token_address)
    assert token_address == asset.data_token_address

    did = asset.did  # did contains the datatoken address
    print(f"did = '{did}'")

    data_token.mint_tokens(alice_wallet.address, 100.0, alice_wallet)

    OCEAN_token = BToken(ocean.OCEAN_address)
    assert OCEAN_token.balanceOf(alice_wallet.address) > 0, "need Rinkeby OCEAN"

    # pool = ocean.pool.create(
    #    token_address,
    #    data_token_amount=100.0,
    #    OCEAN_amount=10.0,
    #    from_wallet=alice_wallet
    # )


    while(True):
        try:
            pool = create_pool(ocean, token_address, alice_wallet)
            break
        except:
            continue

    pool_address = pool.address
    print(f"pool_address = '{pool_address}'")


    config = {
       'network' : os.getenv('NETWORK_URL'),
       'metadataStoreUri' : os.getenv('AQUARIUS_URL'),
       'providerUri' : os.getenv('PROVIDER_URL'),
    }
    market_ocean = Ocean(config)


    asset = market_ocean.assets.resolve(did)
    service1 = asset.get_service(ServiceTypes.ASSET_ACCESS)

    #point to pool
    pool = market_ocean.pool.get(pool_address)

    OCEAN_address = market_ocean.OCEAN_address
    price_in_OCEAN = market_ocean.pool.calcInGivenOut(
        pool_address, OCEAN_address, token_address, token_out_amount=1.0)
    print(f"Price of 1 datatoken is {price_in_OCEAN} OCEAN")

    return did
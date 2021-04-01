#create ocean instance
from ocean_lib.config import Config
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.config_provider import ConfigProvider


def test():
	config = Config('config.ini')
	ocean = Ocean(config)




	ConfigProvider.set_config(config)

	#Alice's wallet
	import os
	from ocean_lib.web3_internal.wallet import Wallet
	alice_wallet = Wallet(ocean.web3, 0x376e05899a4ae00463a3a607c774069b7d6a647860dba723f39b735c91238ddf, None, "EARLYTOBEDANDEARLYTORISE")
	#alice_wallet = Wallet(ocean.web3, private_key=os.getenv('TEST_PRIVATE_KEY1'))

	#Publish a datatoken
	data_token = ocean.create_data_token('DS-token4', 'DST3', alice_wallet, blob=ocean.config.metadata_store_url)
	token_address = data_token.address
	print(f"token address = '{token_address}'")

	#Specify metadata and service attributes, using the Branin test dataset
	date_created = "2019-12-28T10:55:11Z"
	metadata =  {
		"main": {
			"type": "dataset", "name": "RIDDLE", "author": "CODE",
			"license": "CC0: Public Domain", "dateCreated": date_created,
			"files": [{"index": 0, "contentType": "text/text",
				"url": "https://raw.githubusercontent.com/trentmc/branin/master/branin.arff"}]}
	}
	service_attributes = {
			"main": {
				"name": "dataAssetAccessServiceAgreement",
				"creator": alice_wallet.address,
				"timeout": 3600 * 24,
				"datePublished": date_created,
				"cost": 1.0, # <don't change, this is obsolete>
			}
		}
	print(f"wallet  address = '{alice_wallet.address}'")
	#Publish metadata and service attributes on-chain.
	# The service urls will be encrypted before going on-chain.
	# They're only decrypted for datatoken owners upon consume.
	from ocean_lib.data_provider.data_service_provider import DataServiceProvider
	from ocean_utils.agreements.service_factory import ServiceDescriptor

	service_endpoint = DataServiceProvider.get_url(ocean.config)
	download_service = ServiceDescriptor.access_service_descriptor(service_attributes, service_endpoint)
 
	asset = ocean.assets.create(
		metadata,
		alice_wallet,
		service_descriptors=[download_service],
		data_token_address=token_address )
 
	assert token_address == asset.data_token_address
	print(f"token address = '{asset.data_token_address}'")
	print(f"did = '{asset.did}'")
	did = asset.did  # did contains the datatoken address

	#Mint the datatokens
	data_token.mint_tokens(alice_wallet.address, 170.0, alice_wallet)

	#In the create() step below, Alice needs ganache OCEAN. Ensure she has it.
	from ocean_lib.models.btoken import BToken #BToken is ERC20
	OCEAN_token = BToken(ocean.OCEAN_address)
	print(f"wallet address = '{alice_wallet.address}'")
	print(f"balance = '{OCEAN_token.balanceOf(alice_wallet.address)}'")
	assert OCEAN_token.balanceOf(alice_wallet.address) > 149.0, "need OCEAN"

	#Post the asset for sale. This does many blockchain txs: create base
	# pool, bind OCEAN and datatoken, add OCEAN and datatoken liquidity,
	# and finalize the pool.
	pool = ocean.pool.create(
	token_address,
	data_token_amount=20.0,
	OCEAN_amount=2.0,
	from_wallet=alice_wallet
	)
	pool_address = pool.address

	#Print values that we use in the next step
	print(f"token_address = '{token_address}'")
	print(f"did = '{did}'")
	print(f"pool_address = '{pool_address}'")
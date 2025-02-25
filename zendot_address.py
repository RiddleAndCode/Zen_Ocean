from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt

substrate = SubstrateInterface(
    url="wss://westend-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='westend'
)

keypair = Keypair.create_from_mnemonic('abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art')
print(keypair.public_key)
print(keypair.ss58_address)
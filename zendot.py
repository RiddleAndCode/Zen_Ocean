from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt
from substrateinterface.exceptions import SubstrateRequestException

substrate = SubstrateInterface(
    url="wss://westend-rpc.polkadot.io",
    ss58_format=42,
    type_registry_preset='westend'
)

keypair = Keypair.create_from_mnemonic('box change recall shift tent bus mad cherry aerobic engine ocean few')
# keypair = Keypair.create_from_mnemonic('episode together nose spoon dose oil faculty zoo ankle evoke admit walnut')
print(keypair.public_key)


call = substrate.compose_call(
    call_module='Balances',
    call_function='transfer',
    call_params={
        'dest': '5EPCUjPxiHAcNooYipQFWr9NmmXJKpNG5RhcntXwbtUySrgH',
        'value': 0.0001
    }
)

extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

except SubstrateRequestException as e:
    print("Failed to send: {}".format(e))



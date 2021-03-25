from scalecodec.type_registry import load_type_registry_preset
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

# 5CFPcUJgYgWryPaV1aYjSbTpbTLu42V32Ytw1L9rfoMAsfGh
call = substrate.compose_call(
    call_module='Staking',
    call_function='bond',
    call_params={
        'controller': '5EPCUjPxiHAcNooYipQFWr9NmmXJKpNG5RhcntXwbtUySrgH',
        'value': 0.000001,
        'payee': {'Account':'5D5YAyW9o9Y8C39niHLNY623QsvuDtqkaWLDDNgpmYph6zgq'},
    }
)

extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)

try:
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

except SubstrateRequestException as e:
    print("Failed to send: {}".format(e))


keypair = Keypair.create_from_mnemonic('box change recall shift tent bus mad cherry aerobic engine ocean few')
print(keypair.public_key)
print(keypair.ss58_address)

keypair = Keypair.create_from_mnemonic('cash quantum travel innocent cotton link seven inquiry dilemma renew hat space')
print(keypair.public_key)

keypair = Keypair.create_from_mnemonic('abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art')
print(keypair.public_key)
print(keypair.ss58_address)
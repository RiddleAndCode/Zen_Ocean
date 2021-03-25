import lupa
from lupa import LuaRuntime
from zenpolkadot import run_scenario


lua = LuaRuntime(unpack_returned_tuples=True)
lg = lua.globals()
zencode = lua.eval("require('zencode')")
py = lua.eval("require('python')")


lg.zencode = zencode
lua.execute("zencode:begin(1)")

lg.lua_script = '''
Scenario 'polkadot': Westend staking from stash account to controller account 

    Given that controller address is '5EPCUjPxiHAcNooYipQFWr9NmmXJKpNG5RhcntXwbtUySrgH'
    and that wallet password is 'given'
    and that polkadot configuration is 'westend'
    and that the stash address created is 'true'
    and that the stash address is 'funded'
    and that the amount to stake is '0.000002
    Then bond the stake to the controller
    and print the blockhash
'''

lua.execute("zencode:parse(lua_script)")
lua.execute("zencode:run({}, {})")

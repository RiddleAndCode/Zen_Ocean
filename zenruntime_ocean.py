import lupa
from lupa import LuaRuntime
from zenocean import run_scenario

lua = LuaRuntime(unpack_returned_tuples=True)
lg = lua.globals()
zencode = lua.eval("require('zencode')")
py = lua.eval("require('python')")


lg.zencode = zencode
lua.execute("zencode:begin(1)")

lg.lua_script = '''
Scenario 'ocean': Creating ocean data market and staking continous tokens

    Given that wallet address is '0x376e05899a4ae00463a3a607c774069b7d6a647860dba723f39b735c91238ddf'
    and that wallet password is 'given'
    and that ocean configuration is 'given'
    and that the token name is 'Drive&Stake-Token'
    and that the token symbol is 'R3C-DS-T'
    and that the token type is 'dataset'
    and that the license is 'GNU Affero General Public License - AGPL'
    Then create asset token for the data hash '0x12345678912345678'
    and print contract did
'''

lua.execute("zencode:parse(lua_script)")
lua.execute("did = zencode:run({}, {})")
g = lua.globals()

print( " python : " + g.did )

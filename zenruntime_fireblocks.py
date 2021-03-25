import lupa
from lupa import LuaRuntime
from zenfireblocks import run_scenario


lua = LuaRuntime(unpack_returned_tuples=True)
lg = lua.globals()
zencode = lua.eval("require('zencode')")
py = lua.eval("require('python')")

lg.zencode = zencode
lua.execute("zencode:begin(1)")

lg.lua_script = '''
Scenario 'fireblocks': Check whether Fireblocks API is available and connect

    Given that the fireblocks configuration is 'true'
    and that the fireblocks provider is 'sdk token provider'
    When the fireblocks api types imported is 'all'
    Then connect to fireblocks api
'''

lua.execute("zencode:parse(lua_script)")
lua.execute("zencode:run({}, {})")
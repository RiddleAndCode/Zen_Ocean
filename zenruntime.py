import lupa
from lupa import LuaRuntime

result = 'Tom Fuerstner'

lua = LuaRuntime(unpack_returned_tuples=True)
lg = lua.globals()
zencode = lua.eval("require('zencode')")
py = lua.eval("require('python')")
number = py.eval("4+4")
lg.number = number
print(number)
lg.zencode = zencode
lua.execute("zencode:begin(1)")

lg.lua_script = F'''
Scenario 'hello': This is explaining what is going on

    Given that my name is 'Tom' 'Fuerstner'
    and that the result is 'Result'
    Then say hello
    and print all data
'''

lua.execute("zencode:parse(lua_script)")
lua.execute("zencode:run({}, {})")
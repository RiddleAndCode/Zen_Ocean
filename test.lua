require('zencode')
require('python')


zencode:begin(1)

lua_script = 'Scenario \'ocean\': Creating ocean data market and staking continous tokens\n' ..
'Given that wallet address is \'0x376e05899a4ae00463a3a607c774069b7d6a647860dba723f39b735c91238ddf\'\n' ..
'and that wallet password is \'given\'\n' ..
'and that ocean configuration is \'given\'\n' ..
'and that the token name is \'Drive&Stake-Token\'\n' ..
'and that the token symbol is \'R3C-DS-T\'\n' ..
'and that the token type is \'dataset\'\n' ..
'and that the license is \'GNU Affero General Public License - AGPL\'\n' ..
'Then create asset token for the data hash \'976c2eeea33f38a9b7b7aaf3fd1bf237f5cefa433e1e27f1a2f57ccb0680f544\'\n' ..
'and print contract did'

zencode:parse(lua_script)
did = zencode:run({}, {})
print(did)

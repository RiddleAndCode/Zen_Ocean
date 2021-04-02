python = require("python")
python.eval("print('Executing Ocean Smart Contracts from within Zenroom')")

Given("that the wallet address is ''", function(publickey)
    ACK.publickey = publickey
    print(ACK.publickey)
end)
Given("that the wallet password is ''", function(boolean)
    ACK.password_set = boolean -- boolean result
end)
Given("that the ocean configuration is ''", function(boolean)
    ACK.configuration_set = boolean -- boolean result
end)
Given("that the token name is ''", function(name)
    ACK.token_name = name 
end)
Given("that the token symbol is ''", function(symbol)
    ACK.token_symbol = symbol 
end)
Given("that the token type is ''", function(type)
    ACK.token_type = type 
end)
Given("that the license is ''", function(license)
    ACK.license = license
    print(ACK.license)
end)
Given("that the data hash is ''", function(hash)
    ACK.hash = hash
    print(ACK.hash)
end)

Then("create asset token for the data hash ", function(hash)
ACK.hash = hash
print(ACK.hash)
end)

Then("print contract did", function()
    print(ACK.hash)
    --python.eval("print(\"" .. OUT .. "\")") 
    OUT = python.eval( "run_scenario( \"" .. ACK.hash .. "\",\"" .. ACK.token_name .. "\",\"" .. ACK.token_symbol .. "\")" )  
    return OUT
end)

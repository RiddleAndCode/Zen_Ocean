
python = require("python")
python.eval("print('Executing Ocean Smart Contracts from within Zenroom')")


Given("that the wallet is ''", function(publickey)
    ACK.publickey = publickey
end)
Given("that the wallet password is ''", function(boolean)
    ACK.password_set = boolean -- boolean result
end)
Given("that the ocean configuration is ''", function(boolean)
    ACK.configuration_set = boolean -- boolean result
end)
Given("that the token name is ''", function(name)
    ACK.token_name = name 
end)Given("that the token id is ''", function(id)
    ACK.token_id = id 
end)Given("that the token type is ''", function(type)
    ACK.token_type = type 
end)
Given("that the license is ''", function(license)
    ACK.license = license
end)


Then("create asset token", function()
    OUT = "Hello, " .. "! The result is: " .. " Ethereum contract executed, successfully."
end)

Then("print contract did", function()
    print(OUT)
    -- python.eval("print(\"" .. OUT .. "\")") 
    python.eval("run_scenario()")   
end)

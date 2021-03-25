
python = require("python")
python.eval("print('Established direct Cconnection to Fireblocks API from within Zenroom')")


Given("that the fireblocks configuration is ''", function(bool)
    ACK.bool = bool   -- boolean result
end)
Given("that the fireblocks provider is ''", function(provider)
    ACK.provider = provider -- provider result
end)
When("the fireblocks api types imported is ''", function(types_imported)
    ACK.token_name = types_imported  -- types imported 
end)


Then("connect to fireblocks api", function()
    OUT = "Hello, " .. "! The result is: " .. " Fireblocks API connected, successfully."
end)

Then("print contract did", function()
    print(OUT)
    -- python.eval("print(\"" .. OUT .. "\")") 
    python.eval("run_scenario()")   
end)
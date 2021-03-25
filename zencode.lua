-- This file is part of Zenroom (https://zenroom.dyne.org)
--
-- Copyright (C) 2018-2019 Dyne.org foundation
-- designed, written and maintained by Denis Roio <jaromil@dyne.org>
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as
-- published by the Free Software Foundation, either version 3 of the
-- License, or (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
--
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

--- <h1>Zencode language parser</h1>
--
-- Zencode is a <a
-- href="https://en.wikipedia.org/wiki/Domain-specific_language">Domain
-- Specific Language (DSL)</a> made to be understood by humans and
-- inspired by <a
-- href="https://en.wikipedia.org/wiki/Behavior-driven_development">Behavior
-- Driven Development (BDD)</a> and <a
-- href="https://en.wikipedia.org/wiki/Domain-driven_design">Domain
-- Driven Design (DDD)</a>.
--
-- The Zenroom VM is capable of parsing specific scenarios written in
-- Zencode and execute high-level cryptographic operations described
-- in them; this is to facilitate the integration of complex
-- operations in software and the non-literate understanding of what a
-- distributed application does. A generic Zencode looks like this:
--
-- <code>
-- Given that I am known as 'Alice'
--
-- When I create my new keypair
--
-- Then print my data
-- </code>
--
-- This section doesn't provide the documentation on how to write
-- Zencode, but illustrates the internals on how the Zencode parser is
-- made and how it integrates with the Zenroom memory model. It serves
-- as a reference documentation on functions used to write parsers for
-- new Zencode scenarios in Zenroom's Lua.
--
--  @module ZEN
--  @author Denis "Jaromil" Roio
--  @license AGPLv3
--  @copyright Dyne.org foundation 2018-2019

_G['ZEN_traceback'] = ""

local zencode = {
   given_steps = {},
   when_steps = {},
   then_steps = {},
   current_step = nil,
   id = 0,
   matches = {},
   verbosity = 0,
   schemas = {},
   OK = true
}

function sort_ipairs(t)
   local a = {}
   for n in pairs(t) do table.insert(a, n) end
   table.sort(a)
   local i = 0      -- iterator variable
   local iter = function ()   -- iterator function
      i = i + 1
      if a[i] == nil then return nil
      else return a[i], t[a[i]]
      end
   end
   return iter
end

-- TODO slow implementation (was originally in c)
--  http://lua-users.org/wiki/StringTrim
function trim(s)
    return s:match'^()%s*$' and '' or s:match'^%s*(.*%S)'
end

function iscomment(b)
   local x = string.char(b:byte(1))
   if x == '#' then
      return true
   else
       return false
   end
end

function isempty(b)
   if b == nil or b == '' then
       return true
   else
       return false
   end
end

function xxx(n,s)
   if zencode.verbosity >= n then
      print(s)
  end
end

function zencode:begin(verbosity)
    _G['ZEN_traceback'] = ""
    self.verbosity = verbosity
    if verbosity > 0 then
        xxx(2,"Zencode debug verbosity: "..verbosity)
    end
    self.current_step = self.given_steps
    self.OK = true
    return true
end

function zencode:reset()
    self.id = 0
    self.matches = {}
    self.schemas = {}
end

function zencode:step(text)
   if isempty(text) then return true end
   if iscomment(text) then return true end
   -- first word
   local chomp = string.char(text:byte(1,1024))
   local prefix = chomp:match("(%w+)(.+)"):lower()
   local defs -- parse in what phase are we

   if prefix == 'given' then
      self.current_step = self.given_steps
      defs = self.current_step
   elseif prefix == 'when'  then
      self.current_step = self.when_steps
      defs = self.current_step
   elseif prefix == 'then'  then
      self.current_step = self.then_steps
      defs = self.current_step
   elseif prefix == 'and'   then
      defs = self.current_step
   elseif prefix == 'scenario' then
      self.current_step = self.given_steps
      defs = self.current_step
      local scenario = string.match(text, "'(.-)'")
      if scenario ~= "" then
          load_scenario(scenario)
          self:trace("|   Scenario "..scenario)
      end
   else -- defs = nil end
        -- if not defs then
         error("Zencode invalid: "..chomp)
         return false
   end
   for pattern,func in pairs(defs) do
      if (type(func) ~= "function") then
         error("Zencode function missing: "..pattern)
         return false
      end
      -- support simplified notation for arg match
      local pat = string.gsub(pattern,"''","'(.-)'")
      if string.match(text, pat) then
         -- xxx(3,"EXEC: "..pat)
         local args = {} -- handle multiple arguments in same string
         for arg in string.gmatch(text,"'(.-)'") do
            -- xxx(3,"+arg: "..arg)
            arg = string.gsub(arg, ' ', '_') -- NBSP
            table.insert(args,arg)
         end
         self.id = self.id + 1
         table.insert(self.matches,
                      { id = self.id,
                        args = args,
                        source = text,
                        prefix = prefix,
                        regexp = pat,
                        hook = func       })
         -- this is parsing, not execution, hence tracing isn't useful
         -- _G['ZEN_traceback'] = _G['ZEN_traceback']..
         --     "    -> ".. text:gsub("^%s*", "") .. " ("..#args.." args)\n"
      end
   end
end

-- returns an iterator for newline termination
function zencode:newline_iter(text)
   s = trim(text)
   if s:sub(-1)~="\n" then s=s.."\n" end
   return s:gmatch("(.-)\n") -- iterators return functions
end

-- TODO: improve parsing for strings starting with newline, missing scenarios etc.
function zencode:parse(text)
   for line in self:newline_iter(text) do
      self:step(line)
   end
end

function zencode:trace(src)
   -- take current line of zencode
   _G['ZEN_traceback'] = _G['ZEN_traceback']..
      trim(src).."\n"
      -- "    -> ".. src:gsub("^%s*", "") .."\n"
   -- act(src) TODO: print also debug when verbosity is high
end

function zencode:run(data, keys)
   -- xxx(2,"Zencode MATCHES:")
   -- xxx(2,self.matches)
   ACK = {}
   OUT = {}
   for i,x in sort_ipairs(self.matches) do
      if data then IN = data else IN = {} end
      if keys then IN.KEYS = keys else IN.KEYS = {} end
      self:trace("->  "..trim(x.source))
      local ok, err = pcall(x.hook,table.unpack(x.args))
      if not ok then
         self:trace("[!] "..err)
         self:trace("---")
         print(_G['ZEN_traceback'])
         error(trim(x.source))
         -- clean the traceback
         _G['ZEN_traceback'] = ""
      end
   end
   self:trace("--- Zencode execution completed")
   -- if type(OUT) == 'table' then
   --    self:trace("<<< Encoding { OUT } to \"JSON\"")
   --    print(JSON.encode(OUT))
   --    self:trace(">>> Encoding successful")
   -- end
   return OUT
end

function zencode:assert(condition, errmsg)
   if condition then return true end
   self:trace("ERR "..errmsg)
   self.OK = false
end

if _G["load_scenario"] == nil then
    _G["load_scenario"] = function(scenario)
        return require("zencode_"..scenario)
    end
end

_G["Given"] = function(text, fn)
   zencode.given_steps[text] = fn
end
_G["When"] = function(text, fn)
   zencode.when_steps[text] = fn
end
_G["Then"] = function(text, fn)
   zencode.then_steps[text] = fn
end

_G["IN"] = {}
_G["ACK"] = {}
_G["OUT"] = {}

return zencode

-- Castor et eau-de-vie : mise en place (une seule fois) et remise à taille des pièces.
-- Aucune règle n'est automatisée.
local LW, LD = @W@, @D@     -- taille du plan, en unités de plan
local F = 1                 -- facteur plan -> table
local DONE = false

local function notes(o)
  local ok, n = pcall(JSON.decode, o.getGMNotes() or "")
  if ok and type(n) == "table" then return n end
end

local function fit(o, n)
  if not n.w then return end
  local b = o.getBoundsNormalized().size
  if b.x <= 0.001 then return end
  local s = o.getScale()
  local k = n.w * F / b.x
  if n.y3 then o.setScale({s.x * k, s.y * k, s.z * k}) else o.setScale({s.x * k, s.y, s.z * k}) end
end

local function tableInfo()
  local tw, td, top = 90, 60, 1.0
  local ok, t = pcall(function() return Tables.getTableObject() end)
  if ok and t then
    local b = t.getBounds()
    tw, td, top = b.size.x, b.size.z, b.center.y + b.size.y / 2
  end
  return tw, td, top
end

local function layout()
  local tw, td, top = tableInfo()
  F = math.min(tw * 0.97 / LW, td * 0.97 / LD)
  local moved = {}
  for _, o in ipairs(getObjects()) do
    local n = notes(o)
    if n and n.x then
      o.setLock(true)
      o.setRotation({0, 180, n.fz or 0})
      fit(o, n)
      o.setPosition({n.x * F, top + (n.h or 0.5), n.z * F})
      table.insert(moved, {o, n})
    end
  end
  local okH, hands = pcall(function() return Hands.getHands() end)
  if okH and hands then
    for _, h in ipairs(hands) do
      local n = notes(h)
      if n and n.hand then
        h.setPosition({n.x * F, top + 2.5, n.z * F})
        h.setScale({n.hw * F, 5, 4 * F})
        h.setRotation({0, 0, 0})
      end
    end
  end
  Wait.time(function()
    for _, m in ipairs(moved) do
      if not m[1].isDestroyed() and not m[2].lock then m[1].setLock(false) end
    end
    DONE = true
    broadcastToAll("Castor et eau-de-vie : table en place.", {0.9, 0.8, 0.5})
  end, 1.5)
end

local function allLoaded()
  for _, o in ipairs(getObjects()) do
    if o.loading_custom or o.spawning then return false end
  end
  return true
end

function onLoad(state)
  if state and state ~= "" then
    local ok, d = pcall(JSON.decode, state)
    if ok and d and d.done then DONE = true; F = d.F or 1; return end
  end
  Wait.condition(layout, allLoaded, 30, layout)
end

function onSave()
  return JSON.encode({done = DONE, F = F})
end

-- Une pièce qui sort d'un sac ou d'un paquet reprend sa taille.
function onObjectLeaveContainer(container, o)
  local n = notes(o)
  if not (n and n.w) then return end
  Wait.condition(function() if not o.isDestroyed() then fit(o, n) end end,
    function() return o.isDestroyed() or (not o.spawning and not o.loading_custom) end, 10)
end

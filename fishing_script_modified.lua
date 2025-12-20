local vu1 = loadstring(game:HttpGet("https://github.com/Footagesus/WindUI/releases/download/1.6.53/main.lua"))()
local vu2 = game:GetService("ReplicatedStorage")
local vu3 = game:GetService("Players")
local vu4 = vu3.LocalPlayer
local vu5 = game:GetService("HttpService")
game:GetService("RunService")
local vu6 = game:GetService("TeleportService")
local vu7 = game:GetService("Workspace")
game:GetService("Lighting")
game:GetService("VirtualUser")
local vu8 = vu2:WaitForChild("Packages"):WaitForChild("_Index"):WaitForChild("sleitnick_net@0.2.0"):WaitForChild("net")
local vu9 = vu8:WaitForChild("RF/ChargeFishingRod")
local vu10 = vu8:WaitForChild("RF/RequestFishingMinigameStarted")
local vu11 = vu8:WaitForChild("RE/FishingCompleted")
local vu12 = require(vu2:WaitForChild("Shared", 20):WaitForChild("Constants"))
local vu13 = vu3.LocalPlayer:WaitForChild("PlayerGui"):WaitForChild("XP")
local vu14 = game.PlaceId
local vu15 = vu4.Character or vu4.CharacterAdded:Wait()
local vu16 = vu15:WaitForChild("HumanoidRootPart")
local vu17 = vu15:WaitForChild("Humanoid")

-- ==========================================
-- 🎲 FUNGSI RANDOM DELAY (BARU)
-- ==========================================
local function getRandomDelay(min, max)
    return math.random(min * 1000, max * 1000) / 1000
end

vu4.Idled:Connect(function()
    local v18 = game:GetService("VirtualUser")
    v18:Button2Down(Vector2.new(0, 0), workspace.CurrentCamera.CFrame)
    task.wait(1)
    v18:Button2Up(Vector2.new(0, 0), workspace.CurrentCamera.CFrame)
end)
local v19 = next
local v20, v21 = getconnections(game:GetService("Players").LocalPlayer.Idled)
while true do
    local v22
    v21, v22 = v19(v20, v21)
    if v21 == nil then
        break
    end
    if v22.Connection then
        v22.Connection:Disconnect()
    end
end
local v23 = next
local v24, v25 = getconnections(game:GetService("Players").LocalPlayer.Idled)
while true do
    local v26
    v25, v26 = v23(v24, v25)
    if v25 == nil then
        break
    end
    v26:Disable()
end
task.spawn(function()
    if vu13 then
        vu13.Enabled = true
    end
end)
vu3.LocalPlayer.OnTeleport:Connect(function(p27)
    if p27 == Enum.TeleportState.Failed then
        vu6:Teleport(vu14)
    end
end)
task.spawn(function()
    while task.wait(5) do
        if not (vu3.LocalPlayer and vu3.LocalPlayer:IsDescendantOf(game)) then
            vu6:Teleport(vu14)
        end
    end
end)
local v28 = (vu3.LocalPlayer.Character or vu3.LocalPlayer.CharacterAdded:Wait()):WaitForChild("Humanoid")
if not v28:FindFirstChildOfClass("Animator") then
    Instance.new("Animator", v28)
end
local vu29 = vu2:WaitForChild("Shared", 5)
local v30 = vu2:WaitForChild("Modules", 5)
local function vu37(p31)
    if not p31 then
        return nil
    end
    local v32, v33 = pcall(require, p31)
    if v32 then
        return v33
    end
    local v34 = p31:Clone()
    v34.Parent = nil
    local v35, v36 = pcall(require, v34)
    if v35 then
        return v36
    end
    warn("Failed to load module: " .. p31:GetFullName())
    return nil
end
if vu29 then
    if not _G.ItemUtility then
        local v38, v39 = pcall(require, vu29:WaitForChild("ItemUtility", 5))
        if v38 and v39 then
            _G.ItemUtility = v39
        else
            warn("ItemUtility module not found or failed to load.")
        end
    end
    if not _G.ItemStringUtility and v30 then
        local v40, v41 = pcall(require, v30:WaitForChild("ItemStringUtility", 5))
        if v40 and v41 then
            _G.ItemStringUtility = v41
        else
            warn("ItemStringUtility module not found or failed to load.")
        end
    end
    if not _G.Replion then
        pcall(function()
            _G.Replion = require(vu2.Packages.Replion)
        end)
    end
    if not _G.Promise then
        pcall(function()
            _G.Promise = require(vu2.Packages.Promise)
        end)
    end
    if not _G.PromptController then
        pcall(function()
            _G.PromptController = require(vu2.Controllers.PromptController)
        end)
    end
end
local vu42 = {}
local v45, v46 = pcall(function()
    local v43 = vu2:WaitForChild("Controllers", 20)
    local v44 = vu2:WaitForChild("Packages"):WaitForChild("_Index"):WaitForChild("sleitnick_net@0.2.0"):WaitForChild("net", 20)
    if not (v43 and (v44 and vu29)) then
        error("Core game folders not found.")
    end
    vu42.Replion = vu37(vu2.Packages.Replion)
    vu42.ItemUtility = vu37(vu29.ItemUtility)
    vu42.FishingController = vu37(v43.FishingController)
    vu42.EquipToolEvent = v44["RE/EquipToolFromHotbar"]
    vu42.ChargeRodFunc = v44["RF/ChargeFishingRod"]
    vu42.StartMinigameFunc = v44["RF/RequestFishingMinigameStarted"]
    vu42.CompleteFishingEvent = v44["RE/FishingCompleted"]
    vu42.FishCaught = v44["RE/FishCaught"]
end)
if v45 then
    _G.FishingModules = vu42
    print("✓ Global Function Merged Successfully!")
    print("✸ Modules Loaded:", vu42)
    local vu47 = {
        AutoFishingNewMethod = false,
        FishingDelay = 10
    }
    local vu48 = {
        IsFishingNewMethod = false,
        LastFishTime = tick()
    }
    function _G.GetRemote(p49)
        return vu8:FindFirstChild(p49)
    end
    _G.Remotes = {
        EquipTool = _G.GetRemote("RE/EquipToolFromHotbar"),
        ChargeRod = _G.GetRemote("RF/ChargeFishingRod"),
        StartMini = _G.GetRemote("RF/RequestFishingMinigameStarted"),
        FinishFish = _G.GetRemote("RE/FishingCompleted"),
        FishCaught = _G.GetRemote("RE/FishCaught")
    }
    function _G.AutoFishingNewMethod()
        if vu48.IsFishingNewMethod then
            warn("[AutoFishing] Already running")
        else
            task.spawn(function()
                vu48.IsFishingNewMethod = true
                print("[AutoFishing] Started - AeHUB Handle your auto fish.")
                local v50 = false
                for _ = 1, 3 do
                    if pcall(function()
                        if _G.Remotes.EquipTool then
                            _G.Remotes.EquipTool:FireServer(1)
                        end
                    end) then
                        print("[AutoFishing] Rod equipped successfully")
                        v50 = true
                        break
                    end
                    task.wait(0.1)
                end
                if not v50 then
                    warn("[AutoFishing] Failed to equip rod, stopping...")
                    vu47.AutoFishingNewMethod = false
                    vu48.IsFishingNewMethod = false
                    vu1:Notify({
                        Title = "New Method",
                        Content = "Failed to equip rod. Please try again.",
                        Duration = 5,
                        Icon = "ban"
                    })
                    return
                end
                task.wait(0.5)
                local vu51 = tick()
                local vu52 = 0
                local vu53 = 0
                local v54 = 15
                while vu47.AutoFishingNewMethod and vu48.IsFishingNewMethod do
                    local vu55 = false
                    local v59, _ = pcall(function()
                        if not (vu4.Character and vu16) then
                            repeat
                                task.wait(0.01)
                            until vu4.Character and vu4.Character:FindFirstChild("HumanoidRootPart")
                            vu15 = vu4.Character
                            vu16 = vu15:WaitForChild("HumanoidRootPart")
                            vu17 = vu15:WaitForChild("Humanoid")
                        end
                        if _G.Remotes.ChargeRod then
                            local v56, v57 = pcall(function()
                                return _G.Remotes.ChargeRod:InvokeServer(100)
                            end)
                            if not (v56 and v57) then
                                task.wait(0.05)
                                return
                            end
                            task.wait(0.05)
                        end
                        if _G.Remotes.StartMini and not pcall(function()
                            _G.Remotes.StartMini:InvokeServer(1.2854545116425, 1)
                        end) then
                            task.wait(0.05)
                        else
                            local v58 = math.max((vu47.FishingDelay or 0.5) * 0.2, 0.05)
                            task.wait(v58)
                            if _G.Remotes.FinishFish and pcall(function()
                                _G.Remotes.FinishFish:FireServer()
                            end) then
                                vu55 = true
                                vu53 = 0
                                vu48.LastFishTime = tick()
                                vu51 = tick()
                                vu52 = vu52 + 1
                            end
                            task.wait(0.01)
                        end
                    end)
                    if not v59 then
                        local v60 = vu53 + 1
                        if v54 <= v60 then
                            warn("[AutoFishing] Too many errors, performing recovery...")
                            task.wait(3)
                            pcall(function()
                                if _G.Remotes.EquipTool then
                                    _G.Remotes.EquipTool:FireServer(1)
                                end
                            end)
                            task.wait(1)
                            v60 = 0
                            vu51 = tick()
                            vu1:Notify({
                                Title = "Auto Recovery",
                                Content = "Fishing system recovered",
                                Duration = 3,
                                Icon = "info"
                            })
                            vu53 = v60
                        else
                            task.wait(0.2)
                            vu53 = v60
                        end
                    end
                    if tick() - vu51 > 180 then
                        warn("[AutoFishing] No activity for 3 minutes, auto-restarting...")
                        vu48.IsFishingNewMethod = false
                        task.wait(2)
                        if vu47.AutoFishingNewMethod then
                            _G.AutoFishingNewMethod()
                        end
                        break
                    end
                end
                vu48.IsFishingNewMethod = false
                print("[AutoFishing] Stopped after " .. vu52 .. " cycles")
            end)
        end
    end
    _G.tierToRarity = {
        "COMMON",
        "UNCOMMON",
        "RARE",
        "EPIC",
        "LEGENDARY",
        "MYTHIC",
        "SECRET"
    }
    function _G.LoadDatabase()
        local v61, v62, v63 = ipairs({
            "/storage/emulated/0/Delta/Workspace/FULL_ITEM_DATA.json",
            "FULL_ITEM_DATA.json"
        })
        while true do
            local vu64
            v63, vu64 = v61(v62, v63)
            if v63 == nil then
                break
            end
            local v65, vu66 = pcall(function()
                return readfile(vu64)
            end)
            if v65 and vu66 then
                local v67, v68 = pcall(function()
                    return vu5:JSONDecode(vu66)
                end)
                if v67 and v68 then
                    print("[DB] Loaded JSON from path:", vu64)
                    return v68
                end
            end
        end
        warn("[DB] FULL_ITEM_DATA.json not found")
        return nil
    end
    _G.database = _G.LoadDatabase()
    _G.ItemDatabase = {}
    if _G.database and _G.database.Data then
        local v69, v70, v71 = pairs(_G.database.Data)
        while true do
            local v72, v73 = v69(v70, v71)
            if v72 == nil then
                break
            end
            v71 = v72
            if type(v73) == "table" then
                local v74, v75, v76 = pairs(v73)
                while true do
                    local v77, v78 = v74(v75, v76)
                    if v77 == nil then
                        break
                    end
                    v76 = v77
                    if type(v78) == "table" then
                        local v79 = tonumber(v78.Tier) or 0
                        v78.Rarity = v78.Rarity and string.upper(tostring(v78.Rarity)) or (_G.tierToRarity[v79] or "UNKNOWN")
                        if v78.Id then
                            local v80 = tonumber(v78.Id)
                            if v80 then
                                v78.Id = v80
                            end
                        end
                    end
                end
            end
        end
        local v81, v82, v83 = pairs(_G.database.Data)
        while true do
            local v84, v85 = v81(v82, v83)
            if v84 == nil then
                break
            end
            v83 = v84
            if type(v85) == "table" then
                local v86, v87, v88 = pairs(v85)
                while true do
                    local v89, v90 = v86(v87, v88)
                    if v89 == nil then
                        break
                    end
                    v88 = v89
                    if v90 and v90.Id then
                        local v91 = tonumber(v90.Id) or v90.Id
                        local v92 = tonumber(v90.Tier) or 0
                        _G.ItemDatabase[v91] = {
                            Name = v90.Name or tostring(v91),
                            Type = v90.Type or v84,
                            Tier = v92,
                            SellPrice = v90.SellPrice or 0,
                            Weight = v90.Weight or "-",
                            Rarity = v90.Rarity and string.upper(tostring(v90.Rarity)) or (_G.tierToRarity[v92] or "UNKNOWN"),
                            Raw = v90
                        }
                    end
                end
            end
        end
        print("[DATABASE] Item database loaded successfully")
    else
        warn("[DATABASE] Failed to load item database")
    end
    function _G.GetItemInfo(p93)
        local v94 = _G.ItemDatabase[p93]
        if not v94 then
            return {
                Name = "Unknown Item",
                Type = "Unknown",
                Tier = 0,
                SellPrice = 0,
                Weight = "-",
                Rarity = "UNKNOWN"
            }
        end
        v94.Rarity = string.upper(tostring(v94.Rarity or "UNKNOWN"))
        return v94
    end
    
    -- Lanjutan kode yang sama sampai fungsi worker...
    -- (Kode terlalu panjang, saya akan fokus pada bagian yang diubah)
    
    -- ==========================================
    -- 🎲 BLATANT WORKER FUNCTION (MODIFIED)
    -- ==========================================
    local vu160 = {}
    local vu161 = {}
    local vu162 = nil
    local vu163 = Instance.new("BindableEvent")
    local vu164 = false
    local vu165 = {
        AutoFish = false,
        Instant_ChargeDelay = 0.01,
        Instant_SpamCount = 3,
        Instant_WorkerCount = 4,
        Instant_StartDelay = 0.9,
        Instant_CatchTimeout = 0.01,
        Instant_CycleDelay = 0.01,
        Instant_ResetCount = 4.5,
        Instant_ResetPause = 0.01
    }
    
    vu160.Replion = vu42.Replion
    vu160.ItemUtility = vu42.ItemUtility
    vu160.FishingController = vu42.FishingController
    vu160.EquipToolEvent = vu42.EquipToolEvent
    vu160.ChargeRodFunc = vu42.ChargeRodFunc
    vu160.StartMinigameFunc = vu42.StartMinigameFunc
    vu160.CompleteFishingEvent = vu42.CompleteFishingEvent
    
    local vu188 = false
    local vu189 = 0
    local vu190 = 0.3
    local function vu192()
        local v191 = 0
        while vu188 and v191 < 150 do
            if vu190 < tick() - vu189 then
                vu188 = false
                warn("Lock auto-released (stale)")
                break
            end
            v191 = v191 + 1
            task.wait()
        end
        if v191 >= 150 then
            return false
        end
        vu188 = true
        vu189 = tick()
        return true
    end
    local function vu193()
        vu188 = false
        vu189 = 0
    end
    
    -- ==========================================
    -- 🎲 MODIFIED WORKER DENGAN RANDOM DELAY
    -- ==========================================
    local function vu212()
        local vu196 = 0
        while vu165.AutoFish and vu4 do
            local vu197 = vu165.Instant_ResetCount
            if vu195 or vu197 <= vu194 then
                break
            end
            local v209, v210 = pcall(function()
                if not vu192() then
                    return
                end
                if vu197 <= vu194 then
                    vu193()
                    return
                end
                vu194 = vu194 + 1
                vu193()
                local v198 = workspace:GetServerTimeNow()
                
                -- 🎲 RANDOM DELAY REEL: 0.02 - 0.5 seconds
                local randomChargeDelay = getRandomDelay(0.02, 0.5)
                vu160.ChargeRodFunc:InvokeServer(nil, nil, nil, v198)
                task.wait(randomChargeDelay)
                
                -- 🎲 RANDOM DELAY FISHING: 0.5 - 1.5 seconds
                local randomStartDelay = getRandomDelay(0.5, 1.5)
                vu160.StartMinigameFunc:InvokeServer(- 139, 1, v198)
                task.wait(randomStartDelay)
                
                if not vu165.AutoFish or vu195 then
                    return
                end
                local v199 = math.max(0.04, 0.2 / vu165.Instant_SpamCount)
                for v200 = 1, vu165.Instant_SpamCount do
                    local v201 = v200
                    if not vu165.AutoFish or vu195 then
                        break
                    end
                    vu160.CompleteFishingEvent:FireServer()
                    if v201 < vu165.Instant_SpamCount then
                        task.wait(v199)
                    end
                end
                if vu165.AutoFish and not vu195 then
                    local vu202 = false
                    local vu203 = nil
                    local vu204 = true
                    local vu205 = task.delay(vu165.Instant_CatchTimeout, function()
                        vu204 = false
                        if vu203 then
                            pcall(function()
                                vu203:Disconnect()
                            end)
                        end
                    end)
                    vu203 = vu163.Event:Connect(function()
                        if not vu202 then
                            vu202 = true
                            vu204 = false
                            pcall(task.cancel, vu205)
                            if vu203 then
                                pcall(function()
                                    vu203:Disconnect()
                                end)
                            end
                        end
                    end)
                    local vu206 = vu203
                    local v207 = vu204
                    local v208 = 0
                    while not vu202 and (v207 and (v208 < 50 and (vu165.AutoFish and not vu195))) do
                        v208 = v208 + 1
                        task.wait()
                    end
                    if vu206 then
                        pcall(function()
                            vu206:Disconnect()
                        end)
                    end
                    if vu160.FishingController and vu160.FishingController.RequestClientStopFishing then
                        pcall(vu160.FishingController.RequestClientStopFishing, vu160.FishingController, true)
                    end
                    vu196 = 0
                end
            end)
            if not v209 then
                local v211 = vu196 + 1
                warn("Worker error: ", v210)
                if v211 >= 3 then
                    warn("Worker stopped (too many fails)")
                    break
                end
                task.wait(0.5)
                vu196 = v211
            end
            if not vu165.AutoFish then
                break
            end
            task.wait(math.max(vu165.Instant_CycleDelay, 0.05))
        end
    end
    
    print("🎲 Blatant Fishing with Random Delay Loaded!")
    print("📊 Delay Reel: 0.02s - 0.5s (Random)")
    print("📊 Delay Fishing: 0.5s - 1.5s (Random)")
    
else
    warn("FATAL ERROR DURING MODULE LOADING: " .. tostring(v46))
end

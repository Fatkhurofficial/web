-- ==========================================
-- 🎲 AeHUB - BLATANT FISHING (MODIFIED)
-- 🔄 Random Delay Version
-- 📅 Modified: $(date)
-- ==========================================
-- 
-- CHANGELOG:
-- ✅ Added: getRandomDelay() function
-- ✅ Modified: Worker function (vu212) with random delays
-- 🎲 Delay Reel: Random 0.02s - 0.5s
-- 🎲 Delay Fishing: Random 0.5s - 1.5s
-- 
-- ==========================================

-- Paste kode asli di sini, dengan modifikasi:
-- 1. Tambahkan fungsi getRandomDelay setelah baris 200
-- 2. Replace fungsi vu212 dengan versi random

-- INSTRUKSI INSTALASI:
-- 1. Buka file fishing_script_FULL_MODIFIED.lua
-- 2. Copy seluruh kode asli Anda
-- 3. Cari baris "local function vu611" (sekitar baris 230-250)
-- 4. Tambahkan SETELAH fungsi vu611:

local function getRandomDelay(min, max)
    return math.random(min * 1000, max * 1000) / 1000
end

-- 5. Cari fungsi "local function vu212()" (sekitar baris 800-900)
-- 6. Replace dengan kode berikut:

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

-- 7. Save file dan load script ke Roblox
-- 8. Test dengan mengaktifkan "Start Blatant"

print("🎲 Blatant Random Delay Patch Applied!")

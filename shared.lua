AddCSLuaFile()
ENT.Base = "base_nextbot"
ENT.PrintName = "ai_NPC"
ENT.Spawnable = true

-- НАСТРОЙКИ
ENT.Model = "models/props_training/target_medic.mdl"
ENT.StartHealth = 75
ENT.SoundDelay = 10

function ENT:Initialize()
    self:SetModel(self.Model)
    self:SetHealth(self.StartHealth)
    self:SetCollisionGroup(COLLISION_GROUP_NPC)

    self.loco:SetAcceleration(400)
    self.loco:SetDeceleration(400)
    self.loco:SetDesiredSpeed(150)

    self.NextSound = CurTime() + self.SoundDelay
end

function ENT:line(t, f)
    local pos = self:GetPos()
    local ray_x = pos.x
    local ray_y = pos.y
    local ray_z = pos.z
    
    local a1 = math.cos(t) * math.cos(f)
    local a2 = math.cos(f) * math.sin(t)
    local a3 = math.sin(f)
    
    local hit = false
    local dismax = 1000
    local d = 0
    local u = 0

    while not hit and d < dismax do
        ray_x = ray_x + a1 * 1
        ray_y = ray_y + a2 * 1
        ray_z = ray_z + a3 * 1
        d = d + 1
        
        local trace = util.TraceLine({
            start = Vector(ray_x, ray_y, ray_z),
            endpos = Vector(ray_x + a1, ray_y + a2, ray_z + a3),
            filter = self
        })
        
        if trace.Hit then
            hit = true
            local ent = trace.Entity
            
            if IsValid(ent) then
                if ent:IsPlayer() then u = 1
                elseif ent:IsNPC() then u = 2
                elseif ent:IsVehicle() then u = 3
                elseif ent:GetClass() == "prop_physics" then u = 4
                elseif ent:IsWorld() then u = 5
                else u = 6 end
            end
        end
    end
    
    return u, d
end

local neuron1 = {}
local w1 = {}
local neuron21 = {}
local w2 = {}
local neuron22 = {}
local w3 = {}
local neuron23 = {}
local w4 = {}
local neuron3 = {}
local i = 0
local i2 = 0

--while i ~= 3600 do
-- table.insert(w1,math.random(-10,10))
-- table.insert(w2,math.random(-10,10))
-- table.insert(w3,math.random(-10,10))
-- table.insert(w4,math.random(-10,10))
-- i = i + 1
--end
--while i2 ~= 60 do
-- table.insert(neuron21,0)
-- table.insert(neuron22,0)
-- table.insert(neuron23,0)
--end

function ENT:deyctvija()
end

function ENT:G() 
    local players = player.GetAll()
    local closest = nil
    local dist = math.huge

    for _, ply in ipairs(players) do
        if IsValid(ply) then
            local d = self:GetPos():Distance(ply:GetPos())
            if d < dist then
                dist = d
                closest = ply
            end
        end
    end

    return closest
end

function ENT:YYY()
    local ply = self:G()
    if self:GetSkin() == 1 and IsValid(ply) and ply:Health() < 100 then
        -- создаём путь каждый кадр (короткий путь)
        local path = Path("Follow")
        path:SetMinLookAheadDistance(100) -- меньшее значение = быстрее реагирует
        path:SetGoalTolerance(20)
        path:Compute(self, ply:GetPos())

        -- движемся по пути
        while path:IsValid() and IsValid(ply) do
            -- если игрок сильно ушёл, пересчитываем путь
            if self:GetPos():Distance(ply:GetPos()) > 100 then
                path:Compute(self, ply:GetPos())
            end

            path:Update(self)
            self.loco:FaceTowards(ply:GetPos())
            coroutine.yield()
        end
    end
end

function ENT:AttackPlayer()
    local ply = self:G()
    if IsValid(ply) and self:GetPos():Distance(ply:GetPos()) <= 50 then
        if not self.NextAttack or CurTime() >= self.NextAttack then
            if self:GetSkin() == 0 then  
                ply:TakeDamage(1, self, self) 
                self.NextAttack = CurTime() + 0.5
            else  
                ply:SetHealth(math.min(ply:GetMaxHealth(), ply:Health() + 1))
                self.NextAttack = CurTime() + 0.5
            end
        end
    end
end

function ENT:RunBehaviour()
    while true do
        self:AttackPlayer()
        self:YYY()
        coroutine.yield()
    end
end

function ENT:Think()
    if CurTime() >= self.NextSound then
        self:EmitSound("bot/meemstart.wav", 75, 100)
        self.NextSound = CurTime() + self.SoundDelay
    end
end

function ENT:OnKilled(dmginfo)
    local prop = ents.Create("prop_physics_multiplayer")
    if IsValid(prop) then
        prop:SetModel(self:GetModel())
        prop:SetPos(self:GetPos())
        prop:SetAngles(self:GetAngles())
        prop:SetColor(Color(0,255,0))
        prop:Spawn()
        prop:Activate()

        if dmginfo:IsExplosionDamage() then
            prop:SetHealth(1)
            timer.Simple(1, function()
                if IsValid(prop) then
                    prop:Fire("Break", "", 0)
                end
            end)
        end
    end

    self:Remove()
end

SWEP.Spawnable = true
SWEP.AdminOnly = true
SWEP.UseHands = true
SWEP.ViewModel = "models/weapons/c_357.mdl"
SWEP.WorldModel = "models/weapons/w_smg1.mdl"
SWEP.Primary.ClipSize = -1
SWEP.Primary.DefaultClip = -1
SWEP.Primary.Automatic = true
SWEP.Primary.Ammo = "SMG1"
SWEP.AutoSwitchTo = true
SWEP.AutoSwitchFrom = false
SWEP.PrintName = "ai"
SWEP.Slot = 3
SWEP.SlotPos = 2
function SWEP:chel1488()
	self:SetHoldType( "smg" )
end
function SWEP:line(startPos, dir, owner,l)
    local trace = util.TraceLine({
        start = startPos,
        endpos = startPos + dir * 10000,
        filter = owner,
        mask = MASK_SHOT_HULL
    })
    local ply = self:GetOwner()
    local bbb = 0
    if not trace.Hit then 
        return 0
    end
    local ent = trace.Entity
    if ent == game.GetWorld() then
        bbb = ply:GetPos():Distance(trace.HitPos)
    elseif ent:IsValid() then
        bbb = ply:GetPos():Distance(trace.HitPos)
    else
        bbb = 0
    end
    return math.floor(bbb)

end
math.randomseed(os.time())

Atom = {}
Atom.__index = Atom

function Atom.new()
    local self = setmetatable({}, Atom)
    self.w = math.random(-1, 1)
    self.a = 0
    return self
end


kva = {}
for i = 1, 51 do
    kva[i] = {}
    for j = 1, 51 do
        kva[i][j] = Atom.new()
    end
end
inpu = {}
for i2 = 1, 51 do
    inpu[i2] = {}
    for j2 = 1, 51 do
        inpu[i2][j2] = 0
    end
end


function sigma(x1)
    if 1 <= x1 then
        return 1
    else
        return 0
    end
end
lb = {}
function SWEP:learn(RRR, b0, p0)
    local nothing = 0
    for i = 1, 51 do
        for j = 1, 51 do
            if kva[i][j].w > 100 then
                 kva[i][j].w = 100
            elseif kva[i][j].w < -100 then
                   kva[i][j].w = -100
            else
                nothing = 1
            end
        end
    end
end
function SWEP:inter()
    local r = 0
    local d = 0
    local ply = self:GetOwner()
    local ttt = ply:EyePos()
    local x3 = 0
    local y3 = 0
    local z3 = 0
    local hp = ply:Health()
    self.oldhp = ply:GetMaxHealth()
    local maxhp = ply:GetMaxHealth()
    local pos = ply:GetPos()
    local target = nil
    for _, vrag in ipairs(player.GetAll()) do
        if vrag:Nick() == "azalbook333" then
            target = vrag
            break
        end
    end
    local vragpos = target:GetPos()

    local o = 0
    r = 0
    o = 0
    for i2 = 1, 51 do
        for j2 = 1, 51 do
            x3 = math.sin(i2) * math.cos(j2)
            y3 = math.sin(i2) * math.sin(j2)
            z3 = math.cos(i2)
            local ang = ply:EyeAngles()
            local forward = ang:Forward()
            local right = ang:Right()
            local up = ang:Up()
            local dir = forward * x3 + right * y3 + up * z3
            dir:Normalize()
            inpu[i2][j2] = self:line(ttt, dir, ply, 0)
            inpu[51][1] = ply:Health()
            inpu[51][2] = ply:GetMaxHealth()
            inpu[51][3] = pos.x
            inpu[51][4] = pos.y
            inpu[51][5] = pos.z
            inpu[51][6] = target:Health()
            inpu[51][7] = target:GetMaxHealth()
            inpu[51][8] = vragpos.x
            inpu[51][9] = vragpos.y
            inpu[51][10] = vragpos.z
        end
    end
    for i = 1, 51 do
        for j = 1, 51 do
            kva[i][j].a = kva[i][j].w * inpu[i][j]

             if (i + 1) <= 51 and (i - 1) >= 1 and (j + 1) <= 51 and (j - 1) >= 1 then
                kva[i][j].a = kva[i][j].a + sigma((kva[i][j - 1].a + kva[i][j + 1].a + kva[i + 1][j].a + kva[i - 1][j].a) * kva[i][j].w)
                kva[i][j].a = kva[i][j].a + sigma((kva[i + 1][j - 1].a + kva[i - 1][j + 1].a + kva[i + 1][j + 1].a + kva[i - 1][j - 1].a) * kva[i][j].w)
             end

        end
    end

    for i = 1, 51 do
        for j = 1, 51 do
            r = r + kva[i][j].a
        end
    end
    r = math.floor(r)
    print(r)
    r = r % 360
    self.AIAngle = r
    


    o = (hp - self.oldhp)
    if o == 0 then
        o = 10
    end
    table.insert(lb,o)
    local b00 = 0
    for i = 1, #lb do
        b00 = b00 + lb[i]
    end
    b00 = b00 / #lb
    self:learn(o,b00,0)
    self.oldhp = hp
    for i = 1, 51 do
        for j = 1, 51 do
            kva[i][j].a = 0
        end
    end
end
function SWEP:PrimaryAttack()
    
    local ply = self:GetOwner()
    if not IsValid(ply) then return end
    
    self:SetNextPrimaryFire(CurTime() + 0.5)
    
    if SERVER then
        -- Получаем направление взгляда игрока
        local aimVec = ply:GetAimVector()
        local startPos = ply:GetShootPos()
        
        -- Вызываем функцию line напрямую у оружия
        self:line(startPos, aimVec, ply,0)
    end
end
function SWEP:Think()
    if (self.NextAI or 0) > CurTime() then return end
    self.NextAI = CurTime() + 0.1
    self:chel1488()
    self:inter()
    self:learn(0,0,1)
end

hook.Add("StartCommand", "AI_Bot_Control", function(ply, cmd)
    if not ply:IsBot() then return end

    local wep = ply:GetActiveWeapon()
    if not IsValid(wep) then return end
    if wep:GetClass() ~= "weapon_ai" then return end

    if wep.AIAngle then
        cmd:SetViewAngles(Angle(0, wep.AIAngle, 0))
    end

    cmd:SetForwardMove(10000)
end)

function SWEP:ShouldDropOnDie()
    return false
end
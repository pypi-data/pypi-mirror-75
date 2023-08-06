import pymem
import re
import time
import math

def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
    pm = pymem.Pymem('csgo.exe')
    module = pymem.process.module_from_name(pm.process_handle, modname)
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(yes_relative) if relative else "0x{:X}".format(non_relative)

def glowT(clientdll, r, g, b):
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, clientdll).lpBaseOfDll

    GetdwEntityList = get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1)
    dwEntityList = int(GetdwEntityList, 0)
    GetdwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
    dwLocalPlayer = int(GetdwLocalPlayer, 0)
    m_iTeamNum = (0xF4)
    GetdwGlowObjectManager = get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1)
    dwGlowObjectManager = int(GetdwGlowObjectManager, 0)
    m_iGlowIndex = (0xA438)

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2: #Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enabling

def glowCT(clientdll, r, g, b):
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, clientdll).lpBaseOfDll

    GetdwEntityList = get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1)
    dwEntityList = int(GetdwEntityList, 0)
    GetdwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
    dwLocalPlayer = int(GetdwLocalPlayer, 0)
    m_iTeamNum = (0xF4)
    GetdwGlowObjectManager = get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1)
    dwGlowObjectManager = int(GetdwGlowObjectManager, 0)
    m_iGlowIndex = (0xA438)

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 3: #Counter-Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enabling

def glowAll(clientdll, t_r, t_g, t_b, ct_r, ct_g, ct_b):
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, clientdll).lpBaseOfDll

    GetdwEntityList = get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1)
    dwEntityList = int(GetdwEntityList, 0)
    GetdwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
    dwLocalPlayer = int(GetdwLocalPlayer, 0)
    m_iTeamNum = (0xF4)
    GetdwGlowObjectManager = get_sig('client.dll', rb'\xA1....\xA8\x01\x75\x4B', 4, 1)
    dwGlowObjectManager = int(GetdwGlowObjectManager, 0)
    m_iGlowIndex = (0xA438)

    while True:
        glow_manager = pm.read_int(client + dwGlowObjectManager)
        for i in range(1,32):
            entity = pm.read_int(client + dwEntityList + i * 0x10)

            if entity:
                entity_team_id = pm.read_int(entity + m_iTeamNum)
                entity_glow = pm.read_int(entity + m_iGlowIndex)

                if entity_team_id == 2: #Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(t_r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(t_g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(t_b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enabling

                elif entity_team_id == 3: #Counter-Terrorist Glow
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x4, float(ct_r)) #R
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x8, float(ct_g)) #G
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0xC, float(ct_b)) #B
                    pm.write_float(glow_manager + entity_glow * 0x38 + 0x10, float(1)) #A
                    pm.write_int(glow_manager + entity_glow * 0x38 + 0x24, 1) #Enabling

def triggerbot(clientdll):
    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, clientdll).lpBaseOfDll

    GetdwEntityList = get_sig('client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1)
    dwEntityList = int(GetdwEntityList, 0)
    GetdwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
    dwLocalPlayer = int(GetdwLocalPlayer, 0)
    GetdwForceAttack = get_sig('client.dll', rb'\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04', 0, 2)
    dwForceAttack = int(GetdwForceAttack, 0)
    m_iCrosshairId = (0xB3E4)
    m_iTeamNum = (0xF4)
    m_fFlags = (0x104)

    while True:
        localPlayer = pm.read_int(client + dwLocalPlayer)
        crosshairID = pm.read_int(localPlayer + m_iCrosshairId)
        getTeam = pm.read_int(client + dwEntityList + (crosshairID - 1) * 0x10)
        localTeam = pm.read_int(localPlayer + m_iTeamNum)
        crosshairTeam = pm.read_int(getTeam + m_iTeamNum)

        if crosshairID > 0 and crosshairID < 32 and localTeam != crosshairTeam:
            pm.write_int(client + dwForceAttack, 6)

#RCS Functions
def normalizeAngles(viewAngleX, viewAngleY):
    if viewAngleX > 89:
        viewAngleX -= 360
    if viewAngleX < -89:
        viewAngleX += 360
    if viewAngleY > 180:
        viewAngleY -= 360
    if viewAngleY < -180:
        viewAngleY += 360
    return viewAngleX, viewAngleY


def checkangles(x, y):
    if x > 89:
        return False
    elif x < -89:
        return False
    elif y > 360:
        return False
    elif y < -360:
        return False
    else:
        return True


def nanchecker(first, second):
    if math.isnan(first) or math.isnan(second):
        return False
    else:
        return True


def rcs(clientdll):
    GetdwClientState = get_sig('engine.dll', rb'\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0', 0, 1)
    dwClientState = int(GetdwClientState, 0)
    GetdwLocalPlayer = get_sig('client.dll', rb'\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF', 4, 3)
    dwLocalPlayer = int(GetdwLocalPlayer, 0)
    GetdwClientState_ViewAngles = get_sig('engine.dll', rb'\xF3\x0F\x11\x80....\xD9\x46\x04\xD9\x05', 0, 4, False)
    dwClientState_ViewAngles = int(GetdwClientState_ViewAngles, 0)
    m_aimPunchAngle = (0x302C)
    m_iShotsFired = (0xA390)

    pm = pymem.Pymem("csgo.exe")
    client = pymem.process.module_from_name(pm.process_handle, clientdll).lpBaseOfDll
    engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll

    global amount
    oldpunchx = 0.0
    oldpunchy = 0.0
    while True:
        time.sleep(0.01)
        rcslocalplayer = pm.read_int(client + dwLocalPlayer)
        rcsengine = pm.read_int(engine + dwClientState)
        if pm.read_int(rcslocalplayer + m_iShotsFired) > 2:
            rcs_x = pm.read_float(rcsengine + dwClientState_ViewAngles)
            rcs_y = pm.read_float(rcsengine + dwClientState_ViewAngles + 0x4)
            punchx = pm.read_float(rcslocalplayer + m_aimPunchAngle)
            punchy = pm.read_float(rcslocalplayer + m_aimPunchAngle + 0x4)
            newrcsx = rcs_x - (punchx - oldpunchx) * 2
            newrcsy = rcs_y - (punchy - oldpunchy) * 2
            newrcs, newrcy = normalizeAngles(newrcsx, newrcsy)
            oldpunchx = punchx
            oldpunchy = punchy
            if nanchecker(newrcsx, newrcsy) and checkangles(newrcsx, newrcsy):
                pm.write_float(rcsengine + dwClientState_ViewAngles, newrcsx)
                pm.write_float(rcsengine + dwClientState_ViewAngles + 0x4, newrcsy)
        else:
            oldpunchx = 0.0
            oldpunchy = 0.0
            newrcsx = 0.0
            newrcsy = 0.0

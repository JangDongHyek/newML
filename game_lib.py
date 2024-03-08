import globals
import support_lib as sl
import cv2
import numpy as np
import win32gui
import win32con
import win32api
import ctypes
import pyMeow as pm
import lib
import time

def minimap_myPos() :
    p = sl.pixelSearch(globals.map["minimapSize"],globals.my["minimap_pixel"])
    if(p) :
        globals.my["minimap_pos"] = p

def jumpIF() :
    if globals.my["cur_floor"]["move_type"] == "jump" :
        if globals.my["direction"] == "left":
            return globals.my["minimap_pos"][0] < (globals.my["cur_floor"]["rope_xL"] + 15)
        else :
            return globals.my["minimap_pos"][0] > (globals.my["cur_floor"]["rope_xL"] - 15)
    elif globals.my["cur_floor"]["move_type"] == "tel" :
        if globals.my["cur_floor"]["x_dict"] == "left":
            return globals.my["minimap_pos"][0] <= (globals.my["cur_floor"]["rope_xL"] + 3)
        elif  globals.my["cur_floor"]["x_dict"] == "right":
            return globals.my["minimap_pos"][0] >= (globals.my["cur_floor"]["rope_xR"] - 3)

def changeFloor() :
    if (globals.my["cur_floor"]["jump_dict"] == globals.my["direction"]) and globals.my["jump"] and jumpIF():  # 윗점프
        globals.my["jump"] = False

        if globals.my["cur_floor"]["y_dict"] == "up":  # 줄잡고 올라가는
            if globals.my["cur_floor"]["move_type"] == "tel":  # 점프
                sl.hardKey(globals.right, False)
                sl.hardKey(globals.left, False)
                sl.hardKey(globals.up, True)
                time.sleep(0.25)
                sl.hardKey(globals.shift)
                sl.hardKey(globals.up, False)
                time.sleep(0.5)
                if globals.my["minimap_pos"][1] <= globals.my["cur_floor"]["rope_yL"] - 2:
                    a = time.time()
                    while True:
                        time.sleep(0.1)
                        if (globals.my["minimap_pos"][1] <= (globals.my["next_floor"]["low_y"])):
                            break

                        if sl.compareTime(a, 4):
                            sl.hardKey(globals.right, True)
                            time.sleep(0.5)
                            sl.hardKey(globals.alt)
                            time.sleep(0.5)
                            sl.hardKey(globals.right, False)
                            break

                    if globals.my["cur_floor"]["double_xline"] :
                        if globals.my["cur_floor"]["x_dict"] == "left" :
                            globals.my["cur_floor"]["x_dict"] = "right"
                        else :
                            globals.my["cur_floor"]["x_dict"] = "left"

            if globals.my["cur_floor"]["move_type"] == "jump" : #점프
                sl.hardKey(globals.alt)
                sl.hardKey(globals.up, True)
                time.sleep(0.5)
                sl.hardKey(globals.up, False)
                time.sleep(0.5)
                if globals.my["minimap_pos"][1] <= globals.my["cur_floor"]["rope_yL"] - 2:
                    sl.hardKey(globals.up, True)
                    sl.hardKey(globals.right, False)
                    sl.hardKey(globals.left, False)
                    a = time.time()
                    while True:
                        time.sleep(0.1)
                        if (globals.my["minimap_pos"][1] <= (globals.my["next_floor"]["low_y"])):
                            break

                        if sl.compareTime(a, 4):
                            break
                    sl.hardKey(globals.up, False)

                    if globals.my["cur_floor"]["double_yline"]:
                        globals.my["cur_floor"]["y_dict"] = "down"

        else:  # 아랫점프
            sl.hardKey(globals.down, True)
            time.sleep(0.5)
            sl.hardKey(globals.alt)
            sl.hardKey(globals.down, False)
            sl.hardKey(globals.right, False)
            sl.hardKey(globals.left, False)
            time.sleep(1)

            if globals.my["cur_floor"]["double_yline"]:
                globals.my["cur_floor"]["y_dict"] = "up"

def floorJumps(cur_floor) :
    if (globals.my["direction"] == "right") and len(globals.my["cur_floor"]["jumps_R"]):
        for jum in globals.my["cur_floor"]["jumps_R"]:
            if globals.my["minimap_pos"][1] == jum[1] and globals.my["minimap_pos"][0] >= jum[0]:
                sl.hardKey(globals.alt)

    if (globals.my["direction"] == "left") and len(globals.my["cur_floor"]["jumps_L"]):
        for jum in globals.my["cur_floor"]["jumps_L"]:
            if globals.my["minimap_pos"][1] == jum[1] and globals.my["minimap_pos"][0] <= jum[0]:
                sl.hardKey(globals.alt)

def checkPos() :
    try :
        # 좌표에따른 방향 설정 및 점프 초기화
        if globals.my["cur_floor"]["start_x"] + 10 >= globals.my["minimap_pos"][0]:
            globals.my["direction"] = "right"
        if globals.my["cur_floor"]["end_x"] - 10 <= globals.my["minimap_pos"][0]:
            globals.my["direction"] = "left"

        if globals.my["cur_floor"]["jump_dict"] != globals.my["direction"]:
            globals.my["jump"] = True

        # 방향에 따른 이동및 사거리 체크
        if globals.my["direction"] == "left":
            sl.hardKey(globals.right, False)
            sl.hardKey(globals.z, False)
            sl.hardKey(globals.left, True)
            sl.hardKey(globals.z, True)
        elif globals.my["direction"] == "right":
            sl.hardKey(globals.left, False)
            sl.hardKey(globals.z, False)
            sl.hardKey(globals.right, True)
            sl.hardKey(globals.z, True)
    except Exception as e :
        print("E_checkPos")
        print(globals.my["cur_floor"])

def getFloor() :
    for i, m in enumerate(globals.map["floors"]):
        low_y = m["low_y"] - 1
        high_y = m["high_y"] + 1

        if (low_y <= globals.my["minimap_pos"][1] and globals.my["minimap_pos"][1] <= high_y and
                m["search_start_x"] <= globals.my["minimap_pos"][0] and globals.my["minimap_pos"][0] <= m["search_end_x"]):
            floor = m

            if (i + 1) > (len(globals.map["floors"]) - 1):
                next_floor = globals.map["floors"]
            else:
                next_floor = globals.map["floors"][i + 1]

            if globals.my["cur_floor"] != floor:
                globals.my["prev_floor"] = globals.my["cur_floor"]
                globals.my["cur_floor"] = floor
                globals.my["next_floor"] = next_floor

            break

    if globals.map["method"] == "circle" and globals.my["prev_floor"] == globals.map["floors"][len(globals.map["floors"]) - 1]:
        globals.my["cur_floor"] = globals.map["floors"][0]


def findMap(name) :
    for map in globals.maps :
        if name == map["name"] :
            return map

def checkHP() :
    return sl.pixelSearch([500,1050,510,1060],[(190, 190, 190)])

def checkHP() :
    return sl.pixelSearch([500,1050,510,1060],[(190, 190, 190)])
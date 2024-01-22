import globals
import pyautogui
import win32gui
import win32api
import time
import numpy as np
import cv2
import winsound as sd

# def imageTargetRactangle(image,target,targets = []) :
def playBeep() :
    fr = 2000  # range : 37 ~ 32767
    du = 1000  # 1000 ms ==1second
    sd.Beep(fr, du)  # winsound.Beep(frequency, duration)


def offHardKey() :
    arrays = ["right","left","down","up","alt",
              "ctrl","shift","end","pagedown","insert","delete","pageup","n1","n2","a","s","r","z"
              ]
    for key in arrays :
        hardKey(eval("globals.{}".format(key)),False)


def compareTime(value,elapse) :
    if not value :
        return False

    if(time.time() - value >= elapse) :
        return True
    return False

def arrayTargetDelete(array,field,target) :
    for index in range(0, len(array)):
        data = array[index]
        if (data[field] == target):
            del array[index]
            break

def pixelseSerarch(points, pixcels,diff = 1) :
    screen = screenshot().load()

    main = True
    x = points[0]
    y = points[1]

    result = []
    while main:
        if x >= points[2] and y >= points[3]:
            main = False
        if screen[x, y] in pixcels:
            result.append((x, y))
            x += diff
            y += diff
            continue
        if x == points[2]:
            y += 1
            x = points[0]
        x += 1
    return result


def pixelSearch(points, pixcels) :
    screen = screenshot().load()
    start_x = points[0]
    start_y = points[1]
    end_x = points[2]
    end_y = points[3]
    if start_x > 1920:
        start_x = 1900
    if start_x <= 1 :
        start_x = 1

    if end_x > 1920:
        end_x = 1910
    if end_x <= 1 :
        end_x = 1

    if start_y > 1080:
        start_y = 1060
    if start_y <= 1 :
        start_y = 1

    if end_y > 1080:
        end_y = 1070
    if end_y <= 1 :
        end_y = 1


    main = True
    x = start_x
    y = start_y
    try :
        while main:
            if x == end_x and y == end_y:
                main = False
            if screen[x, y] in pixcels:
                return (x, y)

            if x == end_x:
                y += 1
                x = start_x
            x += 1
        return None
    except Exception as e :
        print("pixcel search")
        print(points)

def hardKey(key,bool = None,push = 0.1) :
    if(bool == None or bool == 2) :
        globals.ddl.DD_key(key, 1)
        time.sleep(push)
        globals.ddl.DD_key(key, 2)
    elif (bool == True) :
        globals.ddl.DD_key(key, 1)
    elif(bool == False) :
        globals.ddl.DD_key(key, 2)

def hardClick(point,right = False,time = 0.2) :
    if point :
        x = point[0] + globals.window_x
        y = point[1] + globals.window_y

        pyautogui.moveTo(x, y, duration=time)

    if(right) :
        globals.ddl.DD_btn(4)
        globals.ddl.DD_btn(8)
    else :
        globals.ddl.DD_btn(1)
        globals.ddl.DD_btn(2)

def imageSearch(img,confidence = 0.85,image = None) :
    # 한글이름 이미지 읽게하기
    img_array = np.fromfile(img, np.uint8)
    template = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    if image :
        result = pyautogui.locate(template, image, confidence=confidence)
    else :
        result = pyautogui.locate(template,screenshot(),confidence=confidence)

    return result

def screenshot(name = None,scale = []):
    win32gui.SetForegroundWindow(globals.hwnd)
    x, y, x1, y1 = win32gui.GetClientRect(globals.hwnd)
    x, y = win32gui.ClientToScreen(globals.hwnd, (x, y))
    x1, y1 = win32gui.ClientToScreen(globals.hwnd, (x1 - x, y1 - y))

    if (len(scale)):
        im = pyautogui.screenshot(region=(scale[0], scale[1], scale[2] - scale[0], scale[3] - scale[1]))
    else:
        im = pyautogui.screenshot(region=(x, y, x1, y1))

    if name:
        if ".bmp" in name :
            im.save(name)
        else :
            im.save(name + ".bmp")

    return im


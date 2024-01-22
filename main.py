import time
import init
import game_lib as gl
import support_lib as sl
import thread_lib as tl
import win32api
import globals
import threading
import keyboard

init.Init()
flag = False

# globals.my["game_pixel"] = [(34, 102, 68)] # 혁지션
globals.my["game_pixel"] = [(255, 115, 238)] # 장달프
# globals.map = gl.findMap("와일드보어의 땅")
globals.map = gl.findMap("1호선 4구역")



# thread 활성화
game_myPos = threading.Thread(target=tl.game_myPos)
game_myPos.start()
minimap_myPos = threading.Thread(target=tl.minimap_myPos)
minimap_myPos.start()
checkMonster = threading.Thread(target=tl.checkMonster)
checkMonster.start()
render = threading.Thread(target=tl.render)
render.start()

while True :
    if win32api.GetKeyState(globals.mainKey):
        # 쓰레드 오류시 재실행
        if globals.checkMonsterFlag :
            globals.checkMonsterFlag = False
            checkMonster = threading.Thread(target=tl.checkMonster)
            checkMonster.start()
        if globals.game_myPosFlag :
            globals.game_myPosFlag = False
            game_myPos = threading.Thread(target=tl.game_myPos)
            game_myPos.start()
        if globals.minimap_myPosFlag :
            globals.minimap_myPosFlag = False
            minimap_myPos = threading.Thread(target=tl.minimap_myPos)
            minimap_myPos.start()
        if globals.renderFlag :
            globals.renderFlag = False
            render = threading.Thread(target=tl.render)
            render.start()

        if not flag :
            flag = True

        # 현재 나의 층수 계산
        gl.getFloor()

        # 미니맵 내위치에 따른 방향전환 및 점프 초기화
        gl.checkPos()

        # 미니맵에 점프조건이 되어 층을 바꾸는함수
        gl.changeFloor()

        # 조건 체크후 힐
        if gl.checkHP() :
            sl.hardKey(globals.pagedown)

        # 스킬사용
        for skill in globals.my["skills"] :
            if sl.compareTime(skill["time"],skill["cooldown"]) :
                time.sleep(0.7)
                sl.hardKey(skill["key"])
                time.sleep(0.7)
                skill["time"] = time.time()

        # 몹이 있다면 조건 체크후 공격
        if(globals.monster["pos"]) :
            if(globals.monster["pos"][0] < globals.my["game_pos"][0]) :
                sl.hardKey(globals.right, False)
                sl.hardKey(globals.z, False)
                sl.hardKey(globals.left)
            elif globals.monster["pos"][0] > globals.my["game_pos"][0] :
                sl.hardKey(globals.left, False)
                sl.hardKey(globals.z, False)
                sl.hardKey(globals.right)

            sl.hardKey(globals.ctrl)

        # 몹이 없으면 조건체크후 텔포
        else :
            destination = globals.my["cur_floor"]["end_x"]
            if (globals.my["direction"] == "left"):
                destination = globals.my["cur_floor"]["start_x"]


            jump_x = globals.my["cur_floor"]["rope_xL"]

            if (abs(destination - globals.my["minimap_pos"][0]) >= 40) and sl.compareTime(globals.monster["time"],1.5):
                if globals.my["jump"] == False :
                    sl.hardKey(globals.shift)
                    globals.monster["time"] = time.time()

                else :
                    if globals.my["direction"] == globals.my["cur_floor"]["jump_dict"] :
                        if (abs(jump_x - globals.my["minimap_pos"][0]) >= 40) :
                            sl.hardKey(globals.shift)
                            globals.monster["time"] = time.time()
                    else :
                        sl.hardKey(globals.shift)
                        globals.monster["time"] = time.time()

    else :
        if(flag) :
            sl.offHardKey()
            flag = False
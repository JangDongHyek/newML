import globals
import support_lib as sl
import pyMeow as pm
import time


def checkMonster() :
    try :
        while True :
            p = sl.pixelSearch(globals.my["range"],globals.map["monsters"])
            globals.monster["pos"] = p
            if p :
                globals.monster["time"] = time.time()

    except Exception as e :
        print("checkMonster")
        globals.checkMonsterFlag = True

def game_myPos() :
    try :
        while True :
            p = sl.pixelSearch([100,400,1700,850],globals.my["game_pixel"])
            if p :
                globals.my["game_pos"] = p
                globals.my["range"][0] = p[0] + globals.map["range"][0]
                globals.my["range"][1] = p[1] + globals.map["range"][1]
                globals.my["range"][2] = p[0] + globals.map["range"][2]
                globals.my["range"][3] = p[1] + globals.map["range"][3]

    except Exception as e :
        print("game_myPos")
        globals.game_myPosFlag = True


def minimap_myPos() :
    try :
        while True :
            p = sl.pixelSearch(globals.map["minimapSize"],globals.my["minimap_pixel"])
            if(p) :
                globals.my["minimap_pos"] = p
    except Exception as e :
        print("minimap_myPos")
        globals.minimap_myPosFlag = True

def render() :
    try:
        pm.overlay_init()
        blue = pm.get_color("#0400ff")
        red = pm.get_color("#ff000d")
        green = pm.get_color("#0dff00")
        while pm.overlay_loop():
            pm.begin_drawing()

            # 내 미니맵 좌표
            pm.draw_text("my_minimap_pos x : {} , y : {}".format(globals.my["minimap_pos"][0],globals.my["minimap_pos"][1]),
                         1200 + globals.window_x, 0 + globals.window_y, 25, red)

            # 현재층
            if (globals.my["cur_floor"]):
                pm.draw_text("cur_floor : {}".format(globals.my["cur_floor"]["name"]),
                             1200 + globals.window_x, 25 + globals.window_y, 25, red)

                pm.draw_text("start_x : {}".format(globals.my["minimap_pos"][0] - globals.my["cur_floor"]["start_x"]),
                             1200 + globals.window_x, 50 + globals.window_y, 25, red)

                pm.draw_text("end_x : {}".format(globals.my["cur_floor"]["end_x"] - globals.my["minimap_pos"][0]),
                             1200 + globals.window_x, 75 + globals.window_y, 25, red)

                pm.draw_text("jump : {}".format(globals.my["jump"]),
                             1200 + globals.window_x, 100 + globals.window_y, 25, red)

                pm.draw_text("x_dict : {}".format(globals.my["cur_floor"]["x_dict"]),
                             1200 + globals.window_x, 125 + globals.window_y, 25, red)

                # pm.draw_circle(globals.my["cur_floor"]["rope_xL"] + globals.window_x,
                #                globals.my["cur_floor"]["rope_yL"] + globals.window_y,
                #                5, green)



                # 내스킬 쿨
            for index, skill in enumerate(globals.my["skills"]) :
                pm.draw_text("{} : {}".format(skill["name"],int(skill["cooldown"] - (time.time()- skill["time"]))),
                             800 + globals.window_x, (25 * index) + globals.window_y, 25, red)




            #게임 내 좌표
            if globals.my["game_pos"] :
                # pm.draw_rectangle(globals.my["game_pos"][0] + globals.window_x,
                #                 globals.my["game_pos"][1] + globals.window_y,
                #                 50, 50, green)

                # 사거리
                pm.draw_rectangle_lines(globals.my["range"][0] + globals.window_x,
                                        globals.my["range"][1] + globals.window_y,
                                        globals.my["range"][2] - globals.my["range"][0],
                                        globals.my["range"][3] - globals.my["range"][1],
                                        blue, 3.0)
            #사거리내 몹이있으면
            if globals.monster["pos"]:
                pm.draw_rectangle(globals.monster["pos"][0] + globals.window_x,
                                  globals.monster["pos"][1] + globals.window_y,
                                  50, 50, red)
            pm.end_drawing()
    except Exception as e:
        print("render")
        globals.renderFlag = True
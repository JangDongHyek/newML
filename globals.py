import time
# 기본설정
gameTitle = "MapleStory Worlds-Mapleland (엘나스)"
hwnd = None
ddl = None
window_x = 0
window_y = 0
mainKey = 0x05

# 하드웨어 키값
esc,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12 = 100,101,102,103,104,105,106,107,108,109,110,111,112
q,w,e,r,t,y,u,i,o,p = 301,302,303,304,305,306,307,308,309,310
n1,n2,n3,n4,n5,n6,n7,n8,n9,n0 = 201,202,203,204,205,206,207,208,209,210
a,s,d,f,g,h,j,k,l = 401,402,403,404,405,406,407,408,409
z,x,c,v,b,n,m = 501,502,503,504,505,506,507
up,left,down,right = 709,710,711,712
shift,ctrl,alt,space,enter = 500,600,602,603,313
insert,home,pageup,delete,end,pagedown = 703,704,705,706,707,708

# thread 플래그
game_myPosFlag = False
minimap_myPosFlag = False
renderFlag = False
checkMonsterFlag = False

# 내케릭터에대한 정보
my = {
    "minimap_pixel" : [(255, 255, 136)],
    "minimap_pos" : [0,0],
    "game_pixel" : [],
    "game_pos" : None,
    "jump" : False,
    "range" : [0,0,0,0],
    "direction" : "left",
    "x_direction" : "left",
    "y_direction" : "up",
    "prev_floor" : None,
    "cur_floor" : None,
    "next_floor" : None,

    "skills" : [
        {
            "name": "Inbin",
            "key": insert,
            "cooldown": 200,
            "time": time.time()
        },
        {
            "name" : "bless",
            "key" : home,
            "cooldown" : 150,
            "time" : time.time()
        },
        # {
        #     "name": "Gard",
        #     "key" : pageup,
        #     "cooldown" : 500,
        #     "time" : time.time()
        # },
        {
            "name": "Pet",
            "key": pagedown,
            "cooldown": 600,
            "time": time.time()
        }
    ]
}

# 사냥하고있는맵에 대한 정보
map = None

monster = {
    "pos" : None,
    "time" : time.time()
}



maps = [
    {
        "name": "죽은나무의숲2",
        "map_dict": "right",
        "method": "reverse",
        "minimapSize": [12, 55, 350, 255],
        "range": [-250, -100, +250, +300],
        "monsters": [(222, 239, 206)],  # 와보,스텀프
        "floors": [
            {
                "name": "1",
                "search_start_x": 90,
                "search_end_x": 290,
                "start_x": 73,
                "end_x": 293,
                "low_y": 133,
                "high_y": 178,
                "x_dict": "right",
                "y_dict": "up",
                "jump_dict": "right",
                "double_xline": False,
                "double_yline": False,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 255,
                "rope_yL": 170,
                "rope_xR": 255,
                "rope_yR": 170,
            },
            {
                "name": "2",
                "search_start_x": 160,
                "search_end_x": 270,
                "start_x": 50,
                "end_x": 253,
                "low_y": 110,
                "high_y": 118,
                "x_dict": "right",
                "y_dict": "up",
                "jump_dict": "right",
                "double_xline": False,
                "double_yline": False,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 50,
                "rope_yL": 170,
                "rope_xR": 50,
                "rope_yR": 170,
            },

        ]
    },
    {
        "name" : "1호선 4구역",
        "map_dict" : "left",
        "method" : "reverse",
        "minimapSize" : [12,55,432,218],
        "range" : [-250,-100,+250,+300],
        "monsters" : [(206, 222, 239)],#와보,스텀프
        "floors" : [
            {
                "name": "1-1",
                "search_start_x": 90,
                "search_end_x": 163,
                "start_x": 100,
                "end_x": 153,
                "low_y": 153,
                "high_y": 153,
                "x_dict" : "right",
                "y_dict": "up",
                "jump_dict": "right",
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R" : [],
                "rope_xL": 128,
                "rope_yL": 153,
                "rope_xR": 128,
                "rope_yR": 153,
            },

            {
                "name": "2-1",
                "search_start_x": 90,
                "search_end_x": 163,
                "start_x": 100,
                "end_x": 153,
                "low_y": 138,
                "high_y": 138,
                "x_dict": "right",
                "y_dict": "up",
                "jump_dict": "right",
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 139,
                "rope_yL": 138,
                "rope_xR": 139,
                "rope_yR": 138,
            },

            {
                "name": "3-1",
                "search_start_x": 114,
                "search_end_x": 197,
                "start_x": 124,
                "end_x": 187,
                "low_y": 123,
                "high_y": 123,
                "x_dict": "left",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": True,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 134,
                "rope_yL": 123,
                "rope_xR": 175,
                "rope_yR": 123,
            },

            {
                "name": "4-1",
                "search_start_x": 70,
                "search_end_x": 140,
                "start_x": 80,
                "end_x": 999,
                "low_y": 108,
                "high_y": 108,
                "x_dict": "left",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 0,
                "rope_yL": 0,
                "rope_xR": 0,
                "rope_yR": 0,
            },

            {
                "name": "4-2",
                "search_start_x": 170,
                "search_end_x": 219,
                "start_x": 180,
                "end_x": 999,
                "low_y": 108,
                "high_y": 108,
                "x_dict": "left",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 0,
                "rope_yL": 0,
                "rope_xR": 0,
                "rope_yR": 0,
            },

            {
                "name": "1-2",
                "search_start_x": 254,
                "search_end_x": 337,
                "start_x": 264,
                "end_x": 327,
                "low_y": 153,
                "high_y": 153,
                "x_dict": "left",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 315,
                "rope_yL": 153,
                "rope_xR": 315,
                "rope_yR": 153,
            },

            {
                "name": "2-2",
                "search_start_x": 254,
                "search_end_x": 338,
                "start_x": 264,
                "end_x": 327,
                "low_y": 138,
                "high_y": 138,
                "x_dict": "right",
                "y_dict": "up",
                "jump_dict": "right",
                "double_xline": False,
                "double_yline": False,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 294,
                "rope_yL": 138,
                "rope_xR": 294,
                "rope_yR": 138,
            },

            {
                "name": "4-3",
                "search_start_x": 218,
                "search_end_x": 314,
                "start_x": 0,
                "end_x": 304,
                "low_y": 108,
                "high_y": 108,
                "x_dict": "left",
                "y_dict": "up",
                "jump_dict": None,
                "double_xline": False,
                "double_yline": False,
                "move_type": "tel",
                "jumps_L": [],
                "jumps_R": [],
                "rope_xL": 0,
                "rope_yL": 0,
                "rope_xR": 0,
                "rope_yR": 0,
            },
        ]
    },
    {
        "name" : "와일드보어의 땅",
        "map_dict" : "left",
        "method" : "reverse",
        "minimapSize" : [12,55,360,230],
        "range" : [-450,-100,+450,+200],
        "monsters" : [(198, 146, 148),(137, 122, 88)],#와보,스텀프
        "floors" : [
            {
                "name": "1",
                "search_start_x": 25,
                "search_end_x": 335,
                "start_x": 67,
                "end_x": 312,
                "low_y": 199,
                "high_y": 207,
                "x_dict" : "right",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": False,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R" : [],
                "rope_xL": 270,
                "rope_yL": 199,
                "rope_xR": None,
                "rope_yR": None,
            },

            {
                "name": "2",
                "search_start_x": 130,
                "search_end_x": 280,
                "start_x": 164,
                "end_x": 251,
                "low_y": 181,
                "high_y": 181,
                "x_dict" : "right",
                "y_dict": "up",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": True,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R" : [],
                "rope_xL": 203,
                "rope_yL": 181,
                "rope_xR": None,
                "rope_yR": None,
            },

            {
                "name": "3",
                "search_start_x": 130,
                "search_end_x": 260,
                "start_x": 167,
                "end_x": 233,
                "low_y": 136,
                "high_y": 136,
                "x_dict" : "right",
                "y_dict": "down",
                "jump_dict": "left",
                "double_xline": False,
                "double_yline": False,
                "move_type": "jump",
                "jumps_L": [],
                "jumps_R" : [],
                "rope_xL": 189,
                "rope_yL": 136,
                "rope_xR": None,
                "rope_yR": None,
            },

        ]
    },
]
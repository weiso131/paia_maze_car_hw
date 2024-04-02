
import pickle
import numpy as np
import sys

sys.path.append("C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml")

from geometry.checkGoal import checkGoal



    
class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        self.mapNum = kwargs["game_params"]["map"]
        self.path = "C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml/data/graph"
        self.info = []
        self.turnToGoal = False

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if (scene_info["status"] != "GAME_ALIVE"):
            if (scene_info["status"] == "GAME_PASS"):
                with open(self.path + str(self.mapNum) + ".pickle", 'wb') as f:
                    pickle.dump(self.info, f)
            return "RESET"
        

        L_T_sensor = scene_info["L_T_sensor"]
        L_sensor = scene_info["L_sensor"]
        R_T_sensor = scene_info["R_T_sensor"]
        F_sensor = scene_info["F_sensor"]
        R_sensor = scene_info["R_sensor"]
        goalX = scene_info["end_x"]
        goalY = scene_info["end_y"]
        posX = scene_info["x"]
        posY = scene_info["y"]
        angle = scene_info["angle"]

        if (R_T_sensor < 3.5 or F_sensor < 3.5 or L_T_sensor < 3.5):
            self.control_list["left_PWM"] = -200
            self.control_list["right_PWM"] = 200

        elif (L_T_sensor - R_T_sensor >= 1):
            self.control_list["left_PWM"] = 0
            self.control_list["right_PWM"] = 200
        else:
            self.control_list["right_PWM"] = 0
            self.control_list["left_PWM"] = 200

        cos = np.cos((angle + 90) / 360 * 2 * np.pi)
        sin = np.sin((angle + 90) / 360 * 2 * np.pi)
        vecX = goalX - posX
        vecY = goalY - posY

        if (checkGoal(goalX, goalY, posX, posY, {"L_T_sensor" : L_T_sensor, "L_sensor" : L_sensor, 
                                                 "R_T_sensor" : R_T_sensor, "F_sensor" : F_sensor, 
                                                 "R_sensor" : R_sensor}, angle) or self.turnToGoal):
            print("find goal")
            self.turnToGoal = True
            

            if (cos * vecY - sin * vecX > 5 and cos * vecX + sin * vecY > 0):
                self.control_list["left_PWM"] = -1
                self.control_list["right_PWM"] = 1
            elif (cos * vecY - sin * vecX < -5 and cos * vecX + sin * vecY > 0):
                self.control_list["left_PWM"] = -1
                self.control_list["right_PWM"] = 1
            else:
                self.turnToGoal = False
           
        
            



        self.info.append([[F_sensor, L_T_sensor, R_T_sensor, L_sensor, R_sensor, cos, sin, vecX, vecY], [self.control_list["left_PWM"], self.control_list["right_PWM"]]])
        
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass

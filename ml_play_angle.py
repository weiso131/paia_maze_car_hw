
import pickle
import numpy as np
import sys
from sklearn.tree import DecisionTreeRegressor

sys.path.append("C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml")

from geometry.checkGoal import checkGoal



    
class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        self.mapNum = kwargs["game_params"]["map"]
        self.path = "C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml/model.pickle"
        self.info = []
        self.turnToGoal = False

        with open(self.path, 'rb') as f:
            self.model = pickle.load(f)

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if (scene_info["status"] != "GAME_ALIVE"):
            
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

        

        cos = np.cos((angle + 90) / 360 * 2 * np.pi)
        sin = np.sin((angle + 90) / 360 * 2 * np.pi)
        vecX = goalX - posX
        vecY = goalY - posY

        
           
        
            
        preds = self.model.predict(np.array([[F_sensor, L_T_sensor, R_T_sensor, L_sensor, R_sensor, cos, sin, vecX, vecY]]))
        
        self.control_list["left_PWM"] = preds[0][0]
        self.control_list["right_PWM"] = preds[0][1]


        
        
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass

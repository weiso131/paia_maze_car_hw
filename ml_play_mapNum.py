
import pickle
from sklearn.tree import DecisionTreeRegressor
import numpy as np
class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        self.mapNum = kwargs["game_params"]["map"]
        self.path = "C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml/model_mapNum.pickle"
        self.info = []

        with open(self.path, 'rb') as f:
            self.model = pickle.load(f)

    def update(self, scene_info: dict, *args, **kwargs):
        """
        Generate the command according to the received scene information
        """
        if (scene_info["status"] != "GAME_ALIVE"):
            return "RESET"
        

        L_T_sensor = scene_info["L_T_sensor"]
        R_T_sensor = scene_info["R_T_sensor"]
        F_sensor = scene_info["F_sensor"]
        
        preds = self.model.predict(np.array([[F_sensor, L_T_sensor, R_T_sensor, self.mapNum]]))
        
        self.control_list["left_PWM"] = preds[0][0]
        self.control_list["right_PWM"] = preds[0][1]
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass

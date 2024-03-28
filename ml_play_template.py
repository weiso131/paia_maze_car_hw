
import pickle
class MLPlay:
    def __init__(self, ai_name,*args,**kwargs):
        self.player_no = ai_name
        self.control_list = {"left_PWM" : 0, "right_PWM" : 0}
        self.mapNum = kwargs["game_params"]["map"]
        self.path = "C:/Users/weiso131/Desktop/paia2.4.5/resources/app.asar.unpacked/games/maze_car/ml/data/graph"
        self.info = []

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
        R_T_sensor = scene_info["R_T_sensor"]
        F_sensor = scene_info["F_sensor"]
        
        if (R_T_sensor < 3.5 or F_sensor < 3.5 or L_T_sensor < 3.5):
            self.control_list["left_PWM"] = -200
            self.control_list["right_PWM"] = 200

        elif (L_T_sensor - R_T_sensor >= 1 and (R_T_sensor < 7 or self.mapNum == 8 or self.mapNum == 9)):
            if (self.mapNum == 10):
                self.control_list["left_PWM"] = 30
            else:
                self.control_list["left_PWM"] = 0
            self.control_list["right_PWM"] = 200
        else:
            if (self.mapNum == 10):
                self.control_list["right_PWM"] = 30
            else:
                self.control_list["right_PWM"] = 0
            self.control_list["left_PWM"] = 200
        self.info.append([[F_sensor, L_T_sensor, R_T_sensor, self.mapNum], [self.control_list["left_PWM"], self.control_list["right_PWM"]]])
        
        return self.control_list

    def reset(self):
        """
        Reset the status
        """
        # print("reset ml script")
        pass

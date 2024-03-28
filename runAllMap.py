import os


for i in range(1, 12):
    print(f"第{i}張圖")
    os.system("python -m mlgame -f 120 --one-shot -i ./ml/ml_play_mapNum.py . --game_type PRACTICE --sensor_num 5 --sound off --time_to_play 2500 --map " + str(i))

#PRACTICE
#MAZE
#MOVE_MAZE
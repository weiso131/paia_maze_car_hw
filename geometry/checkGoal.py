import numpy as np

def is_within_limits(goalX, goalY, posX, posY, vecX, vecY, horizonDis, verticalDis):
    # 計算向量 vec（從 pos 到 goal 的向量）
    vecToGoalX = goalX - posX
    vecToGoalY = goalY - posY
    
    # 計算 vecX, vecY 的長度平方
    vecLengthSq = vecX**2 + vecY**2
    
    # 計算 vecToGoal 和 vec 的點積
    dotProduct = vecToGoalX * vecX + vecToGoalY * vecY
    
    # 計算 goal 到 vec 方向上的正射影的距離（水平距離）
    projectionLength = dotProduct / vecLengthSq
    

    
    # 檢查水平距離是否小於 horizonDis
    if abs(projectionLength) > horizonDis:
        
        return False
    
    # 計算 goal 到直線的垂直距離
    verticalDistance = abs(vecX * vecToGoalY - vecY * vecToGoalX) / (vecLengthSq ** 0.5)
    
    # 檢查垂直距離是否小於 verticalDis


    return verticalDistance < verticalDis

def checkGoal(goalX : float, goalY : float , posX : float , posY : float, laserDis : dict, carAngle : float):
    count = 0
    
    checkDict = ["R_sensor", "R_T_sensor", "F_sensor", "L_T_sensor", "L_sensor"]
    for i in range(5):
        
        dis = laserDis.get(checkDict[i])
        angle = carAngle + 90 + -90 + 45 * i
        Cos = np.cos((angle + 90) / 360 * 2 * np.pi)
        Sin = np.sin((angle + 90) / 360 * 2 * np.pi)

        if (is_within_limits(goalX, goalY, posX, posY, Cos, Sin, dis, 10)): 
            count += 1
            if (count == 2): return True
        else:
            count = 0
    
    return False



    
    

checkGoal(12.5, -12.5, 107.506, -112.5, {"R_sensor" : 5.6,
                                          "L_sensor" : 4.7, 
                                          "F_sensor" : 87.6,  "L_T_sensor": -1, "R_T_sensor": -1}, 0)
    
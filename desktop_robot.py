import cv2
from fer.fer import FER
import pybullet as p
import pybullet_data
import time
import sys

try:
    print("1. 正在启动物理引擎...")
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.8)
    p.loadURDF("plane.urdf")
    
    # 加载桌面小机器人 (R2D2)
    robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

    print("2. 正在加载表情识别模型（第一次可能较慢）...")
    detector = FER(mtcnn=True)
    
    print("3. 正在打开摄像头...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 错误：摄像头打不开，可能被其他软件占用了！")
        sys.exit()

    print("4. 一切就绪！按键盘 q 键退出。")

    while True:
        ret, frame = cap.read()
        if not ret: 
            continue
        
        # 识别表情
        result = detector.detect_emotions(frame)
        
        if result:
            # 获取第一个人的情绪字典
            emotions = result[0]["emotions"]
            box = result[0]["box"]
            
            # 设定一个阈值（0.7表示必须有70%的把握是开心，才算开心）
            # 如果你想更难触发，可以改成 0.8
            threshold = 0.65
            
            # 核心过滤逻辑
            if emotions['happy'] > threshold:
                top_emotion = 'happy'
            else:
                top_emotion = max(emotions, key=emotions.get)
                if top_emotion == 'happy' and emotions['happy'] <= threshold:
                    top_emotion = 'neutral'
            
            # 画框和字
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, top_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 机器人动作控制
            if top_emotion == 'happy':
                print("检测到开心！机器人转圈！")
                # 让 R2D2 原地转圈
                p.resetBasePositionAndOrientation(robot_id, [0, 0, 0.5], p.getQuaternionFromEuler([0, 0, time.time()*5]))
            else:
                print(f"当前表情：{top_emotion} -> 机器人待机")
                # 待机姿态
                p.resetBasePositionAndOrientation(robot_id, [0, 0, 0.5], [0, 0, 0, 1])

        # 刷新物理引擎
        p.stepSimulation()
        
        # 显示画面
        cv2.imshow("Desktop Robot Control", frame)
        
        # 按 q 退出
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

except Exception as e:
    print(f"\n❌ 运行崩溃了: {e}")
finally:
    print("正在清理并关闭...")
    if 'cap' in locals() and cap.isOpened(): 
        cap.release()
    cv2.destroyAllWindows()
    p.disconnect()

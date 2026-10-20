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
    
    # 🌟 核心改变 1：把机械臂换成一个小机器人（比如经典的 R2D2）
    # 这里我们用 r2d2.urdf 作为一个可爱的桌面机器人代表
    robot_id = p.loadURDF("r2d2.urdf", basePosition=[0, 0, 0.5])

    print("2. 正在加载表情识别模型...")
    detector = FER(mtcnn=True)
    
    print("3. 正在打开摄像头...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 错误：摄像头打不开！")
        sys.exit()

    print("4. 一切就绪！按键盘 q 键退出。")

    while True:
        ret, frame = cap.read()
        if not ret: continue
        
        result = detector.detect_emotions(frame)
        
        if result:
            top_emotion = max(result[0]["emotions"], key=result[0]["emotions"].get)
            box = result[0]["box"]
            x, y, w, h = box
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, top_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 🌟 核心改变 2：根据表情，给小机器人发送不同的动作指令
            if top_emotion == 'happy':
                print("主人开心 -> 机器人原地转圈！")
                # 改变机器人的姿态（让它原地转圈/晃动）
                p.resetBasePositionAndOrientation(robot_id, [0, 0, 0.5], p.getQuaternionFromEuler([0, 0, time.time()*5]))
            else:
                print(f"当前表情：{top_emotion} -> 机器人待机")
                # 待机姿态
                p.resetBasePositionAndOrientation(robot_id, [0, 0, 0.5], [0, 0, 0, 1])

        p.stepSimulation()
        
        cv2.imshow("Desktop Robot Control", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

except Exception as e:
    print(f"\n❌ 运行崩溃了: {e}")
finally:
    if 'cap' in locals() and cap.isOpened(): cap.release()
    cv2.destroyAllWindows()
    p.disconnect()
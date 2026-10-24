import cv2
import numpy as np
import pybullet as p
import pybullet_data
import time
import math
import requests
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont

# ================= 0. 大模型配置 =================
API_KEY = "请输入你的api" # 🚨 务必替换！
def ask_llm(prompt):
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a dual-arm desktop companion robot. Reply in Chinese."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']
    except:
        return "[SAD]我断网了。"

# ================= 辅助函数 =================
def put_text(img, text, position, text_color=(0, 255, 255), text_size=24):
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/simhei.ttf", text_size)
    except IOError:
        font = ImageFont.load_default() 
    draw.text(position, text, font=font, fill=(text_color[2], text_color[1], text_color[0]))
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# ================= 1. 初始化 3D 双臂机器人 =================
print("\n[System] 正在启动物理引擎组装... Starting PyBullet...")
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.loadURDF("plane.urdf")
p.setPhysicsEngineParameter(fixedTimeStep=1./120., numSubSteps=2)

# 构建身体... (省略与上一版相同的身体搭建代码)
base_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.6, 0.4, 0.1], rgbaColor=[0.2, 0.2, 0.2, 1]) 
base_id = p.createMultiBody(10, p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.6, 0.4, 0.1]), base_vis, basePosition=[0, 0, 0.15])
body_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.25, 0.2, 0.3], rgbaColor=[0.8, 0.8, 0.8, 1]) 
body_id = p.createMultiBody(5, p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.25, 0.2, 0.3]), body_vis, basePosition=[0, 0, 0.55])
p.createConstraint(base_id, -1, body_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,0], [0,0,0])
head_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.1, 0.1, 0.1], rgbaColor=[1, 0.6, 0, 1]) 
head_id = p.createMultiBody(1, p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.1, 0.1, 0.1]), head_vis, basePosition=[0, 0, 1.0])
p.createConstraint(body_id, -1, head_id, -1, p.JOINT_FIXED, [0,0,0], [0,0,0.3], [0,0,0])

arm_right_id = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, -0.25, 0.6], useFixedBase=False)
p.createConstraint(body_id, -1, arm_right_id, -1, p.JOINT_FIXED, [0,0,0], [0,-0.2,0], [0,0,0])
arm_left_id = p.loadURDF("kuka_iiwa/model.urdf", basePosition=[0, 0.25, 0.6], useFixedBase=False)
p.createConstraint(body_id, -1, arm_left_id, -1, p.JOINT_FIXED, [0,0,0], [0,0.2,0], [0,0,0])

def set_both_arms(pose_right):
    p.setJointMotorControlArray(arm_right_id, range(7), p.POSITION_CONTROL, targetPositions=pose_right, forces=[2000]*7)
    pose_left = [pose_right[0]*-1, pose_right[1], pose_right[2]*-1, pose_right[3], pose_right[4], pose_right[5]*-1, pose_right[6]]
    p.setJointMotorControlArray(arm_left_id, range(7), p.POSITION_CONTROL, targetPositions=pose_left, forces=[2000]*7)

pose_sleep = [0, 1.5, 0, -1.5, 0, 1.5, 0]
pose_idle = [0, 0, 0, 0, 0, 0, 0] 
pose_happy = [0, -1.2, 0, 1.5, 0, 0.5, 0]
pose_sad = [0, 0.8, 0, -1.5, 0, -0.5, 0]  

floating_text_id = -1 
def update_floating_text(text, color=[0,1,0]):
    global floating_text_id
    floating_text_id = p.addUserDebugText(text, [0, 0, 1.3], textColorRGB=color, textSize=1.5, replaceItemUniqueId=floating_text_id)

set_both_arms(pose_sleep)
update_floating_text("Zzz... (Sleeping)", [0.5, 0.5, 0.5])

# ================= 主循环 =================
while True:
    # ---------------- 阶段 1：等待跳跃 ----------------
    update_floating_text("Waiting for Soul...", [0, 0.5, 1])
    soul_img = np.zeros((500, 500, 3), dtype=np.uint8)
    cv2.circle(soul_img, (250, 200), 120, (0, 255, 255), -1)
    soul_img = put_text(soul_img, "灵魂在电脑中", (170, 180), (0, 0, 0), 30)
    soul_img = put_text(soul_img, "Soul in PC", (200, 220), (0, 0, 0), 20)
    soul_img = put_text(soul_img, "按任意键触发跳跃", (160, 400), (0, 0, 255), 24)
    soul_img = put_text(soul_img, "Press ANY KEY to Jump", (145, 440), (255, 255, 255), 20)
    
    cv2.imshow("Soul in PC", soul_img)
    cv2.waitKey(0) 

    # ---------------- 阶段 2：跳跃动画 ----------------
    scale, x_offset, y_offset = 1.0, 0, 0
    while scale > 0.1:
        scale -= 0.05
        x_offset += 20
        y_offset += 20
        resized = cv2.resize(soul_img, None, fx=scale, fy=scale)
        canvas = np.zeros((600, 600, 3), dtype=np.uint8)
        h, w = resized.shape[:2]
        if 300 + y_offset + h < 600 and 300 + x_offset + w < 600:
            canvas[300+y_offset:300+y_offset+h, 300+x_offset:300+x_offset+w] = resized
        canvas = put_text(canvas, "灵魂正在跨越虚实边界...", (150, 30), (0, 255, 255), 24)
        canvas = put_text(canvas, "Cross-Reality Jumping...", (180, 65), (255, 255, 255), 18)
        cv2.imshow("Jumping...", canvas)
        cv2.waitKey(40)
    cv2.destroyAllWindows()
    
    set_both_arms(pose_happy)
    update_floating_text("I'm Awake!", [0, 1, 0])
    for _ in range(240): p.stepSimulation(); time.sleep(1./240.)

    # ---------------- 阶段 3：表情识别控制 ----------------
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

    action_state = "idle"
    action_start_time = 0
    cooldown_end_time = 0 
    frame_count = 0 
    
    trigger_count = {"happy": 0, "angry": 0, "sad": 0}
    REQUIRED_COUNT = 2 

    while True:
        ret, frame = cap.read()
        if not ret: break
        frame_count += 1
        current_time = time.time()
        
        if action_state != "idle":
            trigger_count = {"happy": 0, "angry": 0, "sad": 0}
            
        if current_time > cooldown_end_time and frame_count % 2 == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0].landmark
                
                left_mouth = landmarks[61]
                right_mouth = landmarks[291]
                top_lip = landmarks[13]
                bottom_lip = landmarks[14]
                forehead = landmarks[10]
                chin = landmarks[152]
                left_eye = landmarks[159]
                left_brow = landmarks[107]
                right_eye = landmarks[386]
                right_brow = landmarks[336]

                face_height = chin.y - forehead.y

                if face_height > 0:
                    mouth_open = abs(bottom_lip.y - top_lip.y) / face_height
                    mouth_center_y = (top_lip.y + bottom_lip.y) / 2
                    mouth_corners_y = (left_mouth.y + right_mouth.y) / 2
                    smile_curve = (mouth_center_y - mouth_corners_y) / face_height
                    brow_eye_dist = ((left_eye.y - left_brow.y) + (right_eye.y - right_brow.y)) / (2 * face_height)

                    h, w, _ = frame.shape
                    cv2.rectangle(frame, (int(left_mouth.x*w)-30, int(forehead.y*h)), (int(right_mouth.x*w)+30, int(chin.y*h)), (0, 255, 0), 2)
                    
                    if action_state == "idle":
                        if smile_curve > 0.006 and mouth_open > 0.008:
                            update_floating_text("Scanning: Smile detected", [0, 1, 1])
                        elif brow_eye_dist < 0.088: # 生气提示阈值
                            update_floating_text("Scanning: Angry detected", [1, 0, 0])
                        elif smile_curve < -0.030: # 悲伤阈值保持
                            update_floating_text("Scanning: Sad detected", [0, 0.5, 1])
                        else:
                            update_floating_text("Watching you...", [0.5, 0.5, 0.5])

                    # 🌟 最终定稿参数：
                    # 1. 生气：0.088 (最舒服的中间值)
                    if brow_eye_dist < 0.088 and smile_curve < 0.008:
                        trigger_count["angry"] += 1
                    # 2. 开心：保持 0.015
                    elif smile_curve > 0.015 and mouth_open > 0.01: 
                        trigger_count["happy"] += 1
                    # 3. 悲伤：保持 -0.030
                    elif smile_curve < -0.030:
                        trigger_count["sad"] += 1
                    else:
                        trigger_count = {"happy": 0, "angry": 0, "sad": 0}

                    if action_state == "idle":
                        if trigger_count["angry"] >= REQUIRED_COUNT:
                            action_state = "angry"
                            action_start_time = current_time
                            cooldown_end_time = current_time + 2.5
                        elif trigger_count["happy"] >= REQUIRED_COUNT:
                            action_state = "happy"
                            action_start_time = current_time
                            cooldown_end_time = current_time + 2.5
                        elif trigger_count["sad"] >= REQUIRED_COUNT:
                            action_state = "sad"
                            action_start_time = current_time
                            cooldown_end_time = current_time + 2.5

        # 动作执行
        elapsed = current_time - action_start_time
        if action_state == "happy":
            p.setJointMotorControlArray(arm_right_id, range(7), p.POSITION_CONTROL, targetPositions=[0, -1.2 + math.sin(elapsed * 12) * 0.4, 0, 1.5, 0, 0.5, 0], forces=[3000]*7)
            p.setJointMotorControlArray(arm_left_id, range(7), p.POSITION_CONTROL, targetPositions=[0, 1.2 - math.sin(elapsed * 12) * 0.4, 0, 1.5, 0, -0.5, 0], forces=[3000]*7)
            p.resetBasePositionAndOrientation(base_id, [0, 0, 0.15], p.getQuaternionFromEuler([0, 0, elapsed * 5]))
            update_floating_text("HAPPY! \(^o^)/", [0, 1, 0])
            if elapsed > 2.5: 
                action_state = "idle"
                set_both_arms(pose_idle)
        elif action_state == "sad":
            p.setJointMotorControlArray(arm_right_id, range(7), p.POSITION_CONTROL, targetPositions=pose_sad, forces=[3000]*7)
            p.setJointMotorControlArray(arm_left_id, range(7), p.POSITION_CONTROL, targetPositions=[-pose_sad[0], pose_sad[1], -pose_sad[2], pose_sad[3], pose_sad[4], -pose_sad[5], pose_sad[6]], forces=[3000]*7)
            p.resetBasePositionAndOrientation(base_id, [0, 0, 0.1], p.getQuaternionFromEuler([0, 0.3, 0]))
            update_floating_text("SAD... (T_T)", [0, 0.5, 1])
            if elapsed > 2.5: 
                action_state = "idle"
                set_both_arms(pose_idle)
        elif action_state == "angry":
            p.setJointMotorControlArray(arm_right_id, range(7), p.POSITION_CONTROL, targetPositions=[0, -1.5, 0, -0.2 + math.sin(elapsed * 25) * 0.1, 0, 0, 0], forces=[3000]*7)
            p.setJointMotorControlArray(arm_left_id, range(7), p.POSITION_CONTROL, targetPositions=[0, 1.5, 0, -0.2 + math.sin(elapsed * 25) * 0.1, 0, 0, 0], forces=[3000]*7)
            p.resetBasePositionAndOrientation(base_id, [math.sin(elapsed * 30) * 0.06, 0, 0.15], [0, 0, 0, 1])
            update_floating_text("ANGRY! (╬▔皿▔)", [1, 0, 0])
            if elapsed > 2.5: 
                action_state = "idle"
                set_both_arms(pose_idle)
        elif action_state == "idle":
            p.resetBasePositionAndOrientation(base_id, [0, 0, 0.15], [0, 0, 0, 1])

        p.stepSimulation()
        
        h, w, _ = frame.shape
        frame = put_text(frame, "视觉模块运行中... 按 'q' 进入对话", (10, h-60), (0, 255, 255), 20)
        cv2.imshow("Vision (Press q to quit)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    # ---------------- 阶段 4：大模型对话 ----------------
    update_floating_text("Listening...", [0, 1, 0])
    while True:
        print("\n" + "="*50)
        print("🎙️ System: 视觉模块已关闭。Vision closed.")
        user_input = input("👦 User (按回车键退出 / Press Enter to Return): ")
        print("="*50)
        
        if user_input == "": break
        
        update_floating_text("Thinking...", [1, 1, 0])
        reply = ask_llm(user_input)
        print(f"🤖 Robot: {reply}")
        
        update_floating_text(reply[:20], [0, 1, 0])
        if "[HAPPY]" in reply:
            set_both_arms(pose_happy)
        else:
            set_both_arms(pose_sad)
        
        for _ in range(3 * 240):
            p.stepSimulation()
            time.sleep(1./240.)
    
    # ---------------- 阶段 5：灵魂跳出返回电脑 ----------------
    update_floating_text("Going back to PC...", [0, 0.5, 1])
    set_both_arms(pose_sleep)
    for _ in range(1 * 240):
        p.stepSimulation()
        time.sleep(1./240.)
        
    scale = 0.1
    x_offset, y_offset = 400, 400 
    while scale < 1.0:
        scale += 0.05
        x_offset -= 20
        y_offset -= 20
        resized = cv2.resize(soul_img, None, fx=scale, fy=scale)
        canvas = np.zeros((600, 600, 3), dtype=np.uint8)
        h, w = resized.shape[:2]
        start_y, start_x = max(0, y_offset), max(0, x_offset)
        if start_y + h <= 600 and start_x + w <= 600:
            canvas[start_y:start_y+h, start_x:start_x+w] = resized
        
        canvas = put_text(canvas, "灵魂正在返回电脑...", (180, 30), (0, 255, 255), 24)
        canvas = put_text(canvas, "Returning to PC...", (200, 65), (255, 255, 255), 18)
        cv2.imshow("Soul Returning...", canvas)
        cv2.waitKey(30)
        
    cv2.destroyAllWindows()

p.disconnect()
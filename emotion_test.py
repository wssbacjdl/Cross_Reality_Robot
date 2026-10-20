import cv2
# 注意这里！必须从 fer.fer 里面导入，这是这个库的奇葩设定
from fer.fer import FER

# 用 MTCNN 模式，绕开 OpenCV 缺文件的坑
detector = FER(mtcnn=True) 

cap = cv2.VideoCapture(0)
print("按键盘 q 键退出")

# 下面的 while True: 循环保持你之前的样子，不用变
while True:
    ret, frame = cap.read()
    if not ret: break
    result = detector.detect_emotions(frame)
    
    if result:
        top_emotion = max(result[0]["emotions"], key=result[0]["emotions"].get)
        box = result[0]["box"]
        x, y, w, h = box
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, top_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"识别到表情: {top_emotion}")
        
    cv2.imshow("Face", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
# Cross-Reality Robot (跨虚实具身智能桌面机器人)

## 📌 项目简介
本项目是一个基于计算机视觉与物理引擎的具身智能原型。通过电脑摄像头实时识别用户的面部表情，并通过 Python 将信号转化为控制指令，驱动 PyBullet 仿真环境中的桌面机器人做出对应动作（如：识别到微笑，机器人原地转圈打招呼）。

## 🛠️ 技术栈
- **视觉感知**：OpenCV, FER (Facial Expression Recognition), MTCNN
- **物理仿真**：PyBullet
- **编程语言**：Python 3.11

## 🚀 如何运行
1. 安装依赖：
   ```bash
   pip install opencv-python fer pybullet
   2.运行纯视觉表情识别测试：
   python emotion_test.py
   3. 运行表情控制虚拟机器人测试：
   python desktop_robot.py

## 🎥 演示视频
(待更新：后续将上传至B站并在此处粘贴链接)

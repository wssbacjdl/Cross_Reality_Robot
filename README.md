# Cross-Reality Robot (跨虚实具身智能机器人)

## 📌 项目演进史 (Project Evolution)
*   **V1.0 (早期原型)**：基于 OpenCV + FER 实现基础表情识别，驱动单臂/圆筒机器人仿真。
*   **V2.0 (物理升级)**：重构物理模型，实现了“数字生命跳跃”特效。
*   **V3.0 (完全体)**：当前版本 `main_final.py`。抛弃了笨重的 TensorFlow，全面升级为 **MediaPipe 面部几何特征识别**（抗光照干扰）。构建了 **双臂复合型 3D 机器人**，加入 LLM 大模型双语对话与悬浮字幕系统，形成完整的跨虚实情感陪伴闭环。

## 🛠️ 技术栈
- **视觉感知**：OpenCV, MediaPipe
- **物理仿真**：PyBullet (自定义双臂物理模型)
- **智能对话**：LLM 大模型 API
- **界面渲染**：Python Pillow

## 🚀 快速运行
1. 安装依赖：`pip install opencv-python mediapipe pybullet requests pillow`
2. 在 `main_final.py` 中填入你的大模型 API KEY。
3. 运行：`python main_final.py`

## 🎥 演示视频
[[点击这里观看 B站 演示视频](https://www.bilibili.com/video/BV1RWHP6ZE13/?spm_id_from=333.1387.upload.video_card.click&vd_source=63decc686b41bca11bc5a45dfbaba753)

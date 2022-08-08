## 启一个新环境
conda create --name mask_chatpic python=3.8 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/


### 激活环境
conda activate mask_chatpic


### 安装依赖
https://fastapi.tiangolo.com/


pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart


https://pypi.org/project/opencv-python/

import numpy as np
import cv2 as cv

pip install opencv-python

### 开始编码

自动重启，监听html文件本身

uvicorn main:app --host 0.0.0.0 --reload --reload-include "*.html"

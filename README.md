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

### 开始部署

sudo docker run -it lemonhall/synology_downloader bash

	dnf update

	mkdir ~/.venvs
	mkdir ~/.venvs/mask_chatpic
	python3 -m venv ~/.venvs/mask_chatpic
	source ~/.venvs/mask_chatpic/bin/activate

	mkdir mask_chatpic
	cd mask_chatpic/

	sudo dnf install git
	cd ~

	git clone https://github.com/lemonhall/mask_chatpic.git

	pip install fastapi
	pip install "uvicorn[standard]"
	pip install python-multipart
	pip install opencv-python

脚本头部记得
#!/root/.venvs/mask_chatpic/bin/python

### 试试

	sudo docker ps

	sudo docker commit -m "mask_chatpic" -a "lemonhall" cc37478fbf89 lemonhall/mask_chatpic

	sudo docker login

	sudo docker push lemonhall/mask_chatpic

	sudo docker run -it lemonhall/mask_chatpic bash



### 最终的启动参数，记得要重命名一下这个容器哈

	sudo docker run --restart=always --name="mask-chatpic" -d lemonhall/mask_chatpic bash -c 'cd /root/mask_chatpic;source ~/.venvs/mask_chatpic/bin/activate;uvicorn main:app --host ::' 

### 报错
	ImportError: libGL.so.1: cannot open shared object file: No such file or directory

	sudo dnf install mesa-libGL
	sudo docker commit -m "mask_chatpic" -a "lemonhall" edc6a0b410ff lemonhall/mask_chatpic
	sudo docker push lemonhall/mask_chatpic
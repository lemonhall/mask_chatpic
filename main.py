#!/root/.venvs/mask_chatpic/bin/python

from typing import Union
from fastapi import FastAPI,Form,File,UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
import numpy as np
import cv2 as cv
import os

app = FastAPI()

#https://www.techiedelight.com/paste-image-from-clipboard-using-javascript/
#用来测试系统存活性的
@app.get("/", response_class=HTMLResponse)
def root():
	content = ""
	with open('clipboard.html',encoding='utf8') as f:
		content = f.read()
		f.close
	print("from get_clipboard method():")
	#print(content)
	return content


def parse_pic():
	visul_debug = False

	im = cv.imread('clipboard.png')
	imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	#等于说就是，大于36的都给我变成0
	ret, thresh = cv.threshold(imgray, 28, 255, 0)
	#可视化调试开关
	# if visul_debug:
	# 	cv.imshow("gray",imgray)
	# 	cv.waitKey(0)
	# else:
	# 	pass
	#https://wenku.baidu.com/view/872340374731b90d6c85ec3a87c24028915f8531.html
	#https://blog.csdn.net/wzh111wzh/article/details/79162321
	# image-寻找轮廓的图像；

	# mode-轮廓的检索模式：
	#     cv2.RETR_EXTERNAL表示只检测外轮廓
	#     cv2.RETR_LIST检测的轮廓不建立等级关系
	#     cv2.RETR_CCOMP建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
	#     cv2.RETR_TREE建立一个等级树结构的轮廓。

	# method-为轮廓的近似办法：
	#     cv2.CHAIN_APPROX_NONE存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
	#     cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，

	# 例如一个矩形轮廓只需4个点来保存轮廓信息
	#     cv2.CHAIN_APPROX_TC89_L1，CV_CHAIN_APPROX_TC89_KCOS使用teh-Chinl chain 近似算法
	# ————————————————
	# 版权声明：本文为CSDN博主「wzh111wzh」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
	# 原文链接：https://blog.csdn.net/wzh111wzh/article/details/79162321
	contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	#https://blog.csdn.net/Easen_Yu/article/details/89380578
	#绘制为绿色，-1的话就是填充
	# what = cv.drawContours(im, contours, -1, (0,255,0), -1)
	# #可视化调试开关
	# if visul_debug:
	# 	cv.imshow('drawimg',what)
	# 	cv.waitKey(0)
	# else:
	# 	pass

	#给所有在3500~4000面积大小的头像上蓝色来定位头像
	avtars = []
	other_contours=[]
	userName_contours=[]
	#这部分实际上是在定位头像以及对话框
	#头像是使用了面积法去定位的
	#而对话框则使用了扩充图形与原图形的面积比值系数，以及顶点个数两个特征值去筛选
	#同时对话框一开始就排除了头像的正方形
	for cnt in contours:
		area = cv.contourArea(cnt)
		rect = cv.boundingRect(cnt)
		#print(rect)
		rectArea = rect[2] * rect[3]
		#print(rectArea)
		extent = area / rectArea
		hull =cv.convexHull(cnt)
		hullArea = cv.contourArea(hull, False)
		num_of_point = len(cnt)
		if hullArea:
			solidity = area / hullArea
		else:
			solidity = 0
		#print(area)
		if area > 23600 and area < 24000:
		#pc的情况下这个没问题
		#if area > 3500 and area <4000:
			avtars.append(cnt)
			#print("==avtars area==")
		#这一段我不需要了，因为这一次我不需要定位对话框
		# else:
		# 	other_contours.append(cnt)
		# 	if extent > 0.85 and extent < 0.99 and num_of_point>19 and num_of_point<35:
		# 	#if extent > 0.85 and extent < 0.87:
		# 	#if len(cnt) != 20 and extent > 0.9699:
		# 		may_dialogues.append(cnt)
		# 		print(num_of_point)
		# 		print(extent)
		# 		print(solidity)
		# 		print("==dialogues bubbles==")
	# im = cv.imread('clipboard.png')
	# avtars_img = cv.drawContours(im, avtars, -1, (255,0,0), -1)
	# #可视化调试开关
	# if visul_debug:
	# 	cv.imshow('avtars_img====',avtars_img)
	# 	cv.waitKey(0)
	# else:
	# 	pass


	#然后开始遍历所有的头像数组
	for avtar_cnt in avtars:
		x,y,w,h = cv.boundingRect(avtar_cnt)
		#ROI = image[y1:y2, x1:x2]
		#https://stackoverflow.com/questions/9084609/how-to-copy-a-image-region-using-opencv-in-python
		#这是头像的大小
		#roi=im[y:y+h,x:x+w]
		# 	-------------------------------------------
		# |                                         | 
		# |    (x1, y1)                             |
		# |      ------------------------           |
		# |      |                      |           |
		# |      |                      |           | 
		# |      |         ROI          |           |  
		# |      |                      |           |   
		# |      |                      |           |   
		# |      |                      |           |       
		# |      ------------------------           |   
		# |                           (x2, y2)      |    
		# |                                         |             
		# |                                         |             
		# |                                         |             
		# -------------------------------------------
		#====================这一部分是在解析对话者的名字====================
		#这里是规避一个y小于0的错误
		#这里的y不需要减少，因为和头像是平行的
		name_y1 = y + -10
		if name_y1<0:
			name_y1 =0
		#https://stackoverflow.com/questions/14161331/creating-your-own-contour-in-opencv-using-python
		point1 = [x+w+10,name_y1]
		point2 = [x+w+500,name_y1]
		point3 = [x+w+500,name_y1+60]
		point4 = [x+w+10,name_y1+60]
		#roi_name=im[name_y1:y+30,x+w+5:x+220]
		points = np.array([point1, point2, point3, point4])
		#把计算好的username的边缘压入数组去
		userName_contours.append(points)

		# 	-------------------------------------------
		# |                                         | 
		# |    (x1, y1)                             |
		# |      ------------------------           |
		# |      |                      |   用户名   |
		# |      |                      |           | 
		# |      |         头像          |           |  
		# |      |                      |           |   
		# |      |                      |           |   
		# |      |                      |           |       
		# |      ------------------------           |   
		# |                           (x2, y2)      |    
		# |                                         |             
		# |                                         |             
		# |                                         |             
		# -------------------------------------------
		#====================这一部分是在解析对话者的名字====================
		#可视化调试开关是否打开了？
		# if visul_debug:
		# 	cv.imshow('====roi_name ',roi_name)
		# 	cv.waitKey(0)
		# else:
		# 	pass


	im = cv.imread('clipboard.png')
	avtars_img = cv.drawContours(im, avtars, -1, (255,0,0), -1)
	output_img = cv.drawContours(avtars_img, userName_contours, -1, (255,0,0), -1)

	#可视化调试开关
	if visul_debug:
		cv.imshow('output_img====',output_img)
		cv.waitKey(0)
	else:
		pass

	#这一段我不需要了，因为这一次我不需要定位对话框
	# im = cv.imread('clipboard.png')
	# may_dialogues_img = cv.drawContours(im, may_dialogues, -1, (0,0,255), -1)
	# #可视化调试开关
	# if visul_debug:
	# 	cv.imshow('may_dialogues_img====',may_dialogues_img)
	# 	cv.waitKey(0)
	# else:
	# 	pass
	# Image path
	image_path = 'output_img.png'
	cv.imwrite(image_path, output_img)

	return True

#https://fastapi.tiangolo.com/tutorial/request-forms/?h=form
#https://stackoverflow.com/questions/63048825/how-to-upload-file-using-fastapi
#https://fastapi.tiangolo.com/advanced/custom-response/
@app.post("/")
async def set_clipboard(clipboard: UploadFile = File(...)):
	output_img = None
	try:
		#print("I am reading")
		contents = await clipboard.read()
		with open(clipboard.filename, 'wb') as f:
			f.write(contents)
	except Exception:
		return {"message": "There was an error uploading the file"}
	finally:
		await clipboard.close()
		parse_pic()

	return FileResponse('output_img.png')

#uvicorn main:app --host 0.0.0.0 --reload --reload-include "*.html"
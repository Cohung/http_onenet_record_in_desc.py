# -*- coding: utf-8 -*
#!C:\Program Files (x86)\Python27


import codecs
import socket #for sockets
import sys #for exit
import os
import time #数字单位为秒
import json

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
# 初始化client,apikey作为所有请求的默认值
clnt = YunpianClient('f112f4be2850c7951cb8bda154c437d5')

host = 'api.heclouds.com'
port = 80

request_num=0 #全局变量，用于记录扫描次数。不参与具体事务


while True:
		reply="" #作用：存储每次查询记录的初始返回数据。新的扫描开始前需要清空。
		reply_sms="" #作用：存储每次查询短信提示的初始返回数据。新的扫描开始前需要清空。
		rec_id=[] #作用：用来记录所有传感器ID用于后续删除。新的扫描开始前需要清空。
		sms_id=[] #作用：用来记录所有传感器ID用于后续删除。新的扫描开始前需要清空。
		num=0;
		sms_num=0;
		request_num=request_num+1
		print "这是第"+str(request_num)+"次查询！"

		try:
			#create an AF_INET, STREAM socket(TCP)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as msg:
			print 'Failed to create socket.'
			sys.exit();
		#print ("Socket Created")

		try:
			remote_ip = socket.gethostbyname(host)
			
		except socket.gaierror:
			#could not resolve
			print 'Hostname could not be resolved.'
			sys.exit()
			
		#print ('IP address of '+host+' is '+remote_ip)

		#Connect to remote server
		s.connect((remote_ip, port))

		#print ('Socket Connected to '+host+' on IP '+remote_ip)
		#handling errors in python socket programs
		###################以下先读取领用记录信息
		message = "GET /devices?key_words=mydevice HTTP/1.1\r\nHost:api.heclouds.com\r\nAccept:*/*\r\napi-key:X6gNMI=4KPqDDLuHNLR40rS=9nY=\r\nContent-Length:0\r\n\r\n"
		try:
			#Set the whole string
			s.sendall(message.encode("UTF-8"))
			print(message.encode("UTF-8"))
		except socket.error:
			#Send Failed
			print 'Send Failed'
			sys.exit()
			
		#print ('Message send successfully')

		#Now receive data
		# while True:
			# print "in recv"
			# recv_data=s.recv(8192)
			# if not recv_data: break
			# reply+=recv_data
		reply = s.recv(8192) #8192这个缓冲区的大小直接影响到接收数据的完整程度
		#print "out recv"
		###################以下再读取短信记录信息
		message = "GET /devices?key_words=mysmsrec HTTP/1.1\r\nHost:api.heclouds.com\r\nAccept:*/*\r\napi-key:X6gNMI=4KPqDDLuHNLR40rS=9nY=\r\nContent-Length:0\r\n\r\n"
		try:
			#Set the whole string
			s.sendall(message.encode("UTF-8"))
			print(message.encode("UTF-8"))
		except socket.error:
			#Send Failed
			print 'Send Failed'
			sys.exit()
			
		#print ('Message send successfully')

		#Now receive data
		# while True:
			# print "in recv"
			# recv_data=s.recv(8192)
			# if not recv_data: break
			# reply+=recv_data
		reply_sms = s.recv(8192) #8192这个缓冲区的大小直接影响到接收数据的完整程度
		#print "out recv"
		####################以下断开扫描领用记录和短信通知
		s.close()
		
		# f=open("./pre.txt","a") #追加写入
		# f.write(reply_sms.encode('utf-8')) #rec_str是自创的字符串，默认为ascii编码
		# f.close()
		####################以下处理收集到的领用记录数据
		str_num = reply.find('{')
		reply_1 = reply[str_num:] #首先完成将接收到的带HTTP头的返回数据的清理--去除HTTP头		
		
		reply_2 = json.loads(reply_1) #将返回数据转换为python对象

		rec_str = "" #用于存储领用记录。每次扫描开始前需要清空。
		num = reply_2["data"]["total_count"] #num为此次扫描返回的记录数量

		#print reply_2["data"]["total_count"]#此处输出为返回的记录数据条数，用于后续的循环输出
		for rec_num in range(0,num):
			rec_str = rec_str + reply_2["data"]["devices"][rec_num]["desc"] + "\r\n"
			rec_id.append(reply_2["data"]["devices"][rec_num]["id"])			

		f=open("./http_onenet_record_in_desc.txt","a") #追加写入
		f.write(rec_str.encode('utf-8')) #rec_str是自创的字符串，默认为ascii编码
		f.close()
		####################以下处理收集到的短信记录数据
		str_num = reply_sms.find('{')
		reply_1 = reply_sms[str_num:] #首先完成将接收到的带HTTP头的返回数据的清理--去除HTTP头				
		reply_2 = json.loads(reply_1) #将返回数据转换为python对象

		sms_str = "" #用于存储短信发送目标,每条发送目标是一条字符串，作为元素存入列表
		sms_num = reply_2["data"]["total_count"] #num为此次扫描返回的记录数量

		#print reply_2["data"]["total_count"]#此处输出为返回的记录数据条数，用于后续的循环输出
		for rec_num in range(0,sms_num):
			sms_str = sms_str + reply_2["data"]["devices"][rec_num]["desc"] + "\r\n"
			sms_id.append(reply_2["data"]["devices"][rec_num]["id"])			

		f=open("./http_onenet_sms_in_desc.txt","a") #追加写入
		f.write(sms_str.encode('utf-8')) #rec_str是自创的字符串，默认为ascii编码
		f.close()
		
		##########得到所需记录后删除Onenet上的存储##############
		
		print "这次查到了"+str(num)+"条记录,下面开始逐个删除。"
		#print(num)
		message_del_1 = "DELETE /devices/"
		message_del_2 = " HTTP/1.1\r\nHost:api.heclouds.com\r\nAccept:*/*\r\napi-key:X6gNMI=4KPqDDLuHNLR40rS=9nY=\r\nContent-Length:0\r\n\r\n\r\n"


		#注意删除操作时服务器会在执行完毕后自动断开连接，因此每执行一次删除操作，都需要重新连接一次。因此将新建连接的内容包括在循环体内。删除操作所需要的参数是记录ID
		try:
			#create an AF_INET, STREAM socket(TCP)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error as msg:
			print  'Failed to create socket.'
			sys.exit();
			#print ("Socket Created")
			#Connect to remote server
		s.connect((remote_ip, port))
		
		for x in range(0,num):
				
				try:
						#Set the whole string
						s.sendall(message_del_1.encode("UTF-8")+rec_id[x].encode("UTF-8")+message_del_2.encode("UTF-8"))
						#print(message_del_1.encode("UTF-8")+rec_id[x].encode("UTF-8")+message_del_2.encode("UTF-8"))
						#time.sleep(2)
				except socket.error:
						#Send Failed
						print  'Send Failed'
						sys.exit()
				print "删除第"+str(x+1)+"条记录!"
				time.sleep(0.05) #休息50ms
		print "这次查到了"+str(sms_num)+"条短信,下面开始逐个删除。"		
		for x in range(0,sms_num):
				
				try:
						#Set the whole string
						s.sendall(message_del_1.encode("UTF-8")+sms_id[x].encode("UTF-8")+message_del_2.encode("UTF-8"))
						#print(message_del_1.encode("UTF-8")+rec_id[x].encode("UTF-8")+message_del_2.encode("UTF-8"))
						#time.sleep(2)
				except socket.error:
						#Send Failed
						print  'Send Failed'
						sys.exit()
				print "删除第"+str(x+1)+"条短信!"
				time.sleep(0.05) #休息50ms
		s.close() #可以在连接状态下，间歇地发送多条数据删除指令，最后再关闭。
		
		time.sleep(5) #休息15秒钟

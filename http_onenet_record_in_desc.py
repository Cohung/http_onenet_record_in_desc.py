# -*- coding: utf-8 -*
#!C:\Program Files (x86)\Python27


import codecs
import socket #for sockets
import sys #for exit
import os
import time #���ֵ�λΪ��
import json

from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
# ��ʼ��client,apikey��Ϊ���������Ĭ��ֵ
clnt = YunpianClient('f112f4be2850c7951cb8bda154c437d5')

host = 'api.heclouds.com'
port = 80

request_num=0 #ȫ�ֱ��������ڼ�¼ɨ��������������������


while True:
		reply="" #���ã��洢ÿ�β�ѯ��¼�ĳ�ʼ�������ݡ��µ�ɨ�迪ʼǰ��Ҫ��ա�
		reply_sms="" #���ã��洢ÿ�β�ѯ������ʾ�ĳ�ʼ�������ݡ��µ�ɨ�迪ʼǰ��Ҫ��ա�
		rec_id=[] #���ã�������¼���д�����ID���ں���ɾ�����µ�ɨ�迪ʼǰ��Ҫ��ա�
		sms_id=[] #���ã�������¼���д�����ID���ں���ɾ�����µ�ɨ�迪ʼǰ��Ҫ��ա�
		num=0;
		sms_num=0;
		request_num=request_num+1
		print "���ǵ�"+str(request_num)+"�β�ѯ��"

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
		###################�����ȶ�ȡ���ü�¼��Ϣ
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
		reply = s.recv(8192) #8192����������Ĵ�Сֱ��Ӱ�쵽�������ݵ������̶�
		#print "out recv"
		###################�����ٶ�ȡ���ż�¼��Ϣ
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
		reply_sms = s.recv(8192) #8192����������Ĵ�Сֱ��Ӱ�쵽�������ݵ������̶�
		#print "out recv"
		####################���¶Ͽ�ɨ�����ü�¼�Ͷ���֪ͨ
		s.close()
		
		# f=open("./pre.txt","a") #׷��д��
		# f.write(reply_sms.encode('utf-8')) #rec_str���Դ����ַ�����Ĭ��Ϊascii����
		# f.close()
		####################���´����ռ��������ü�¼����
		str_num = reply.find('{')
		reply_1 = reply[str_num:] #������ɽ����յ��Ĵ�HTTPͷ�ķ������ݵ�����--ȥ��HTTPͷ		
		
		reply_2 = json.loads(reply_1) #����������ת��Ϊpython����

		rec_str = "" #���ڴ洢���ü�¼��ÿ��ɨ�迪ʼǰ��Ҫ��ա�
		num = reply_2["data"]["total_count"] #numΪ�˴�ɨ�践�صļ�¼����

		#print reply_2["data"]["total_count"]#�˴����Ϊ���صļ�¼�������������ں�����ѭ�����
		for rec_num in range(0,num):
			rec_str = rec_str + reply_2["data"]["devices"][rec_num]["desc"] + "\r\n"
			rec_id.append(reply_2["data"]["devices"][rec_num]["id"])			

		f=open("./http_onenet_record_in_desc.txt","a") #׷��д��
		f.write(rec_str.encode('utf-8')) #rec_str���Դ����ַ�����Ĭ��Ϊascii����
		f.close()
		####################���´����ռ����Ķ��ż�¼����
		str_num = reply_sms.find('{')
		reply_1 = reply_sms[str_num:] #������ɽ����յ��Ĵ�HTTPͷ�ķ������ݵ�����--ȥ��HTTPͷ				
		reply_2 = json.loads(reply_1) #����������ת��Ϊpython����

		sms_str = "" #���ڴ洢���ŷ���Ŀ��,ÿ������Ŀ����һ���ַ�������ΪԪ�ش����б�
		sms_num = reply_2["data"]["total_count"] #numΪ�˴�ɨ�践�صļ�¼����

		#print reply_2["data"]["total_count"]#�˴����Ϊ���صļ�¼�������������ں�����ѭ�����
		for rec_num in range(0,sms_num):
			sms_str = sms_str + reply_2["data"]["devices"][rec_num]["desc"] + "\r\n"
			sms_id.append(reply_2["data"]["devices"][rec_num]["id"])			

		f=open("./http_onenet_sms_in_desc.txt","a") #׷��д��
		f.write(sms_str.encode('utf-8')) #rec_str���Դ����ַ�����Ĭ��Ϊascii����
		f.close()
		
		##########�õ������¼��ɾ��Onenet�ϵĴ洢##############
		
		print "��β鵽��"+str(num)+"����¼,���濪ʼ���ɾ����"
		#print(num)
		message_del_1 = "DELETE /devices/"
		message_del_2 = " HTTP/1.1\r\nHost:api.heclouds.com\r\nAccept:*/*\r\napi-key:X6gNMI=4KPqDDLuHNLR40rS=9nY=\r\nContent-Length:0\r\n\r\n\r\n"


		#ע��ɾ������ʱ����������ִ����Ϻ��Զ��Ͽ����ӣ����ÿִ��һ��ɾ������������Ҫ��������һ�Ρ���˽��½����ӵ����ݰ�����ѭ�����ڡ�ɾ����������Ҫ�Ĳ����Ǽ�¼ID
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
				print "ɾ����"+str(x+1)+"����¼!"
				time.sleep(0.05) #��Ϣ50ms
		print "��β鵽��"+str(sms_num)+"������,���濪ʼ���ɾ����"		
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
				print "ɾ����"+str(x+1)+"������!"
				time.sleep(0.05) #��Ϣ50ms
		s.close() #����������״̬�£���Ъ�ط��Ͷ�������ɾ��ָ�����ٹرա�
		
		time.sleep(5) #��Ϣ15����

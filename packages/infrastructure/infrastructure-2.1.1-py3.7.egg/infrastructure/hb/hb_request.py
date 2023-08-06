# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-06-10 14:43:59
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-07-23 16:51:00
import os
from infrastructure.http_agent.http_request import HttpRequest
from infrastructure.variables.hb_conf import JAVA_COV

class HBRequest(object):
	def __init__(self,coverageLog=""):
		self.coverageLog = coverageLog

	def logs(self,operationType="",message="",typeInfo="",remark=""):
		record = self.coverageLog(data=
					{
						"operationType": operationType,
						"message": message,
						"typeInfo": typeInfo,
						"remark": remark,
						"status":1
					})					
		record.is_valid(raise_exception=True)
		record.save()

	def ticketGit(self,team,service_name,cookie,user_agent):
		"""
			申请git权限
		"""
		url = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		data = {
			"template":100002740,
			"application_args":{
				"username":"maoyongfan10020",
				"projects":{
					"team":{
						"value":team,
						"label":team
					},
					"name":service_name,
					"access":{
						"value":30,
						"label":"开发"
					}
				}
			}
		}

		headers = {'content-type': "application/json;charset=UTF-8",
			'cookie': cookie,
			'User-Agent': user_agent}

		response = HttpRequest.post(url,headers=headers,data=data)
		if response['code'] == 201:

			if self.coverageLog:
				self.logs(operationType="成功申请权限",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

		else:
			if self.coverageLog:
				self.logs(operationType="申请权限失败",
					message=str(response),
					typeInfo="申请git权限",
					remark="")

			raise Exception("等待git审批")

			

	def openServerAuth(self,server,token,cookie,user_agent):
		"""
		先获取服务器挂载app,再去请求开通权限
		"""
		addECSUserURL = "https://ticket-inner.hellobike.cn/api/v1/work/workorder"
		appsTemp = ""
		if server.apps:
			appsTemp = server.apps
		else:
			searchDetail = self.searchEcsDetail(server,token,cookie,user_agent)
			if not searchDetail:
				# 获取服务器详细信息失败，无法开通服务访问权限
				raise Exception("获取服务器详细信息失败，无法开通服务访问权限")
			else:			 
				for app in searchDetail['apps']:
					appsTemp += app["app__name"]+","
				if appsTemp[-1] == ",":
					appsTemp = appsTemp[:-1]
				server.apps = appsTemp
				server.save()

		data = {
			"template":100004103,
			"application_args":
				{"ip":"{}".format(server.ip.intranet),
				"team_name":"{}".format(server.team),
				"name":"{}".format(server.name),
				"env":"{}".format(server.env),
				"apps":"{}".format(appsTemp)}
		}

		headers = {'token': token,
			#'cookie': cookie,
			'User-Agent': user_agent}	

		response = HttpRequest.post(addECSUserURL,headers=headers,data=data)
		if response['code'] == 201:
			if self.coverageLog:
				self.logs(operationType="申请服务器权限成功",
					message=str(response),
					typeInfo="申请服务器权限成功",
					remark="")
			return True
		else:
			if self.coverageLog:
				self.logs(operationType="申请服务器权限时失败",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="")
			raise Exception("无法开通服务器访问权限")		

	def searchEcsDetail(self,server,token,cookie,user_agent):
		searchEcsDetailURL = "http://10.111.90.230:20001/api/v1/ecs/{}/".format(server.server_id)
		# print (self.searchEcsDetailURL)
		response = HttpRequest.get(searchEcsDetailURL,headers={'token': token,
			#'cookie': cookie,
			'User-Agent': user_agent})
		if response['code'] == 200:
			detailData = response['result']['data']
			return detailData
		else:
			if self.coverageLog:
				self.logs(operationType="获取服务器挂载app信息失败,请分析",
					message=str(response),
					typeInfo="申请服务器权限失败",
					remark="获取该{}服务器 {} 挂载app信息,失败"
					.format(server.name,server.env))

			return False


	def getGitTag(self,alreadyRecord,helloBikeToken,user_agent):
		releaseRecordUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(
			service_name=alreadyRecord.service_name)
		data = {
				"page":1,
				"page_size":20,
				"search":alreadyRecord.commit,
				"action":"tt.code.deploy.tags.filter"
				}
		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(releaseRecordUrl,headers=headers,data=data)

		if response['status']:
			git_tag = response['result'].get("data",[])[0].get("name","")
			branch = response['result'].get("data",[])[0].get("branch","")
			alreadyRecord.git_tag = git_tag
			alreadyRecord.branch = branch
			alreadyRecord.save()
			self.get_zip_url(alreadyRecord,helloBikeToken,user_agent)
			return git_tag
		else:
			raise Exception("获取版本对应标签异常")

	def get_zip_url(self,alreadyRecord,helloBikeToken,user_agent):
		"""
			从atls获取编译后class zip包下载地址
		"""
		zipUrl = "https://tt-inner.hellobike.cn/v1/api/{service_name}".format(
			service_name=alreadyRecord.service_name)
		data = {
			"lang":"java",
			"env":"PRO",
			"expires":3600,
			"name":alreadyRecord.git_tag,
			"action":"tt.code.deploy.tags.download"
			}
		headers = {'content-type': "application/json;charset=UTF-8",
			'token': helloBikeToken,
			'user-Agent': user_agent}

		response = HttpRequest.post(zipUrl,headers=headers,data=data)

		if response['status']:

			zip_url = response['result'].get("data",{}).get("url","")

			alreadyRecord.zip_url = zip_url
			alreadyRecord.save()
			return zip_url
		else:
			raise Exception("获取编译后class Zip包下载地址异常")




	def isK8s(self,alreadyRecord,ip,helloBikeToken,user_agent):
		"""
			判断cmdb ip是否能搜索到该IP
		"""
		searchIpUrl = "http://10.111.90.230:20001/api/v1/ip/?search={ip}".format(ip=ip)

		headers = {'content-type': "application/json;charset=UTF-8",
					'token': helloBikeToken,
					'user-Agent': user_agent}

		response = HttpRequest.get(searchIpUrl,headers=headers)
		if self.coverageLog:
			self.logs(operationType="{ip}机器".format(ip=ip),
						message=str(response),
						typeInfo="判断是否是容器",
						remark="")

		if response['status']:
			if response['result']['count'] == 0:
				alreadyRecord.is_container = True
				alreadyRecord.save()
				return True
			else:
				return False
		else:
			raise Exception("判断是否是容器发布异常")

	def downClassZip(self,alreadyRecord):
		"""
		下载atls提供的编译后class zip包
		"jarDir": "/home/maoyongfan10020/jc/{service_name}"
		"/home/maoyongfan10020/jc/{service_name}/{service_name}.zip" 下载的zip包
		"""
		jarDir = JAVA_COV["jarDir"].format(
				service_name=alreadyRecord.service_name)
		os.makedirs(jarDir) if not os.path.exists(jarDir) else True

		zipPath = JAVA_COV["jarDir"].format(
				service_name=alreadyRecord.service_name)+"/{service_name}.zip".format(
				service_name=alreadyRecord.service_name)
		self.checkZip(zipPath)
		response = HttpRequest.download(alreadyRecord.zip_url,zipPath)
		return True
		# if not response:
		# 	self.logs(operationType="下载编译后class_zip包",
		# 			message="失败",
		# 			typeInfo="下载atls包",
		# 			remark="")
		# 	return False
		# else:
		# 	self.logs(operationType="下载编译后class_zip包",
		# 			message="成功",
		# 			typeInfo="下载atls包",
		# 			remark="")
		# 	return True

	def checkZip(self,zipPath):
		"""
			删除旧atls下载zip包
		"""
		if os.path.exists(zipPath):
			command = "rm -rf {zipPath}".format(zipPath = zipPath)
			os.popen(command).read()

			self.logs(operationType="删除旧的编译后zip包",
				message=command,
				typeInfo="删除atls旧zip包",
				remark="")



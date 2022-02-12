# -*- coding: utf-8 -*-
import scrapy
import os
import requests
import json
import time

class ToScrapeCSSSpider(scrapy.Spider):
	name = "zju-cst"
	start_urls = [
		'http://www.cst.zju.edu.cn/36216/list.htm',
	]

	# 自定义函数第一个参数more是当前scrapy爬虫自带的相关信息
	def myprint(self, name, msg):
		print("===")
		print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + " " + name + " : " + msg)
		print("===\n")
	

	def parse(self, response):
		msg = ''
		lastRecord = ''
		# 获取上一次的最新记录
		if os.path.exists('./record.json'):
			with open("./record.json",'r') as f:
				record = json.load(f)
				lastRecord = record["lastRecord"]
				print(lastRecord)
				print(type(lastRecord))
				print(type("aaa"))
				self.myprint("lastRecord", lastRecord)

		for item in response.css('span.lm_new_zk')[::-1]:
			# 倒序遍历
			# item为相对链接 href="/2022/0124/c36216a2477281/page.htm"
			relative_url = item.css('a::attr(href)').get()
			if relative_url > lastRecord:
				title = item.css('a::text').get()
				url = response.urljoin(relative_url)
				if msg:
					msg += "\n\n---\n\n"
				
				msg += title + "\n" + url
				lastRecord = relative_url
		self.myprint("msg", msg)

		newRecode = {"lastRecord": lastRecord}

		with open("./record.json",'w') as f:
			# 不存在则创建
			json.dump(newRecode, f)

		if msg == '':
			return

		msg = "教务信息:\n" + msg
		data = {
			"at": {
				"atMobiles":[
					"15279768436"
				],
			},
			"text": {
				"content": msg + "\n\n @15279768436"
			},
			"msgtype":"text"
		}
		header = {
			"Content-Type": "application/json",
			"Charset": "UTF-8"
		}
		send_data = json.dumps(data)  # 将字典类型数据转化为json格式
		# 添加钉钉机器人的推送URL
		url = ''
		req = requests.post(url, data=send_data, headers=header)
		self.myprint('send_to_dingtalk.result', req.text)

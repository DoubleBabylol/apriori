#! -*- coding: utf-8 -*-
import numpy as np
class Apriori:
	def __init__(self, min_support, min_confidence):
		self.min_support = min_support  # 最小支持度
		self.min_confidence = min_confidence  # 最小置信度
	def count(self):
		self.total = 0  # 数据总行数
		items = {}  # 字典统计
		with open ('retail.txt') as f:
			for l in f:
				self.total += 1
				for i in l.strip ().split (' '):  # 隔开
					if i in items:
						items[i] += 1
					else:
						items[i] = 1
		# 统计完成频率  #self.items存储 筛选过的数字
		self.items = {i: j / self.total for i, j in items.items () if j / self.total > self.min_support}
		self.item2id = {j: i for i, j in enumerate (self.items)}
		# print(self.item2id)  #统计出频次高于最小支持度的数字
		self.D = np.zeros ((self.total, len (self.item2id)))
		with open ('retail.txt')as f:  # 建立布尔矩阵 存储字典中的值为真   行  列为数字所在值
			for i, l in enumerate (f):
				for k in l.strip ().split (' '):
					if k in self.items:
						self.D[i][self.item2id[k]] = 1
	# print(self.total)
	# print(items)#16949
	def build(self):
		self.count ()
		rule = [{(i,): j for i, j in self.items.items ()}] #元组
		l = 0  # 当前步的频繁项的物品数
		while rule[-1]:
			rule.append ({})
			keys = sorted (rule[-2].keys ())  # 对每个k频繁项按字典序排序（核心）加了一个空所以从倒数第二个开始排序
			num = len (rule[-2])
			l += 1
			for i in range (num):  # 遍历每个k频繁项对
				for j in range (i + 1, num):
					if keys[i][:l-1]==keys[j][:l-1]:   #1-n 个进行比较
						nes=keys[i]+(keys[j][l-1],) #到此转换为元组
						_id = [self.item2id[k] for k in nes]
						support = 1. * np.sum (np.prod (self.D[:, _id], 1)) / self.total  #一行元素相乘候 一列元素相加
						if support>self.min_support:
							rule[-1][nes]=support
		m = [len (rule[i]) for i in range (len (rule) - 1)]
		print (sum (m))
		print(rule)
		#分项集数输出
		'''for i in rule:
			print(i)'''
model = Apriori (0.01, 0.75)
model.build()

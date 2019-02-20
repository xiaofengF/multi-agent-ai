from __future__ import division
import csv
import random

CONSTANT_BID_PRICE = [86.63265306,
177.5,
84.66666667,
141.0869565,
116.7692308,
118.5652174,
104.3928571,
93.83783784,
99.81818182]

RAND_UPPER_BOUND = [300,
294,
294,
294,
277,
238,
300,
238,
252]

RAND_LOWER_BOUND = [68.87562748,
93.85629674,
89.65874539,
90.36335509,
62.9507772,
84.82409909,
76.78095826,
75.25925114,
77.07708349]


BUDGET = [4294602,
1568808,
1214876,
2394900,
388784,
2794021,
4350793,
3776735,
2993751]

PERCENTAGE = 8

ADVERTISERS = [1458, 2259, 2261, 2821, 2997, 3358, 3386, 3427, 3476]

total_impression = [0,0,0,0,0,0,0,0,0]
total_click = [0,0,0,0,0,0,0,0,0]
total_cost = [0,0,0,0,0,0,0,0,0]
click_through_rate = [0,0,0,0,0,0,0,0,0]
average_cpm = [0,0,0,0,0,0,0,0,0]
average_cpc = [0,0,0,0,0,0,0,0,0]

with open('we_data/validation.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:
		temp = row[0].split(',')
		if(temp[0] == 'click'):
			continue

		for i in range(len(ADVERTISERS)):
			if ADVERTISERS[i] == int(temp[23]):
				advertiser = i

		click = int(temp[0])
		payprice =int(temp[21])

		# random
		upper_bound = int(RAND_UPPER_BOUND[advertiser]) + 1
		lower_bound = int(RAND_LOWER_BOUND[advertiser]) + 1
		random_bid = random.randint(lower_bound,upper_bound)

		# const
		# constant_bid = int(CONSTANT_BID_PRICE[advertiser]) + 1

		if random_bid > payprice:
			if total_cost[advertiser] + payprice <= BUDGET[advertiser]/PERCENTAGE:
				total_cost[advertiser] += payprice
				total_click[advertiser] += click
				total_impression[advertiser] += 1
			else:
				print "Run out of budget!"
				break
		
	print "total impressions:\n"
	for i in total_impression:
		print i
	print '\n'
	print "total click:\n"
	for i in total_click:
		print i
	print '\n'
	print "total cost:\n"
	for i in total_cost:
		print i
	print '\n'

	for i in range(len(ADVERTISERS)):
		click_through_rate[i] = float(total_click[i]/total_impression[i])
		average_cpm[i] = (total_cost[i]/total_impression[i])*1000
		if total_click[i] == 0:
			average_cpc[i] = ""
		else:
			average_cpc[i] =  total_cost[i]/total_click[i]

	print "click-through rate:\n" 
	for i in click_through_rate:
		print i
	print '\n'
	print "average cpm:\n"
	for i in average_cpm:
		print i
	print '\n'
	print "average cpc:\n"
	for i in average_cpc:
		print i
	print '\n'

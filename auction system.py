from __future__ import division
import csv
import random
import matplotlib.pyplot as plt 

BUDGET = 6250000

def RTB_simulation(price):
	click_through_rate = 0
	total_impression = 0
	total_click = 0
	total_cost = 0

	with open('we_data/validation.csv', 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			temp = row[0].split(',')
			if(temp[0] == 'click'):
				continue

			click = int(temp[0])
			payprice =int(temp[21])

			if price > payprice:
				if total_cost+ payprice <= BUDGET:
					total_cost += payprice
					total_click += click
					total_impression += 1
				else:
					break
		
		if total_impression == 0:
			click_through_rate = 0
			average_cpm = 0
		else:
			click_through_rate = float(total_click/total_impression)

		return total_click, click_through_rate


def random_bidding_strategy():
	highest_upper_bound = 0
	highest_lower_bound = 0
	lower_bound = 0
	highest_CTR = 0
	highest_Click = 0

	for i in xrange(100):
		lower_bound += 1
		upper_bound = lower_bound
		while upper_bound < 300:
			upper_bound += 10

			average_bid = 0
			for j in range(5):
				average_bid += random.randint(lower_bound,upper_bound)
			average_bid = average_bid/5

			click, ctr = RTB_simulation(average_bid)
			global Highest_Click
			if click > highest_Click:
				highest_Click = click
				highest_CTR = ctr
				highest_upper_bound = upper_bound
				highest_lower_bound = lower_bound

		print "Progress:", i

	print "Best upper bound: ", highest_upper_bound, "Best lower bound: ", highest_lower_bound
	print "Highest click: ", highest_Click, "Highest_CTR: ", highest_CTR


def constant_bidding_strategy():

	clicks = []
	ctrs = []
	constant_bid_price = 0
	highest_CTR = 0
	highest_Click = 0

	for i in xrange(1,302):
		constant_bid_price += 1
		click, ctr = RTB_simulation(constant_bid_price)
		clicks.append(click)
		ctrs.append(ctr)
		bid_price.append(constant_bid_price)

		if click > highest_Click:
			highest_Click = click
			highest_CTR = ctr

		print "Progress:", i

	print "Highest click: ", highest_Click, "Highest_CTR: ", highest_CTR
	
	AVERAGE_CTR.append(avg_ctr) 
	plt.plot(bid_price, ctrs, linewidth=3)
	# plt.plot(bid_price, clicks, linewidth=3)
	plt.xlabel('bid price') 
	plt.ylabel('click_through_rate') 
	# plt.ylabel('total clicks') 
	plt.title('constant bidding') 
	plt.legend()
	plt.show() 


def multi_agent_rand_bidding():
	

def main():
	# constant_bidding_strategy()
	# random_bidding_strategy()
	multi_agent_rand_bidding()

if __name__ == '__main__':
	main()



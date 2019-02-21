from __future__ import division
import csv
import random
import matplotlib.pyplot as plt 


CONSTANT_BID_PRICE = 0
BUDGET = 6250000



def RTB_simulation(price):
	click_through_rate = 0
	total_impression = 0
	total_click = 0
	total_cost = 0
	average_cpm = 0
	average_cpc = 0

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

		# print "total click", total_click, "total impression", total_impression
		
		if total_impression == 0:
			click_through_rate = 0
			average_cpm = 0
		else:
			click_through_rate = float(total_click/total_impression)
		# 	average_cpm = (total_cost/total_impression)*1000

		# if total_click == 0:
		# 	average_cpc = ""
		# else:
		# 	average_cpc =  total_cost/total_click

		# global Highest_Click, Highest_CTR
		# if total_click > Highest_Click:
		# 	Highest_Click = total_click
		# if click_through_rate > Highest_CTR:
		# 	Highest_CTR = click_through_rate

		# print "total clicks", total_click

		return total_click, click_through_rate

highest_upper_bound = 0
highest_lower_bound = 0
Highest_CTR = 0
Highest_Click = 0

def main():
	AVERAGE_CTR = []
	bid_price =[]

	# clicks = 0
	# ctrs = 0
	lower_bound = 0

	for i in xrange(100):
		# global CONSTANT_BID_PRICE
		# CONSTANT_BID_PRICE += 1

		# random
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
			if click > Highest_Click:
				Highest_Click = click
				Highest_CTR = ctr
				highest_upper_bound = upper_bound
				highest_lower_bound = lower_bound

		print "Progress:", i

	print "Best upper bound: ", highest_upper_bound, "Best lower bound: ", highest_lower_bound
	print "Highest click: ", Highest_Click, "Highest_CTR: ", Highest_CTR


		# print "total clicks:", clicks/10,"CTR", ctrs/10
		# print "CTR:", ctr, "bid price:", random_bid

	
	# AVERAGE_CTR.append(avg_ctr) 
	# bid_price.append(CONSTANT_BID_PRICE)
	# plt.plot(bid_price, AVERAGE_CTR, linewidth=3)

	# print "Highest CTR:", Highest_CTR, "Highest clicks:", Highest_Click

	# plt.xlabel('bid price') 
	# plt.ylabel('click_through_rate') 
	# plt.title('constant bidding') 
	# plt.legend()
	# plt.show() 



if __name__ == '__main__':
	main()



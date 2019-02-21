from __future__ import division
import csv
import random
import matplotlib.pyplot as plt 


CONSTANT_BID_PRICE = 0
RAND_UPPER_BOUND = 
RAND_LOWER_BOUND = 
BUDGET = 6250000
Highest_CTR = 0
Highest_Click = 0

def calculate_CTR(price):
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

		print "total click", total_click, "total impression", total_impression
		
		if total_impression == 0:
			click_through_rate = 0
			average_cpm = 0
		else:
			click_through_rate = float(total_click/total_impression)
			average_cpm = (total_cost/total_impression)*1000

		if total_click == 0:
			average_cpc = ""
		else:
			average_cpc =  total_cost/total_click

		global Highest_Click, Highest_CTR

		if total_click > Highest_Click:
			Highest_Click = total_click
		if click_through_rate > Highest_CTR:
			Highest_CTR = click_through_rate

		print "total clicks", total_click

		return click_through_rate


def main():
	AVERAGE_CTR = []
	bid_price =[]



	for i in xrange(10):
		# global CONSTANT_BID_PRICE
		# CONSTANT_BID_PRICE += 1

		# random
		upper_bound = int(RAND_UPPER_BOUND) + 1
		lower_bound = int(RAND_LOWER_BOUND) + 1
		random_bid = random.randint(lower_bound,upper_bound)

		avg_ctr = calculate_CTR(CONSTANT_BID_PRICE)
		print "CTR:", avg_ctr, "bid price:", CONSTANT_BID_PRICE
	
	AVERAGE_CTR.append(avg_ctr) 
	bid_price.append(CONSTANT_BID_PRICE)
	plt.plot(bid_price, AVERAGE_CTR, linewidth=3)

	print "Highest CTR:", Highest_CTR, "Highest clicks:", Highest_Click

	plt.xlabel('bid price') 
	plt.ylabel('click_through_rate') 
	plt.title('constant bidding') 
	plt.legend()
	plt.show() 



if __name__ == '__main__':
	main()



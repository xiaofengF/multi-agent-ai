from sklearn.metrics import accuracy_score, log_loss, roc_curve, auc
from sklearn.feature_extraction.text import CountVectorizer
from xgboost import  XGBRegressor, XGBClassifier
import pandas as pd
import os
import matplotlib.pyplot as plt

from sklearn.metrics import roc_auc_score
from sklearn.neural_network import MLPClassifier

BUDGET = 6250000
USELESS_FEATURE = ['adexchange','click', 'bidprice', 'payprice', 'bidid', 'IP', 'userid', 'creative', 'domain', 'url', 'urlid', 'slotid', 'keypage']

# Gradient boosting decision trees GBDT
def preprocess_useragent(dataset):
	# first part of the column  
	print "Preprocessing useragent"
	dataset['os_system'] = dataset['useragent'].apply(lambda x: x.split('_')[0])
	# second part of the column
	dataset['browser'] = dataset['useragent'].apply(lambda x: x.split('_')[1])
	# delete user agent
	return dataset.drop('useragent', axis=1)

def preprocess_slotprice(dataset):
	# divide slot price into 3 parts
	print "Preprocessing slotprice"
	dataset['encoded_slotprice'] = pd.cut(dataset['slotprice'], 3, labels=[1, 2, 3])
	# delete slot price
	return dataset.drop('slotprice', axis=1)

# def preprocess_slotwidth(dataset):
# 	print "Preprocessing slotwidth"
# 	dataset['encoded_slotwidth'] = pd.cut(dataset['slotwidth'], 5, labels=[1, 2, 3, 4, 5])
# 	# delete slot price
# 	return dataset.drop('slotwidth', axis=1)

# def preprocess_slotheight(dataset):
# 	print "Preprocessing slotheight"
# 	dataset['encoded_slotheight'] = pd.cut(dataset['slotheight'], 5, labels=[1, 2, 3, 4, 5])
# 	# delete slot price
# 	return dataset.drop('slotheight', axis=1)


def preprocess_user_tags(dataset):
	print "Preprocessing user tags"

	data_usertag=dataset.usertag.fillna('0')
	data_usertag=data_usertag.str.replace(',',' ')
	vect=CountVectorizer()
	data_usertag_vect=vect.fit_transform(data_usertag)
	usertag=pd.DataFrame(data_usertag_vect.toarray(),columns=vect.get_feature_names())
	dataset = pd.concat([usertag, dataset], axis=1)
	return dataset.drop('usertag', axis=1)

def data_preprocessing(dataset):
	# one hot encoding and preprocessing
	dataset = dataset.drop(USELESS_FEATURE, axis=1)
	dataset = preprocess_useragent(dataset)
	dataset = preprocess_slotprice(dataset)
	# dataset = preprocess_slotheight(dataset)
	# dataset = preprocess_slotwidth(dataset)

 
	print "Encoding data"
	columns = list(dataset.columns.values)
	for i in range(len(columns)): 
		print "Encoding for:", columns[i]
		if columns[i] not in ['usertag']:
			dataset = pd.concat([dataset, pd.get_dummies(dataset[columns[i]],prefix=columns[i], sparse=True, drop_first=True, dummy_na=False)],axis=1).drop(columns[i], axis=1)

	dataset = preprocess_user_tags(dataset)

	return dataset

# def feature_extraction():

# def pCTR_prediction():


print "Loading data"
df_train = pd.read_csv('we_data/train.csv')
df_valid = pd.read_csv('we_data/validation.csv')

print "Processing data for training set"
x_train = data_preprocessing(df_train)

print "Processing data for validation set"
x_valid = data_preprocessing(df_valid)

# # label
y_train = df_train['click']
y_valid = df_valid['click']

print "Training data"

# Neural network
# model = MLPClassifier(verbose=True, hidden_layer_sizes=(300,150,50),solver='adam', alpha=0.0001)

# model = model.fit(x_train, y_train)
# pctr = model.predict_proba(x_valid)[:,1]

# # Print scores
# print("AUC: %0.5f for Neural Network Model"% (roc_auc_score(y_valid, pctr)))



# Gradient boosting

clf = XGBClassifier(max_depth=5, silent=False, gamma=0, min_child_weight =7, colsample_bytree=0.6,
                    subsample=0.95, reg_alpha = 0.03, learning_rate = 0.1, n_estimators=100)

clf_pCTR = clf.fit(x_train, y_train)

print "Predicting data"
# y_pred = clf_pCTR.predict(x_valid)
# predictions = [round(value) for value in y_pred]

pctr = clf_pCTR.predict_proba(x_valid)[:, 1]
print "PCTR:", pctr

# fpr, tpr, thresholds = roc_curve(y_valid, pctr)

# auc = auc(fpr, tpr)

# print "AUC:", auc



print "Bidding...."


avgCTR = df_train['click'].mean()

clicks = []
base_prices = []
p = df_valid['payprice']
c = df_valid['click']

for i in range(50, 200):
	total_click = 0
	total_cost = 0
	for j in range(len(df_valid)):
		bidprice = i * pctr[j] / avgCTR
		payprice = p[j]

		click = c[j]
		if bidprice > payprice:
			if total_cost + payprice <= BUDGET:
				total_cost += payprice
				total_click += click
			else:
				break

	print('base price=', i, 'total click=', total_click)
	clicks.append(total_click)
	base_prices.append(i)

plt.plot(base_prices, clicks, linewidth=3)
# plt.plot(bid_price, clicks, linewidth=3)
plt.xlabel('base price')
plt.ylabel('total clicks')
# plt.ylabel('total clicks')
plt.title('non linear bidding')
plt.legend()
plt.show()











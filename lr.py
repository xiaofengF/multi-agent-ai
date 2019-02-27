# dropped features: "bidid", "userid", "IP", "url" ( unique, or near-unique)

# dropped "urlid" -- only took 1 possible value in the training set

# one-hot-encoding were one-hot-encoded: "useragent", "region", "city", "adexchange", "domain", "soltid",
# "slotvisibility", "slotformat", "creative", "keypage","usertage", "advertiser"

# the following feature were left unchanged: weekday, hour, slotwidth, slotheight, slptprice
import graphlab as gl
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import csv

BUDGET = 6250*1000


def main():
    traindata = gl.SFrame.read_csv('train.csv', verbose=False)
    validation = gl.SFrame.read_csv('validation.csv', verbose=False)

    print(traindata.head(1))
    avgCTR = traindata['click'].mean()  # average CTR for training data

    print('trainset CTR',avgCTR)
    print('Validation CTR',validation['click'].mean())  # average CTR for validation data

    gl.canvas.set_target('ipynb')
    traindata.show()

    # change the tpye to string
    traindata['weekday'] = traindata['weekday'].astype(str)
    traindata['hour'] = traindata['hour'].astype(str)
    traindata['region'] = traindata['region'].astype(str)
    traindata['city'] = traindata['city'].astype(str)
    traindata['advertiser'] = traindata['advertiser'].astype(str)
    traindata['slotformat'] = traindata['slotformat'].astype(str)

    model = gl.logistic_classifier.create(traindata, target='click', max_iterations=100,
                                          features=['city', 'slotwidth', 'slotheight', 'useragent', 'slotformat', 'usertag', 'weekday', 'advertiser', 'creative', 'hour', 'slotvisibility', 'slotprice','region'])

    validation['weekday'] = validation['weekday'].astype(str)
    validation['hour'] = validation['hour'].astype(str)
    validation['region'] = validation['region'].astype(str)
    validation['city'] = validation['city'].astype(str)
    validation['advertiser'] = validation['advertiser'].astype(str)
    validation['slotformat'] = validation['slotformat'].astype(str)

    pCTRarr = model.predict(validation, output_type='probability')
    print('mean of the pCTR',pCTRarr.mean())
    print(len(validation))


    # bid= base_bid * pCTR / avgCTR
    clicks = []
    base_prices = []
    p = validation['payprice']
    c = validation['click']
    print(c.sum())
    for i in range(50, 200):
        total_click = 0
        total_cost = 0
        for j in range(len(validation)):
            bidprice = i * pCTRarr[j] / avgCTR
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
    plt.title('linear bidding')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
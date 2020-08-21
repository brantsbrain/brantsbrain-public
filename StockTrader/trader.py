from Robinhood import Robinhood
from cred import my_user,passwd,QR
import datetime, time, math

print("Beginning Program")
rh = Robinhood()

try:
    print("Logging In")
    logged_in = rh.login(username=my_user, password=passwd, qr_code=QR)
    print("Success")
except:
    print("Error logging in... exiting")

class Stock:
    def __init__(self,name,premarkhigh):
        self.name = name
        self.premarkhigh = premarkhigh
        self.bought = False
        self.sold = False
        self.cutoff = 0.02
        self.floor = premarkhigh - premarkhigh * self.cutoff
        self.ceiling = premarkhigh + premarkhigh * self.cutoff
        self.lastprice = premarkhigh
        self.sharesseeking = 0
        self.sharesowned = 0
        self.sold = False
        self.adjceil = False
        self.conf1 = "name"
        self.investment = 0.0
        self.url = ""

# Enter stock ticker and pre-market high
mystockdict = {"WATT" : Stock("WATT", 2.9), "VXRT" : Stock("VXRT", 3.35), "LIFE" : Stock("LIFE", 4.34), "NAT" : Stock("NAT", 5.8), "BIMI" : Stock("BIMI", 3.3)}
cash = 50
buysleft = 2
end = 1200

for x,y in mystockdict.items():
    y.investment = float(input("How much cash of remaining $" + str(cash) + " do you want to invest in " + x + " at PMH = $" + str(y.premarkhigh) + "/share?\nFull investment would buy " + str(math.floor(cash/y.premarkhigh)) + " shares: "))
    cash -= y.investment
    y.url = rh.instruments(x)[0]["url"]

print("\n")
marketopen = datetime.datetime.now().replace(hour=9, minute=30, second=0, microsecond=0)
# end = int(input("Enter timeout in seconds (300 = 5:00 min): "))
print("Will sell remaining positions after " + str(end/60) + " minutes")

def runProgram(cash, buysleft):
    cash = cash
    closed = True

    while closed == True:
        if datetime.datetime.now() >= marketopen:
            closed = False
            print(str(datetime.datetime.now()))
            print("Market is open\n")
            for x, y in mystockdict.items():
                print(x + " Last Traded Price: $" + rh.quote_data(x)["last_trade_price"] + "/share")
            print()
            start = time.time()

    while 1 == 1:
        for x,y in mystockdict.items():
            currentprice = float(rh.quote_data(x)["last_trade_price"])
            y.sharesseeking = int(math.floor(y.investment / currentprice))
            if currentprice <= y.floor and y.bought == True and y.sold == False:
                try:
                    marketsell = rh.place_market_sell_order(y.url, x, "GFD", y.sharesowned)
                    try:
                        print(marketsell)
                        print(rh.get_open_orders())
                        print(datetime.datetime.now())
                    except:
                        pass
                    y.sold = True
                    print("\nSold " + x + " at $" + str(currentprice) + "/share")
                except:
                    print("An error occured in selling... exiting.")
            elif currentprice > y.premarkhigh and y.bought == False and buysleft > 0 and y.sharesseeking != 0:
                try:
                    marketbuy = rh.place_market_buy_order(y.url, x, "GFD", y.sharesseeking)
                    try:
                        print(marketbuy)
                        print(rh.get_open_orders())
                        print(datetime.datetime.now())
                    except:
                        pass
                    y.sharesowned = y.sharesseeking
                    buysleft -= 1
                    y.bought = True
                    print("Bought " + str(y.sharesowned) + " shares of " + x + " at $" + str(currentprice))
                    y.investment = y.investment - y.sharesowned * currentprice
                    print("Investment left: $" + str(y.investment))
                    print("Initial Floor: $" + str(y.floor) + "\nInitial Celing: $" + str(y.ceiling) + "\n")
                except:
                    print("An error occurred in buying... exiting.")
            elif currentprice > y.lastprice and y.bought == True and y.sold == False:
                if currentprice > y.ceiling and y.adjceil == False:
                    y.cutoff = 0.01
                    y.adjceil = True
                    print("Moved " + x + " floor from $" + str(y.floor) + " to a 1% margin because price hit " + str(y.ceiling) + " ceiling")
                    print("New " + x + " floor: $" + str(currentprice - currentprice * y.cutoff))
                y.floor = currentprice - currentprice * y.cutoff
                y.lastprice = currentprice
                print("Adjusted " + x + " floor to: $" + str(y.floor))
            elif time.time() > start + end:
                print("Time Limit Reached")
                for x,y in mystockdict.items():
                    currentprice = float(rh.quote_data(x)["last_trade_price"])
                    if y.bought == True and y.sold == False:
                        rh.place_market_sell_order(y.url, x, "GFD", y.sharesowned)
                        y.sold = True
                        print("\nSold " + x + " at $" + str(currentprice) + "/share")
                return

runProgram(cash, buysleft)
print(datetime.datetime.now())

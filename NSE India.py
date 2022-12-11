import os
import matplotlib.pyplot as plt
import pandas as pd
import requests



###############                                          NSE to Excel market data (Graph)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class NseIndia:
    print(" ")
    print(" ")
    print("..                                    Fetching The most Updated Data 📟  ")
    print("..")
    print("..                                                             CONNECTING TO data_Server: NSEindia // Mumbai,India ")
    print("..                                                                                                      ⛓ .")
    print("..                                                                                                      ⛓ .")
    print("..                                                                                                      ⛓ .")
    print("..                                                                                                      ⛓ .")
    print("..                                                                                                      ⛓ .")
    print("..                                                                                            📡        ⛓ .")
    print(".                                                                             CONNECTION: Established http//:nse.com")
    print(".                                                                              Login:  KumudKumar//KumudTheDude//69 📍🇮🇳")
    print("          Printing Raw Market Data 📑")
    print(" ")
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        self.session = requests.Session()
        self.session.get("http://nseindia.com", headers=self.headers)

    def pre_market_data(self):
        pre_market_key = {"NIFTY 50": "NIFTY", "Nifty Bank": "BANKNIFTY", "Emerge": "SME", "Securities in F&O": "FO",
                          "Others": "OTHERS", "All": "ALL"}
        key = "NIFTY 50"   # input
        data = self.session.get(f"https://www.nseindia.com/api/market-data-pre-open?key={pre_market_key[key]}", headers=self.headers).json()["data"]
        new_data = []
        for i in data:
            new_data.append(i["metadata"])
        df = pd.DataFrame(new_data)
        # return list(df['symbol'])
        return df

    def live_market_data(self):
        live_market_index = {
            'Broad Market Indices': ['NIFTY 50', 'NIFTY NEXT 50', 'NIFTY MIDCAP 50', 'NIFTY MIDCAP 100',
                                     'NIFTY MIDCAP 150', 'NIFTY SMALLCAP 50', 'NIFTY SMALLCAP 100',
                                     'NIFTY SMALLCAP 250', 'NIFTY MIDSMALLCAP 400', 'NIFTY 100', 'NIFTY 200'],
            'Sectoral Indices': ["NIFTY AUTO", "NIFTY BANK", "NIFTY ENERGY", "NIFTY FINANCIAL SERVICES",
                                 "NIFTY FINANCIAL SERVICES 25/50", "NIFTY FMCG", "NIFTY IT", "NIFTY MEDIA",
                                 "NIFTY METAL", "NIFTY PHARMA", "NIFTY PSU BANK", "NIFTY REALTY",
                                 "NIFTY PRIVATE BANK"],
            'Others': ['Securities in F&O', 'Permitted to Trade'],
            'Strategy Indices': ['NIFTY DIVIDEND OPPORTUNITIES 50', 'NIFTY50 VALUE 20', 'NIFTY100 QUALITY 30',
                                 'NIFTY50 EQUAL WEIGHT', 'NIFTY100 EQUAL WEIGHT', 'NIFTY100 LOW VOLATILITY 30',
                                 'NIFTY ALPHA 50', 'NIFTY200 QUALITY 30', 'NIFTY ALPHA LOW-VOLATILITY 30',
                                 'NIFTY200 MOMENTUM 30'],
            'Thematic Indices': ['NIFTY COMMODITIES', 'NIFTY INDIA CONSUMPTION', 'NIFTY CPSE', 'NIFTY INFRASTRUCTURE',
                                 'NIFTY MNC', 'NIFTY GROWTH SECTORS 15', 'NIFTY PSE', 'NIFTY SERVICES SECTOR',
                                 'NIFTY100 LIQUID 15', 'NIFTY MIDCAP LIQUID 15']}

        indices = "Broad Market Indices"    # input Sector # Input
        key = "NIFTY 50"              # input   # Input
        # key = "NIFTY GROWTH SECTORS 15"              # input   # Input
        # indices = "Thematic Indices"    # input Sector # Input
        data = self.session.get(f"https://www.nseindia.com/api/equity-stockIndices?index={live_market_index[indices][live_market_index[indices].index(key)].upper().replace(' ','%20').replace('&', '%26')}", headers=self.headers).json()["data"]
        df = pd.DataFrame(data)          ### This point to short code: Df range here 
        # return list(df["symbol"])
        return df

    def holidays(self):
        holiday = ["clearing", "trading"]
        # key = input(f'Select option {holiday}\n: ')
        key = "trading"   # input
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={holiday[holiday.index(key)]}', headers=self.headers).json()
        df = pd.DataFrame(list(data.values())[0])
        return df                        ###  Return only works in Indent?

nse = NseIndia()

# print(nse.pre_market_data())
print(nse.live_market_data())
# print(nse.holidays())

#####            Data Processing Task 

raw_file_location = ## Location of your raw data in '' , eg:  '/Users/ray/Documents/Python.py /Excel test/Trading and Python Files/NSE RAW Data.xlsx'
savedata = nse.live_market_data().to_excel(raw_file_location)
raw_excel = pd.read_excel(raw_file_location)
df = pd.DataFrame(raw_excel)
# print(df)
print(".")
print("       Printing Cleaned Data 🖨 🧹")
print(".")
df.drop(['priority','identifier','ffmc','yearHigh','yearLow','nearWKH','Unnamed: 0'],axis=1,inplace=True)
df.drop(['nearWKL','perChange365d','date365dAgo','perChange30d','chartTodayPath','series','meta','chart30dPath','chart365dPath','date30dAgo'],axis=1,inplace=True)
df.columns=['Company','open','dayHIGH','dayLOW','LTP','PrevClosing','Change','% Change','Volumes','TotalValue','last updated time']
df.to_excel('/Users/ray/Documents/Python.py /Excel test/NSE Filtered Data.xlsx')

print(df)
filtered_excel_location = ## Location of your filtered data in ''  eg:  'Users/ray/Documents/Python.py /Excel test/Trading and Python Files/NSE RAW Data.xlsx'
df.to_excel(filtered_excel_location)

            ## Graph 1 (% Change)
print("  ")
print("  ")
print("Chart as Followes:         top 5 :  % Change from previous closing 📶")
print("  ")
grph = pd.DataFrame(df.nlargest(5,columns=['% Change']))
x = grph['Company']
y = grph['% Change']
print(grph)
plt.bar(x,y)
plt.xlabel("company")
plt.ylabel("Percentage Change")
plt.title('''        Top 5 Performers : 
                  Percentage Change ''')
plt.show()

            ## Graph 2 (total volume traded)
print("  ")
print("  ")
print("Chart as Followes:           top 7 :   Total Volumes Traded  🧭 ")
print("  ")
update_df = df.drop(labels=[0],axis=0)
grph2 = pd.DataFrame(update_df.nlargest(7, columns=['Volumes']))
x = grph2['Company']
y = grph2['Volumes']
print(grph2)
plt.bar(x,y)
plt.xlabel("company")
plt.ylabel("Volumes Traded")
plt.title('''        Top 7 Performers : 
                   Volume traded  ''')
plt.show()
print(" ")
print(" ")
print("                                                      NSE  Is LIVE 🟢  " )
print("")
print("")
print("This Data Has Been Saved In EXCEl Sheet post formatting 💾 ")
print("")
print("")





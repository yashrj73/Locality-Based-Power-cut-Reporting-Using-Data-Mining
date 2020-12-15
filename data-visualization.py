from matplotlib import pyplot as plt
from datetime import datetime
from sklearn import datasets
import pandas as pd
from collections import Counter

df = pd.read_csv(r"C:\Users\yshrivastava\Desktop\electricity-UPDATED.csv")
#print(df.dtypes)

to_drop = ['Demand Loss (MW)', 'Tags', 'Number of Customers Affected']

df.drop(columns=to_drop, inplace=True, axis=0)

#df["Date_of_Restoration"].replace('Unknown', 'Nan')

#print(df.head())
df[df.Date_of_Restoration != 'Unknown']
#print(df.head())
#print(type(df["Date Event Began"]))

#x = df["Time of Restoration"] - df["Time Event Began"]
year = df["Year"]
#print(year)
value = []
sum =0
months = []
count = dict()
for i in range(0, 120):
    x = df.iloc[i, :]
    #date = x.split("/ ")
    #print(x)
    FMT = '%H:%M:%S'
    date_format = "%m/%d/%Y"
    if x.loc["Date_Event_Began"] != ["Unknown", "Ongoing", "NaN", "NA", "N/A"] and x.loc["Date_of_Restoration"]\
            != "Ongoing" and x.loc["Date_of_Restoration"] != "Unknown" and x.loc["Date_of_Restoration"] != "NaN"and\
            x.loc["Date_of_Restoration"] != "NA" and x.loc["Date_of_Restoration"] != "N/A":
        delta1 = datetime.strptime(x.loc["Date_Event_Began"], date_format)
        delta = datetime.strptime(x.loc["Date_of_Restoration"], date_format) - datetime.strptime(x.loc["Date_Event_Began"], date_format)
        time = datetime.strptime(x.loc["Time of Restoration"], FMT) - datetime.strptime(x.loc["Time Event Began"], FMT)
        duration = delta.days*24 + time.seconds/3600
        months.append(delta1.month)
        sum = sum + duration
        #time = ((delta.days*24*60) + (min.seconds/60))
        #print(month)
        value.append(duration)
        #print("delta.days: {}".format(delta.days))
length = len(value)
average = sum/length
print("average : {}".format(average))
count = Counter(months)
print(count.keys())
lists = sorted(count.items()) # sorted by key, return a list of tuples

x, y = zip(*lists) # unpack a list of pairs into two tuples

plt.plot(x, y)
plt.title('Month-wise power cut for year 2014')
plt.xlabel('Month')
plt.ylabel('No of power cuts')
plt.show()
print("count: {}".format(count))
print("duration: {}".format(len(value)))
print("year: {}".format(len(year)))
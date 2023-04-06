import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%d')
ax.xaxis.set_major_formatter(myFmt)

# make up some data
x = [datetime.datetime.now() + datetime.timedelta(hours=i) for i in range(12)]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# plot
plt.scatter(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
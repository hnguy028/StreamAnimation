import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

dates = ['01/02/1991','01/03/1991','01/04/1991']
x = [dt.datetime.strptime(d,'%m/%d/%Y').date() for d in dates]
y = range(len(x)) # many thanks to Kyss Tao for setting me straight here

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,y, 'r+')

plt.legend(fontsize=18, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=False,
               shadow=False)
plt.gcf().autofmt_xdate()

plt.show()
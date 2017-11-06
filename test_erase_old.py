import datetime
import matplotlib.pyplot as plt

x = [datetime.datetime(2014, 1, 29, 12, 0, 0), datetime.datetime(2014, 1, 29, 6, 6, 0), datetime.datetime(2014, 1, 29, 4, 3, 2)]
y = [2, 4, 1]

fig, ax = plt.subplots()
ax.plot_date(x, y, markerfacecolor='CornflowerBlue', markeredgecolor='white')
fig.autofmt_xdate()
ax.set_xlim([datetime.datetime(2014, 1, 26, 0, 0, 0), datetime.datetime(2014, 2, 1, 12, 0, 0)])
ax.set_ylim([0, 5])

plt.show()
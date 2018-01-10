import matplotlib.pyplot as plt
import matplotlib.legend as mlegend

ax = plt.subplot(222)
ax2 = plt.subplot(221)

l1, = ax.plot([1,2,3])

leg1 = ax.legend([l1], ["long lable"], ncol=1)

leg2 = mlegend.Legend(ax, [l1, l1, l1, l1], tuple("1234"), ncol=2)

leg1._legend_box._children.append(leg2._legend_box._children[1])
leg1._legend_box.align="left" # the default layout is 'center'

plt.show()
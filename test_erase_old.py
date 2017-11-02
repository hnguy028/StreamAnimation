import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

class some():
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.line,  = self.ax.plot([],[], color="red", linestyle="-")
        self.scat, = self.ax.plot([],[], color="orange", marker="s", linestyle="")

        self.data = np.random.rand(1000)
        self.times = np.arange(1000)

        self.stepsize = 10
        self.showntimes = np.arange(self.stepsize)
        self.ax.set_ylim([0,1])
        self.ax.set_xlim([self.showntimes[0],self.showntimes[-1]])

        self.ani = animation.FuncAnimation(self.fig, self._upd_plot, blit=False, interval=60, repeat=False)
        plt.show()

    def _upd_plot(self,i):
        print i
        if i < len(self.data)-self.stepsize:
            self.scat.set_data(self.showntimes, self.data[i:i+self.stepsize])
            self.line.set_data(self.showntimes, self.data[i:i+self.stepsize].mean()*np.ones(len(self.showntimes)) )
            self.ax.set_xticklabels(self.times[i:i+self.stepsize])
        else:
            self.ani.event_source.stop()

if __name__ == '__main__':
    s = some()
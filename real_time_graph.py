import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import crypto_hype_automated
from matplotlib import animation


def run():
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    def animate(i):
        crypto_hype_automated.update()
        pull_data = open("out_count_temp.txt", "r").read()
        data_array = pull_data.split('\n')
        xar = []
        points = []
        for each_line in data_array:
            if len(each_line) > 1:
                x, y = each_line.split(',')
                xar.append(x)
                xar.append(int(y))
                points.append(xar)
                xar = []

        ax1.clear()

        for pt in points:
            ax1.plot([pt[0], pt[0]], [0, pt[1]])

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

#run()

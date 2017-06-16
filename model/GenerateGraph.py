import matplotlib
# this line is necessary otherwise matplotlib starts freaking out
matplotlib.use("svg")
import matplotlib.pyplot as plt

def createGraph(books):
    # create variables to save data for axes
    y = []
    x = [0, 1, 2, 3, 4, 5, 6, 7]
    xlabels = [0]
    ylabels = []

    # add data
    for book in books:
        y.append((book["BorrowedAmount"]))
        xlabels.append((book["Title"]))
    print(xlabels)
    # generate graph
    plt.bar(x, y, width=0.9, linewidth=0, align="center", color="#FDD05F")

    # add labels
    plt.ylabel("Amount")
    plt.xlabel("Books")
    plt.title("Number Of Times A Book Got Borrowed")

    # get current axes
    axes = plt.gca()
    # set limits
    axes.set_xlim([-0.5, max(x)+1])
    axes.set_ylim([0, max(y)+1])
    # change x values to strings with name of books
    axes.set_xticklabels(xlabels, rotation=75, horizontalalignment="right")
    # change y values to integers instead of floats
    for number in range(0, max(y)+2):
        ylabels.append(number)
    plt.yticks(ylabels)

    # make sure all axes labels are visible
    plt.tight_layout()

    #change size
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(10, 7)

    # save graph
    plt.savefig("/home/annelynn/P1_Site/static/img/_graph.svg", dpi=None, orientation='portrait', papertype=None, format=None, transparent=False, bbox_inches=None, pad_inches=0.1, frameon=None)


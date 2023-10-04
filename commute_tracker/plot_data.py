import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import polars as pl

def plot_go_work(plot, data, day_of_week=None):
    plot.scatter(
        data["time"], 
        data["duration_in_traffic"], 
        alpha=0.2, 
        edgecolors=None,
        linewidths=0)
    if day_of_week is not None:
        # if day_of_week is None, it's an all_plot
        plot.set_title(f"go_work {day_of_week}")
    else:
        # else, it's a day plot
        plot.set_title("go_work all")
    plot.set_ylim(15,30)
    plot.set_xlabel("travel start time")
    plot.set_ylabel("duration (mins)")
    plot.set_yticks(range(15, 30+1, 5))
    plot.tick_params(axis='x', rotation=90, labelsize=6)
    plot.minorticks_on()
    plot.grid(which="major", alpha=0.5, axis='y')
    plot.grid(which="minor", alpha=0.25, axis='y', linewidth=0.5)

def plot_go_home(plot, data, day_of_week=None):
    plot.scatter(
        data["time"], 
        data["duration_in_traffic"], 
        alpha=0.2, 
        edgecolors=None,
        linewidths=0)
    if day_of_week is not None:
        # if day_of_week is None, it's an all_plot
        plot.set_title(f"go_home {day_of_week}")
    else:
        # else, it's a day plot
        plot.set_title("go_home all")
    plot.set_ylim(15,40)
    plot.set_xlabel("travel start time")
    plot.set_ylabel("duration (mins)")
    plot.set_yticks(range(15, 40+1, 5))
    plot.tick_params(axis='x', rotation=90, labelsize=5)
    plot.minorticks_on()
    plot.grid(which="major", alpha=0.5, axis='y')
    plot.grid(which="minor", alpha=0.25, axis='y', linewidth=0.5)

if __name__ == "__main__":

    df = pl.read_csv("./commute_tracker/data.csv")

    # parse text properly. "22 mins" -> "22"
    df = df.with_columns(
        pl.col("duration_in_traffic").str.strip_suffix(" mins").cast(pl.Int64),
    ).sort("time")

    # filter out pipeworks gym location, not interested in that right now
    df = df.filter(
        (pl.col("origin") != "116 N 16th St, Sacramento, CA 95811, USA")
        & (pl.col("destination") != "116 N 16th St, Sacramento, CA 95811, USA")
    )

    # filter out weekend data, not interested in that either
    df = df.filter(
        (pl.col("day") != "Saturday")
        & (pl.col("day") != "Sunday")
    )

    # create matplotlib plot. Use 10 as least common multiple of rows of 2 and 5
    gs = GridSpec(3, 10)
    plt.suptitle("Travel times between home (2947 ottumwa) and WECO (301 harter)")

    # filter to separate go_work and go_home directions of travel
    all_go_work = df.filter(
        (pl.col("origin") == "2947 Ottumwa Dr, Sacramento, CA 95835, USA")
        & (pl.col("destination") == "301 Harter Ave, Woodland, CA 95776, USA")
        & (pl.col("time") <= "12:00")
    ).sort("time")
    all_go_home = df.filter(
        (pl.col("origin") == "301 Harter Ave, Woodland, CA 95776, USA")
        & (pl.col("destination") == "2947 Ottumwa Dr, Sacramento, CA 95835, USA")
        & (pl.col("time") >= "12:00")
    ).sort("time")

    # plot all go_work
    plot = plt.subplot(gs[0,0:5])
    plot_go_work(plot, all_go_work)

    # plot all go_home
    plot = plt.subplot(gs[0,5:10])
    plot_go_home(plot, all_go_home)

    # plot go_work and go_home for each day of the week
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i, day_of_week in enumerate(days_of_week):
        # filter for each direction
        go_work = all_go_work.filter(pl.col("day") == day_of_week).sort("time")
        go_home = all_go_home.filter(pl.col("day") == day_of_week).sort("time")

        # plot go_work for a day
        plot = plt.subplot(gs[1,2*i:(2*i+2)])
        plot_go_work(plot, go_work, day_of_week)

        # plot go_home for a day
        plot = plt.subplot(gs[2,2*i:(2*i+2)])
        plot_go_home(plot, go_home, day_of_week)

    plt.subplots_adjust(hspace=0.6, wspace=0.5)
    plt.show()
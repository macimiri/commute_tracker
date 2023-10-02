import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import polars as pl

if __name__ == "__main__":

    df = pl.read_csv("./commute_tracker/data.csv")

    # parse text properly
    df = df.with_columns(
        pl.col("duration_in_traffic").str.strip_suffix(" mins").cast(pl.Int64),
        # pl.col("time").str.to_time("%H:%M")
    ).sort("time")

    gs = GridSpec(3, 5)
    all_plot = plt.subplot(gs[0,:])

    all_plot.scatter(
        df["time"], 
        df["duration_in_traffic"],
        alpha=0.1,
        edgecolors=None)
    all_plot.set_title("all data")
    all_plot.set_ylim(0,50)
    all_plot.set_xlabel("travel start time")
    all_plot.set_ylabel("duration (mins)")
    all_plot.tick_params(axis='x', rotation=90)

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for i, day_of_week in enumerate(days_of_week):

        go_work = df.filter(
            (pl.col("origin") == "2947 Ottumwa Dr, Sacramento, CA 95835, USA")
            & (pl.col("destination") == "301 Harter Ave, Woodland, CA 95776, USA")
            & (pl.col("day") == day_of_week)
            & (pl.col("time") <= "12:00")
        )
        go_home = df.filter(
            (pl.col("origin") == "301 Harter Ave, Woodland, CA 95776, USA")
            & (pl.col("destination") == "2947 Ottumwa Dr, Sacramento, CA 95835, USA")
            & (pl.col("day") == day_of_week)
            & (pl.col("time") >= "12:00")
        ).sort("time")

        day_plt = plt.subplot(gs[1,i])
        day_plt.scatter(
            go_work["time"], 
            go_work["duration_in_traffic"], 
            alpha=0.1, 
            edgecolors=None)
        day_plt.set_title(f"go_work {day_of_week}")
        day_plt.set_ylim(0,50)
        day_plt.set_xlabel("travel start time")
        day_plt.set_ylabel("duration (mins)")
        day_plt.tick_params(axis='x', rotation=90)

        day_plt = plt.subplot(gs[2,i])
        day_plt.scatter(
            go_home["time"], 
            go_home["duration_in_traffic"], 
            alpha=0.1, 
            edgecolors=None)
        day_plt.set_title(f"go_home {day_of_week}")
        day_plt.set_ylim(0,50)
        day_plt.set_xlabel("travel start time")
        day_plt.set_ylabel("duration (mins)")
        day_plt.tick_params(axis='x', rotation=90)

    plt.subplots_adjust(hspace=1)
    plt.show()
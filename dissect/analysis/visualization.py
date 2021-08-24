import matplotlib.pyplot as plt
from dissect.analysis.data_processing import get_all, filter_df
from dissect.analysis.widgets import get_choices
from ipywidgets import widgets, interact, fixed
from IPython.display import display
import pandas


def violin(df, feature):
    plt.figure(figsize=(12, 8), dpi=100, facecolor='w', edgecolor='k')
    plt.violinplot([df[feature].tolist()])
    plt.show()


def multibarplot(ax, df, param, feature, modifier=lambda x: x, title=None, tick_spacing=0, xlab="Values",
                 ylab="Normalized count", drop_timeouts=True):
    # make a copy of the dataframe, drop timeouts if eligible and apply the modifier function to the feature row
    df2 = df.copy(deep=False)
    if drop_timeouts:
        df2 = df2[df2[feature] != "NO DATA (timed out)"]
    df2[feature] = df2[feature].apply(modifier)

    # classify entries and count them
    std = df2[df2["standard"] == True]
    sim = df2[df2["standard"] == False]
    if len(df2) == 0:
        return
    df2_counts = df2[feature].value_counts() / len(df2)

    # choose suitable x-axis ticks
    if tick_spacing == 0:
        ticks = sorted(list(df2_counts.index))
        locs = range(len(ticks))
        labels = ticks
    else:
        low = min(df2_counts.index) - (min(df2_counts.index) % tick_spacing)
        high = (
                max(df2_counts.index)
                - (max(df2_counts.index) % tick_spacing)
                + tick_spacing
        )
        ticks = range(low, high + 1)
        locs = [i for i in range(len(ticks)) if i % tick_spacing == 0]
        labels = [t for t in ticks if t % tick_spacing == 0]

    # create the normalized barplot
    if not len(std) == 0:
        std_counts = std[feature].value_counts() / len(std)
        ax.bar(
            std_counts.index.map(ticks.index) - 0.2,
            std_counts.values,
            width=0.4,
            label=f"Standard curves n={len(std)}",
        )
    if not len(sim) == 0:
        sim_counts = sim[feature].value_counts() / len(sim)
        ax.bar(
            sim_counts.index.map(ticks.index) + 0.2,
            sim_counts.values,
            width=0.4,
            label=f"Simulated curves n={len(sim)}",
        )
    if len(param) > 0 and title is None:
        p, v = param.popitem()
        # title = f"Normalized barplot of {feature} for {p}={v[0]}"
        title = f"{p}={v[0]}"
        ax.title.set_text(title)
    ax.set_xticks(locs)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)


# def normalized_parameters_bubbleplot()


def multiplot_mess(height, width, columns, trait_df, choices, modifier=None, tick_spacing=None):
    custom_modifier = True if modifier is not None else False
    results = get_all(trait_df, choices)
    nrows = len(results) // columns + 1
    fig, axes = plt.subplots(figsize=(width, height), nrows=nrows, ncols=columns)
    if nrows == 1 and columns == 1:
        axes = [axes]
    fig.tight_layout(pad=4.0, rect=[0, 0.03, 1, 0.95])
    if nrows > 1 and columns > 1:
        axes = [item for sublist in axes for item in sublist]
    for ax in axes[len(results):]:
        fig.delaxes(ax)
    for result, ax in zip(results, axes):
        df, param, feature, picked_modifier, modifier_name = result
        picked_modifier = modifier if custom_modifier else picked_modifier
        picked_tick_spacing = tick_spacing if tick_spacing is not None else 0
        multibarplot(ax, df, param, feature, picked_modifier, tick_spacing=picked_tick_spacing)
    modifier_title = "custom" if custom_modifier else modifier_name
    title = f"Normalized barplot of {feature} with modifier: {modifier_title}"
    fig.suptitle(title)
    return fig


def change_size(figure, width, height):
    figure.set_figheight(height)
    figure.set_figwidth(width)
    display(figure)


def interact_multiplot(trait_df, choices, modifier=None, tick_spacing=0, columns=1):
    def_height, def_width = 10, 7
    fig = multiplot_mess(def_height, def_width, columns, trait_df, choices, modifier=modifier,
                         tick_spacing=tick_spacing)
    plt.close()
    heightSlider = widgets.IntSlider(description='height', min=1, max=30, step=1, value=10)
    widthSlider = widgets.IntSlider(description='width', min=1, max=30, step=1, value=7)
    ui = widgets.HBox([heightSlider, widthSlider])
    out = widgets.interactive_output(change_size, {'width': widthSlider, 'height': heightSlider, 'figure': fixed(fig)})
    display(ui, out)


def multiplot(nrows, ncols, height=5, width=7):
    fig, axes = plt.subplots(figsize=(width, height), nrows=nrows, ncols=ncols)
    return axes


def normalized_barplot(v1, v2, ax=None, v1_title="Standard curves", v2_title="Simulated curves", title=None):
    both = pandas.concat([v1, v2])

    both_counts = both.value_counts() / len(both)
    v1_counts = v1.value_counts() / len(v1)
    v2_counts = v2.value_counts() / len(v2)

    ticks = sorted(list(both_counts.index))

    if not ax:
        fig, ax = plt.subplots(figsize=(6, 6), nrows=1, ncols=1)
    ax.bar(v1_counts.index.map(ticks.index) - 0.2, v1_counts.values, width=0.4,
           label=f"{v1_title} n={len(v1)}")
    ax.bar(v2_counts.index.map(ticks.index) + 0.2, v2_counts.values, width=0.4,
           label=f"{v2_title} n={len(v2)}")
    ax.set_xticks(range(len(ticks)))
    ax.legend()
    if title:
        ax.title(title)
    ax.set_xlabel("values")
    ax.set_ylabel("Normalized count")


def normalized_bubbleplot(v1, v2, ax=None, v1_title="Standard curves", v2_title="Simulated curves", title=None):
    v1_counts = v1.value_counts()
    v2_counts = v2.value_counts()
    v1_positions = zip(*v1_counts.index)
    v2_positions = zip(*v2_counts.index)

    v1_area = 30 ** 2 * v1_counts.values / sum(v1_counts.values)
    v2_area = 30 ** 2 * v2_counts.values / sum(v2_counts.values)

    if not ax:
        fig, ax = plt.subplots(figsize=(6, 6), nrows=1, ncols=1)
    ax.scatter(*v1_positions, s=v1_area, alpha=0.5, label=f"{v1_title} n={len(v1)}")
    ax.scatter(*v2_positions, s=v2_area, alpha=0.5, label=f"{v2_title} n={len(v2)}")
    ax.legend()
    labels = list(v1.keys())
    if title:
        ax.title(title)
    if v1_title:
        ax.set_xlabel(labels[0])
    if v2_title:
        ax.set_ylabel(labels[1])
    if not ax:
        ax.plot()

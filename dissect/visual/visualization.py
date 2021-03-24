import matplotlib.pyplot as plt
from dissect.utils.data_processing import get_all, filter_df
from dissect.visual.widgets import get_choices
from ipywidgets import widgets, interact, fixed


def normalized_barplot(
        ax,
        df,
        param,
        feature,
        modifier=lambda x: x,
        title=None,
        tick_spacing=0,
        xlab="Values",
        ylab="Normalized count",
        drop_timeouts=True,
):
    # make a copy of the dataframe, drop timeouts if eligible and apply the modifier function to the feature row
    df2 = df.copy(deep=False)
    if drop_timeouts:
        df2 = df2[df2[feature] != "NO DATA (timed out)"]
    df2[feature] = df2[feature].apply(modifier)

    # classify entries and count them
    std = df2[df2["simulated"] == False]
    sim = df2[df2["simulated"] == True]
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

    p, v = param.popitem()
    ax.set_xticks(locs)
    ax.set_xticklabels(labels)
    ax.legend()
    if title is None:
        # title = f"Normalized barplot of {feature} for {p}={v[0]}"
        title = f"{p}={v[0]}"
    ax.title.set_text(title)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)
    # plt.show()


def normalized_bubbleplot(
        df, xfeature, yfeature, title="Normalized bubble plot", xlab=None, ylab=None
):
    if not xlab:
        xlab = xfeature
    if not ylab:
        ylab = yfeature

    df = df[["simulated", xfeature, yfeature]]
    df = df.dropna(subset=(xfeature, yfeature))

    std = df[df["simulated"] == False]
    std = std.drop(["simulated"], axis=1)
    sim = df[df["simulated"] == True]
    sim = sim.drop(["simulated"], axis=1)

    std_counts = std.value_counts()
    sim_counts = sim.value_counts()

    std_positions = zip(*std_counts.index)
    sim_positions = zip(*sim_counts.index)

    std_area = 30 ** 2 * std_counts.values / sum(std_counts.values)
    sim_area = 30 ** 2 * sim_counts.values / sum(sim_counts.values)

    plt.figure(figsize=(10, 6))
    plt.scatter(
        *std_positions, s=std_area, alpha=0.5, label=f"Standard curves n={len(std)}"
    )
    plt.scatter(
        *sim_positions, s=sim_area, alpha=0.5, label=f"Simulated curves n={len(sim)}"
    )
    plt.legend()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()


def multiplot(height, width, columns, trait_df, filtering_widgets,modifier = None, tick_spacing = None):
    custom_modifier = True if modifier!=None else False
    results = list(get_all(trait_df, get_choices(filtering_widgets)))
    nrows = len(results) // columns + 1
    fig, axes = plt.subplots(figsize=(width, height), nrows=nrows, ncols=columns)
    fig.tight_layout(pad=4.0, rect=[0, 0.03, 1, 0.95])
    if nrows > 1 and columns > 1:
        axes = [item for sublist in axes for item in sublist]
    for ax in axes[len(results):]:
        fig.delaxes(ax)
    for result, ax in zip(results, axes):
        df, param, feature, picked_modifier, modifier_name = result
        picked_modifier = modifier if custom_modifier else picked_modifier
        picked_tick_spacing = tick_spacing if tick_spacing!=None else 0
        normalized_barplot(ax, df, param, feature, picked_modifier, tick_spacing=picked_tick_spacing)
    modifier_title = "custom" if custom_modifier else modifier_name
    title = f"Normalized barplot of {feature} with modifier: {modifier_title}"
    fig.suptitle(title)
    plt.show()


def interact_multiplot(trait_df, filtering_widgets, modifier = None, tick_spacing = 0):
    # interact(multiplot, height=widgets.IntSlider(min=1, max=30, step=1, value=10), width=widgets.IntSlider(min=1, max=30, step=1, value=7), columns=widgets.IntSlider(min=1, max=10, step=1, value=1), results=fixed(results.values()))
    interact(multiplot, height=widgets.IntSlider(min=1, max=30, step=1, value=10),
             width=widgets.IntSlider(min=1, max=30, step=1, value=7),
             columns=widgets.IntSlider(min=1, max=10, step=1, value=1), trait_df=fixed(trait_df),
             filtering_widgets=fixed(filtering_widgets),
             modifier = fixed(modifier),
             tick_spacing= fixed(tick_spacing))
    return filter_df(trait_df, get_choices(filtering_widgets))

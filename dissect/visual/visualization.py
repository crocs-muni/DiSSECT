import matplotlib.pyplot as plt


def normalized_barplot(df, feature, modifier=lambda x: x, title=None, all_x_ticks=True, xlab="Values",
                       ylab="Normalized count"):
    # make a copy of the dataframe and apply the modifier function to the feature row
    df = df.copy(deep=False)
    df[feature] = df[feature].apply(modifier)

    # classify entries and count them
    std = df[df["simulated"] == False]
    sim = df[df["simulated"] == True]
    if len(df) == 0:
        return
    df_counts = df[feature].value_counts() / len(df)

    # choose suitable x-axis ticks
    if all_x_ticks:
        ticks = range(min(df_counts.index), max(df_counts.index) + 1)
    else:
        ticks = sorted(list(df_counts.index))

    # create the normalized barplot
    plt.figure(figsize=(10, 6))
    if not len(std) == 0:
        std_counts = std[feature].value_counts() / len(std)
        plt.bar(std_counts.index.map(ticks.index) - 0.2, std_counts.values, width=0.4,
                label=f"Standard curves n={len(std)}")
    if not len(sim) == 0:
        sim_counts = sim[feature].value_counts() / len(sim)
        plt.bar(sim_counts.index.map(ticks.index) + 0.2, sim_counts.values, width=0.4,
                label=f"Simulated curves n={len(sim)}")

    plt.xticks(range(len(ticks)), ticks)
    plt.legend()
    if title is None:
        title = f"Normalized barplot of {feature}"
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()


def normalized_bubbleplot(df, xfeature, yfeature, title="Normalized bubble plot", xlab=None, ylab=None):
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
    plt.scatter(*std_positions, s=std_area, alpha=0.5, label=f"Standard curves n={len(std)}")
    plt.scatter(*sim_positions, s=sim_area, alpha=0.5, label=f"Simulated curves n={len(sim)}")
    plt.legend()
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.show()

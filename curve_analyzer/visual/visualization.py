import matplotlib.pyplot as plt


def normalized_barplot(df, feature, title="Normalized bar plot", xlab="Values", ylab="Normalized count"):
    std = df[df["simulated"] == False]
    sim = df[df["simulated"] == True]

    df_counts = df[feature].value_counts() / len(df)
    std_counts = std[feature].value_counts() / len(std)
    sim_counts = sim[feature].value_counts() / len(sim)

    ticks = sorted(list(df_counts.index))

    plt.figure(figsize=(10, 6))
    plt.bar(std_counts.index.map(ticks.index) - 0.2, std_counts.values, width=0.4, label=f"Standard curves n={len(std)}")
    plt.bar(sim_counts.index.map(ticks.index) + 0.2, sim_counts.values, width=0.4, label=f"Simulated curves n={len(sim)}")
    plt.xticks(range(len(ticks)), ticks)
    plt.legend()
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

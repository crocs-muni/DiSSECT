import matplotlib.pyplot as plt
from sage.all import RR, ZZ


class Modifier:
    """a class of lambda functions for easier modifications if visualised values"""

    def __init__(self):
        pass

    @staticmethod
    def identity():
        return lambda x: x

    @staticmethod
    def ratio(ratio_precision=10):
        return lambda x: RR(x).numerical_approx(digits=ratio_precision)

    @staticmethod
    def bits():
        return lambda x: ZZ(x).nbits()

    @staticmethod
    def factorization_bits(factor_index=-1):
        return lambda x: ZZ(x[factor_index]).nbits()

    @staticmethod
    def length():
        return lambda x: len(x)


def normalized_barplot(df,param, feature, modifier=lambda x: x, title=None, tick_spacing=0, xlab="Values",
                       ylab="Normalized count", figsize=(10, 6), drop_timeouts=True):
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
        high = max(df2_counts.index) - (max(df2_counts.index) % tick_spacing) + tick_spacing
        ticks = range(low, high + 1)
        locs = [i for i in range(len(ticks)) if i % tick_spacing == 0]
        labels = [t for t in ticks if t % tick_spacing == 0]

    # create the normalized barplot
    plt.figure(figsize=figsize)
    if not len(std) == 0:
        std_counts = std[feature].value_counts() / len(std)
        plt.bar(std_counts.index.map(ticks.index) - 0.2, std_counts.values, width=0.4,
                label=f"Standard curves n={len(std)}")
    if not len(sim) == 0:
        sim_counts = sim[feature].value_counts() / len(sim)
        plt.bar(sim_counts.index.map(ticks.index) + 0.2, sim_counts.values, width=0.4,
                label=f"Simulated curves n={len(sim)}")

    p,v = param.popitem()
    plt.xticks(locs, labels)
    plt.legend()
    if title is None:
        title = f"Normalized barplot of {feature} for {p}={v[0]}"
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

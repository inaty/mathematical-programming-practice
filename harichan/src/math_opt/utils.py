import matplotlib.pyplot as plt


def plot_map(pos_warehouse: dict, stores_info: dict):
    """倉庫と店舗の位置関係を描画する。"""

    fig, ax = plt.subplots(figsize=(10, 10))

    # plot warehouse
    ax.scatter(*pos_warehouse, s=600, c="red", marker="*")
    ax.text(pos_warehouse[0] - 0.06, pos_warehouse[1] + 0.03, "warehouse", size=12, c="red")

    # plot stores
    xs = [info["pos"][0] for info in stores_info.values()]
    ys = [info["pos"][1] for info in stores_info.values()]

    ax.scatter(xs, ys)
    for store_name, info in stores_info.items():
        ax.text(info["pos"][0] - 0.05, info["pos"][1] + 0.02, f"{store_name}: {info['stock']}", size=12)

    fig.patch.set_facecolor("white")
    ax.set(xlim=(-0.05, 1.05), ylim=(-0.05, 1.05))
    ax.set_xlabel("x coordinate", size=20)
    ax.set_ylabel("y coordinate", size=20)
    ax.tick_params(labelsize=15)

    return fig

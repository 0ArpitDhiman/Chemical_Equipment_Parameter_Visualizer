from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

THEME_BG = "#111426"
GRID = "#262a40"
TEXT = "#cbd5e1"

COLORS = [
    "#6366f1",
    "#8b5cf6",
    "#ec4899",
    "#f59e0b",
    "#10b981",
    "#3b82f6",
    "#fb7185",
]


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.fig.patch.set_facecolor(THEME_BG)
        self.ax.set_facecolor(THEME_BG)
        self.ax.tick_params(colors=TEXT)
        for s in self.ax.spines.values():
            s.set_color(GRID)

    def _style(self, title=""):
        self.ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold")
        self.ax.tick_params(colors=TEXT)
        for s in self.ax.spines.values():
            s.set_color(GRID)

    def clear(self, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)
        self._style(title)
        self.draw()

    def bar(self, labels, values, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)

        if labels and values:
            colors = [COLORS[i % len(COLORS)] for i in range(len(labels))]
            self.ax.bar(labels, values, color=colors, edgecolor=GRID, linewidth=0.8)
            self.ax.tick_params(axis="x", rotation=20)

        self._style(title)
        self.fig.tight_layout()
        self.draw()

    def lines(self, xlabels, series, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)

        for i, (name, y) in enumerate(series.items()):
            self.ax.plot(
                xlabels,
                y,
                label=name,
                linewidth=2.4,
                marker="o",
                markersize=4,
                color=COLORS[i % len(COLORS)],
            )

        self.ax.grid(True, color=GRID, alpha=0.4)
        self.ax.legend(facecolor=THEME_BG, edgecolor=GRID, labelcolor=TEXT)
        self._style(title)
        self.fig.tight_layout()
        self.draw()

    def pie(self, labels, values, title=""):
        self.ax.clear()
        self.fig.patch.set_facecolor(THEME_BG)

        if not labels or not values:
            self.draw()
            return

        colors = [COLORS[i % len(COLORS)] for i in range(len(labels))]

        self.ax.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.1f%%",
            startangle=140,
            textprops={"color": TEXT, "fontsize": 9},
            wedgeprops={"edgecolor": GRID, "linewidth": 1},
        )

        self.ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold")
        self.ax.axis("equal")
        self.fig.tight_layout()
        self.draw()

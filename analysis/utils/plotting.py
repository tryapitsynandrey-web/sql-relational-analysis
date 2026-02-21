"""
Matplotlib plotting helpers for the Olist analytics notebook layer.

All charts produced in this project share a consistent visual style defined
in :func:`apply_style`.  Use :func:`save_figure` to persist output to the
``analysis/figures/`` directory.

Calling :func:`apply_style` once at the top of a notebook is sufficient to
propagate the theme to every subsequent plot in that session.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.figure import Figure


# ---------------------------------------------------------------------------
# Directory configuration
# ---------------------------------------------------------------------------

# Resolved at import time so that notebooks can call save_figure() with a
# bare filename and have it land in the right place regardless of the current
# working directory.
_FIGURES_DIR = Path(__file__).resolve().parents[1] / "figures"
_FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Style
# ---------------------------------------------------------------------------

# A hand-picked, muted colour palette for categorical series.
PALETTE = [
    "#2196F3",  # blue
    "#4CAF50",  # green
    "#FF9800",  # amber
    "#9C27B0",  # purple
    "#F44336",  # red
    "#00BCD4",  # cyan
    "#FF5722",  # deep orange
    "#8BC34A",  # light green
]

# Two-colour scheme for binary comparisons (e.g. on-time vs delayed).
BINARY_PALETTE = {"positive": "#4CAF50", "negative": "#F44336"}


def apply_style() -> None:
    """
    Apply a consistent, publication-ready Matplotlib rcParams style.

    Call this once per notebook session, immediately after the notebook's
    import block.  All subsequent plots in the session will inherit these
    settings without further configuration.

    The style emphasises readability: light grid lines, legible font sizes,
    and a clean white background suitable for both screen and print.
    """
    plt.rcParams.update(
        {
            # Figure defaults
            "figure.dpi": 120,
            "figure.facecolor": "white",
            "figure.edgecolor": "white",
            # Axes
            "axes.facecolor": "#F9F9F9",
            "axes.edgecolor": "#CCCCCC",
            "axes.linewidth": 0.8,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.prop_cycle": plt.cycler(color=PALETTE),
            "axes.spines.top": False,
            "axes.spines.right": False,
            # Grid
            "grid.color": "#E0E0E0",
            "grid.linewidth": 0.6,
            "grid.linestyle": "--",
            # Typography
            "font.family": "sans-serif",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            # Legend
            "legend.framealpha": 0.85,
            "legend.fontsize": 10,
            # Lines and markers
            "lines.linewidth": 2.0,
            "lines.markersize": 6,
            # Output
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )


def save_figure(fig: Figure, filename: str) -> Path:
    """
    Save a Matplotlib figure to ``analysis/figures/``.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure object to save.
    filename : str
        Output filename including extension, e.g. ``"01_revenue_trend.png"``.
        The file will be written to ``analysis/figures/<filename>``.

    Returns
    -------
    Path
        Absolute path to the saved file.

    Examples
    --------
    >>> fig, ax = plt.subplots()
    >>> ax.plot([1, 2, 3])
    >>> path = save_figure(fig, "example_chart.png")
    >>> path.name
    'example_chart.png'
    """
    output_path = _FIGURES_DIR / filename
    fig.savefig(output_path)
    return output_path


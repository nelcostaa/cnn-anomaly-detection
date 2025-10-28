from __future__ import annotations

from pathlib import Path

import nbformat as nbf


def add_md(nb: nbf.NotebookNode, text: str) -> None:
    nb.cells.append(nbf.v4.new_markdown_cell(text))


def add_py(nb: nbf.NotebookNode, code: str) -> None:
    nb.cells.append(nbf.v4.new_code_cell(code))


def build_notebook() -> nbf.NotebookNode:
    nb = nbf.v4.new_notebook()

    add_md(
        nb,
        "# GECCO2018 Water Quality — Notebook 02: Time-Aware Visualizations\n\n"
        "Este notebook foca em visualizações orientadas a série temporal do dataset GECCO2018.\n\n"
        "Objetivos:\n"
        "- Carregar o dataset e aplicar limpezas básicas (parse de `Time`, coerção de tipos, remoção de nulos).\n"
        "- Visualizar séries temporais das variáveis sensoriais com indicação de `EVENT`.\n"
        "- Explorar distribuições e correlações entre sensores.\n"
        "- Salvar figuras principais em `reports/figures/`.",
    )

    add_py(
        nb,
        "# Package imports (wqdab installed via pip install -e .)\n"
        "# No sys.path manipulation needed with proper package structure",
    )

    add_py(
        nb,
        "%load_ext autoreload\n"
        "%autoreload 2\n\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "import seaborn as sns\n"
        "import matplotlib.pyplot as plt\n\n"
        "from wqdab.utils.paths import ensure_directories_exist, FIGURES_DIR\n"
        "from wqdab.data.loaders import load_gecco2018_csv\n\n"
        "sns.set_theme(style=\"whitegrid\")\n"
        "plt.rcParams[\"figure.figsize\"] = (14, 5)",
    )

    add_py(
        nb,
        "# Ensure data/ and reports/figures directories exist\n"
        "ensure_directories_exist()\n"
        "print(\"FIGURES_DIR:\", FIGURES_DIR)",
    )

    add_py(
        nb,
        "# Load dataset\n"
        "try:\n"
        "    df = load_gecco2018_csv()\n"
        "except FileNotFoundError as e:\n"
        "    print(e)\n"
        "    raise\n\n"
        "print(df.shape)\n"
        "df.head(10)",
    )

    add_py(
        nb,
        "# Basic cleaning: drop unnamed, parse time, coerce types, drop nulls\n"
        "# Drop unnamed index column if present\n"
        "if \"Unnamed: 0\" in df.columns:\n"
        "    df = df.drop(columns=[\"Unnamed: 0\"])\n\n"
        "# Parse Time\n"
        "df[\"Time\"] = pd.to_datetime(df[\"Time\"], errors=\"coerce\")\n\n"
        "# Coerce numeric columns\n"
        "numeric_cols = [\"Tp\", \"Cl\", \"pH\", \"Redox\", \"Leit\", \"Trueb\", \"Cl_2\", \"Fm\", \"Fm_2\"]\n"
        "for c in numeric_cols:\n"
        "    df[c] = pd.to_numeric(df[c], errors=\"coerce\")\n\n"
        "# Ensure EVENT is boolean\n"
        "if df[\"EVENT\"].dtype != bool:\n"
        "    df[\"EVENT\"] = df[\"EVENT\"].astype(str).str.lower().isin([\"true\", \"1\", \"t\", \"yes\"])\n\n"
        "# Drop rows with nulls in Time or numeric sensors\n"
        "df_clean = df.dropna(subset=[\"Time\"] + numeric_cols)\n\n"
        "# Sort by time and set index\n"
        "df_clean = df_clean.sort_values(\"Time\").reset_index(drop=True)\n"
        "df_ts = df_clean.set_index(\"Time\").sort_index()\n\n"
        "print(\"After cleaning:\", df_ts.shape)\n"
        "df_ts.head(5)",
    )

    add_py(
        nb,
        "# Info and missingness check\n"
        "print(df_ts.info())\n"
        "df_ts.isnull().sum()",
    )

    add_py(
        nb,
        "# Event count and timeframe\n"
        "print(\"EVENT true count:\", int(df_ts[\"EVENT\"].sum()))\n"
        "print(\"Time range:\", df_ts.index.min(), \"->\", df_ts.index.max())",
    )

    add_py(
        nb,
        "# Time series plots with event overlays\n"
        "import matplotlib.pyplot as plt\n\n"
        "def plot_timeseries_with_events(df_ts, columns, event_col=\"EVENT\", max_cols_per_fig=3, save=False, prefix=\"ts\"):\n"
        "    cols = list(columns)\n"
        "    for start in range(0, len(cols), max_cols_per_fig):\n"
        "        subset = cols[start:start+max_cols_per_fig]\n"
        "        n = len(subset)\n"
        "        fig, axes = plt.subplots(n, 1, figsize=(14, 4*n), sharex=True)\n"
        "        if n == 1:\n"
        "            axes = [axes]\n"
        "        for ax, col in zip(axes, subset):\n"
        "            ax.plot(df_ts.index, df_ts[col], color=\"C0\", linewidth=0.8)\n"
        "            ax.set_ylabel(col)\n"
        "            ax.set_title(f\"{col} over time\")\n"
        "            if event_col in df_ts.columns:\n"
        "                event_times = df_ts.index[df_ts[event_col]]\n"
        "                if len(event_times) > 0:\n"
        "                    ymin, ymax = ax.get_ylim()\n"
        "                    ax.vlines(event_times, ymin=ymin, ymax=ymax, color=\"crimson\", alpha=0.2, linewidth=0.5)\n"
        "        plt.tight_layout()\n"
        "        if save:\n"
        "            from pathlib import Path as _Path\n"
        "            out = _Path(FIGURES_DIR) / f\"{prefix}_{start//max_cols_per_fig+1}.png\"\n"
        "            fig.savefig(out, dpi=150, bbox_inches=\"tight\")\n"
        "        plt.show()\n\n"
        "sensor_cols = [\"Tp\", \"Cl\", \"pH\", \"Redox\", \"Leit\", \"Trueb\", \"Cl_2\", \"Fm\", \"Fm_2\"]\n"
        "plot_timeseries_with_events(df_ts, sensor_cols, save=True, prefix=\"timeseries\")",
    )

    add_py(
        nb,
        "# Distributions\n"
        "numeric_cols = df_ts.select_dtypes(include=[np.number]).columns.tolist()\n"
        "df_ts[numeric_cols].hist(bins=30, figsize=(16, 12))\n"
        "plt.tight_layout()\n"
        "plt.show()",
    )

    add_py(
        nb,
        "# Correlation heatmap\n"
        "numeric_cols = df_ts.select_dtypes(include=[np.number]).columns.tolist()\n"
        "corr = df_ts[numeric_cols].corr()\n"
        "plt.figure(figsize=(10, 8))\n"
        "sns.heatmap(corr, annot=False, cmap=\"vlag\", center=0)\n"
        "plt.title(\"Correlation heatmap (numeric features)\")\n"
        "plt.tight_layout()\n"
        "plt.show()",
    )

    add_py(
        nb,
        "# Resampled means as a smoother view\n"
        "sensor_cols = [\"Tp\", \"Cl\", \"pH\", \"Redox\", \"Leit\", \"Trueb\", \"Cl_2\", \"Fm\", \"Fm_2\"]\n"
        "window = \"1H\"\n"
        "df_roll = df_ts[sensor_cols].resample(window).mean()\n"
        "_ = df_roll.plot(subplots=False, figsize=(14,6), linewidth=1.2)\n"
        "plt.title(f\"Resampled mean ({window})\")\n"
        "plt.tight_layout()\n"
        "plt.show()",
    )

    add_py(
        nb,
        "# Save correlation heatmap to figures\n"
        "from pathlib import Path as _Path\n"
        "numeric_cols = df_ts.select_dtypes(include=[np.number]).columns.tolist()\n"
        "corr = df_ts[numeric_cols].corr()\n"
        "plt.figure(figsize=(10, 8))\n"
        "sns.heatmap(corr, annot=False, cmap=\"vlag\", center=0)\n"
        "plt.title(\"Correlation heatmap (numeric features)\")\n"
        "plt.tight_layout()\n"
        "out = _Path(FIGURES_DIR) / \"correlation_heatmap.png\"\n"
        "plt.savefig(out, dpi=150, bbox_inches=\"tight\")\n"
        "plt.show()\n"
        "print(\"Saved:\", out)",
    )

    add_md(
        nb,
        "## Resumo\n"
        "- `df_ts`: DataFrame limpo e indexado por tempo.\n"
        "- Visualizações: séries temporais com marcação de eventos, distribuições e correlação.\n"
        "- Figuras salvas em `reports/figures/`.",
    )

    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3"}

    return nb


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    out_path = project_root / "notebooks" / "02_visualizations_gecco2018.ipynb"
    nb = build_notebook()
    out_path.write_text(nbf.writes(nb))
    print("WROTE", out_path)


if __name__ == "__main__":
    main()



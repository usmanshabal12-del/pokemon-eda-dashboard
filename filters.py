"""
filters.py — Filter & Data Processing Functions
Pokemon EDA Dashboard
"""

import pandas as pd


def load_data(filepath: str = "data/pokemon.csv") -> pd.DataFrame:
    """Load and clean the Pokemon dataset."""
    df = pd.read_csv(filepath)

    # Rename '#' column to 'ID' for cleaner access
    df.rename(columns={"#": "ID"}, inplace=True)

    # Fill missing Type 2 with 'None'
    df["Type 2"] = df["Type 2"].fillna("None")

    # Ensure correct data types
    df["Legendary"] = df["Legendary"].astype(bool)
    df["Generation"] = df["Generation"].astype(int)

    return df


def apply_filters(
    df: pd.DataFrame,
    search_text: str = "",
    selected_type1: list = None,
    selected_type2: list = None,
    selected_generations: list = None,
    legendary_filter: str = "All",
    total_range: tuple = (0, 1000),
    hp_range: tuple = (0, 300),
    attack_range: tuple = (0, 300),
) -> pd.DataFrame:
    """
    Apply all filters to the dataframe and return filtered result.
    All charts must use this filtered dataframe.
    """
    filtered = df.copy()

    # 1. Search / Text Filter
    if search_text:
        filtered = filtered[
            filtered["Name"].str.contains(search_text, case=False, na=False)
        ]

    # 2. Category Filter — Type 1
    if selected_type1:
        filtered = filtered[filtered["Type 1"].isin(selected_type1)]

    # 3. Multi-Select Filter — Type 2
    if selected_type2:
        filtered = filtered[filtered["Type 2"].isin(selected_type2)]

    # 4. Multi-Select Filter — Generation
    if selected_generations:
        filtered = filtered[filtered["Generation"].isin(selected_generations)]

    # 5. Legendary Filter
    if legendary_filter == "Legendary Only":
        filtered = filtered[filtered["Legendary"] == True]
    elif legendary_filter == "Non-Legendary Only":
        filtered = filtered[filtered["Legendary"] == False]

    # 6. Numerical Range Slider — Total Stats
    filtered = filtered[
        (filtered["Total"] >= total_range[0]) & (filtered["Total"] <= total_range[1])
    ]

    # 7. Numerical Range Slider — HP
    filtered = filtered[
        (filtered["HP"] >= hp_range[0]) & (filtered["HP"] <= hp_range[1])
    ]

    # 8. Numerical Range Slider — Attack
    filtered = filtered[
        (filtered["Attack"] >= attack_range[0])
        & (filtered["Attack"] <= attack_range[1])
    ]

    return filtered


def get_kpi_stats(df: pd.DataFrame) -> dict:
    """Compute KPI summary card values from filtered dataframe."""
    return {
        "total_records": len(df),
        "avg_total": round(df["Total"].mean(), 1) if len(df) > 0 else 0,
        "avg_hp": round(df["HP"].mean(), 1) if len(df) > 0 else 0,
        "avg_attack": round(df["Attack"].mean(), 1) if len(df) > 0 else 0,
        "max_total": int(df["Total"].max()) if len(df) > 0 else 0,
        "min_total": int(df["Total"].min()) if len(df) > 0 else 0,
        "legendary_count": int(df["Legendary"].sum()) if len(df) > 0 else 0,
        "strongest_pokemon": df.loc[df["Total"].idxmax(), "Name"] if len(df) > 0 else "N/A",
    }

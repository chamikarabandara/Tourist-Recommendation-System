
import pandas as pd
from pathlib import Path

# Get the project root directory reliably
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "destination_features.csv"
)

def recommend_destinations(
    preferred_type=None,
    min_rating=0,
    top_n=5
):
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH}"
        )

    destinations = pd.read_csv(DATA_PATH)

    if preferred_type and preferred_type != "All":
        destinations = destinations[
            destinations["Location_Type"].str.casefold()
            == preferred_type.casefold()
        ]

    destinations = destinations[
        destinations["Average_Rating"] >= float(min_rating)
    ].copy()

    destinations["Recommendation_Score"] = (
        0.7 * destinations["Rating_Score"]
        + 0.3 * destinations["Review_Popularity"]
    )

    destinations = destinations.sort_values(
        "Recommendation_Score",
        ascending=False
    )

    return destinations.head(top_n).to_dict(orient="records")

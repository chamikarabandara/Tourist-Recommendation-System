
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

HOTEL_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "hotel_master.csv"
)

DESTINATION_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "destination_master.csv"
)

RESULT_COLUMNS = [
    "Name",
    "Type",
    "District",
    "Grade",
    "Rooms",
    "Address"
]


def empty_results(status):
    """Return an empty result with a reason for the application."""
    results = pd.DataFrame(columns=RESULT_COLUMNS)
    results.attrs["status"] = status
    return results


def recommend_hotels(
    destination_name,
    accommodation_type=None,
    top_n=5
):
    # Load datasets
    hotels = pd.read_csv(HOTEL_DATA_PATH)
    destinations = pd.read_csv(DESTINATION_DATA_PATH)

    # Find the selected destination
    destination = destinations[
        destinations["Location_Name"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        == str(destination_name).strip().casefold()
    ]

    if destination.empty:
        return empty_results("destination_not_found")

    destination_row = destination.iloc[0]

    district = destination_row.get("Mapped_District")
    city = str(destination_row.get("Located_City", "")).strip()

    # Do not recommend accommodations when district mapping is missing
    if pd.isna(district) or not str(district).strip():
        return empty_results("missing_district_mapping")

    # Filter accommodations by district
    results = hotels[
        hotels["District_Key"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.casefold()
        == str(district).strip().casefold()
    ].copy()

    # Apply accommodation type filter
    if (
        accommodation_type
        and accommodation_type.casefold()
        not in ["all", "all accommodation types"]
    ):
        results = results[
            results["Type"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.casefold()
            == accommodation_type.strip().casefold()
        ]

    if results.empty:
        return empty_results("no_accommodation_found")

    # Prepare text fields for matching
    address_text = (
        results["Address"].fillna("").astype(str).str.casefold()
    )
    name_text = (
        results["Name"].fillna("").astype(str).str.casefold()
    )

    destination_text = str(destination_name).strip().casefold()
    city_text = (
        city.casefold()
        if city and city.casefold() != "nan"
        else ""
    )

    # Match destination name and associated city
    destination_match = (
        address_text.str.contains(destination_text, regex=False)
        | name_text.str.contains(destination_text, regex=False)
    )

    city_match = pd.Series(False, index=results.index)

    if city_text:
        city_match = (
            address_text.str.contains(city_text, regex=False)
            | name_text.str.contains(city_text, regex=False)
        )

    # Prioritize destination matches, then city matches
    results["_Match_Priority"] = 0
    results.loc[city_match, "_Match_Priority"] = 1
    results.loc[destination_match, "_Match_Priority"] = 2

    # Use local text matches when available.
    # Otherwise, use district-level fallback results.
    local_matches = results[
        results["_Match_Priority"] > 0
    ].copy()

    if not local_matches.empty:
        results = local_matches

    # Remove duplicate accommodation names
    results = results.sort_values(
        "_Match_Priority",
        ascending=False
    )

    results = results.drop_duplicates(
        subset=["Name"],
        keep="first"
    )

    results = results[RESULT_COLUMNS].head(top_n).reset_index(drop=True)
    results.attrs["status"] = (
        "local_matches" if not local_matches.empty
        else "district_fallback"
    )

    return results

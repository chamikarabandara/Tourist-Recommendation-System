
from flask import Flask, render_template, request
from recommender import recommend_destinations
from hotel_recommender import recommend_hotels
from pathlib import Path
import pandas as pd

app = Flask(__name__)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"
DESTINATION_PATH = PROCESSED_DATA / "destination_master.csv"


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    selected_type = "All"
    min_rating = 4.0

    if request.method == "POST":
        selected_type = request.form.get("preferred_type", "All")
        min_rating = float(request.form.get("min_rating", 4.0))

        recommendations = recommend_destinations(
            preferred_type=selected_type,
            min_rating=min_rating,
            top_n=5
        )

    return render_template(
        "index.html",
        recommendations=recommendations,
        selected_type=selected_type,
        min_rating=min_rating
    )


@app.route("/hotels", methods=["GET", "POST"])
def hotels_page():
    hotel_results = []
    selected_accommodation_type = "All"
    selected_destination = request.args.get(
        "destination_name", ""
    ).strip()
    error_message = ""
    info_message = ""

    # Load destination names
    try:
        destinations_df = pd.read_csv(DESTINATION_PATH)
        destination_names = sorted(
            destinations_df["Location_Name"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )
    except (FileNotFoundError, KeyError, pd.errors.ParserError):
        destination_names = []
        error_message = (
            "Destination data could not be loaded. "
            "Please check destination_master.csv."
        )

    # Read form values
    if request.method == "POST":
        selected_destination = request.form.get(
            "destination_name", ""
        ).strip()
        selected_accommodation_type = request.form.get(
            "accommodation_type", "All"
        )

    # Search accommodation
    if selected_destination and not error_message:
        if selected_destination not in destination_names:
            error_message = "Please select a valid destination."
        else:
            try:
                results = recommend_hotels(
                    destination_name=selected_destination,
                    accommodation_type=selected_accommodation_type,
                    top_n=10
                )

                # Read result status before converting the DataFrame
                result_status = (
                    results.attrs.get("status", "")
                    if isinstance(results, pd.DataFrame)
                    else ""
                )

                if isinstance(results, pd.DataFrame):
                    hotel_results = results.to_dict(orient="records")
                else:
                    hotel_results = results or []

                # Show a specific message for each situation
                if result_status == "missing_district_mapping":
                    error_message = (
                        "Accommodation recommendations are currently "
                        "unavailable because this destination's district "
                        "mapping has not been verified."
                    )

                elif result_status == "destination_not_found":
                    error_message = (
                        "The selected destination could not be found "
                        "in the destination dataset."
                    )

                elif not hotel_results:
                    error_message = (
                        "No accommodation options were found for this "
                        "destination and accommodation type."
                    )

                elif result_status == "district_fallback":
                    info_message = (
                        "No accommodation matched the destination name "
                        "or associated city. These options are district-level "
                        "fallback results and may not be nearby."
                    )

            except FileNotFoundError:
                error_message = (
                    "Accommodation data could not be found. "
                    "Please check hotel_master.csv and related files."
                )

            except (KeyError, pd.errors.ParserError) as exc:
                error_message = (
                    "The accommodation data could not be processed. "
                    "Please check the dataset columns and file format."
                )

    return render_template(
        "hotels.html",
        hotel_results=hotel_results,
        destination_names=destination_names,
        selected_destination=selected_destination,
        selected_accommodation_type=selected_accommodation_type,
        error_message=error_message,
        info_message=info_message
    )


if __name__ == "__main__":
    app.run(debug=True)

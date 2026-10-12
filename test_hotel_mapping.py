
from app.hotel_recommender import recommend_hotels

test_destinations = [
    "Sinharaja Forest Reserve",
    "Udawalawe National Park",
    "Wilpattu National Park",
]

for destination in test_destinations:
    results = recommend_hotels(destination_name=destination, top_n=5)

    print(f"\nDestination: {destination}")

    if results.empty:
        print("PASS: No accommodation returned.")
    else:
        print("CHECK: Accommodation results were returned.")
        print(results)

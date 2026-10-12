# Personalized Tourist Destination and Accommodation Recommendation System for Sri Lanka Using Machine Learning

## 1. Project Overview

This project aims to develop a personalized tourist destination and accommodation recommendation system for Sri Lanka. The system helps users explore tourist destinations based on destination type and minimum rating. It also provides accommodation recommendations associated with selected destinations.

The system uses tourism-related datasets, data preprocessing, exploratory data analysis, feature engineering, and a recommendation approach based on destination ratings and review popularity. A Flask web application provides the user interface.

## 2. Project Objectives

- To explore and preprocess tourism-related datasets.
- To analyse tourist destinations using ratings, reviews, and destination categories.
- To develop a destination recommendation approach.
- To provide accommodation recommendations based on selected destinations.
- To develop a user-friendly web application using Flask.
- To evaluate the functionality of the implemented system.

## 3. Technologies Used

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Data Visualisation:** Matplotlib, Seaborn
- **Web Framework:** Flask
- **Frontend:** HTML and CSS
- **Development Environment:** Jupyter Notebook and Visual Studio Code
- **Version Control:** Git and GitHub

## 4. Datasets

The project uses tourism-related datasets containing information about:

- Tourist destination reviews and ratings
- Accommodation establishments
- Tourism activities and services
- Water sports centres

The review dataset contains 16,156 records and covers 76 destinations. The accommodation dataset contains 2,130 records.

The datasets are cleaned and processed before being used in the recommendation system.

## 5. Main Features

### Destination Recommendations

- Filter destinations by destination type.
- Set a minimum rating.
- Display the top five recommended destinations.
- Rank destinations using a score based on ratings and review popularity.

### Accommodation Recommendations

- Select a tourist destination.
- Filter accommodation by accommodation type.
- Display available accommodation information, including name, type, district, grade, rooms, and address.
- Display a warning when a destination's district mapping has not been verified.

### Web Application

The Flask application provides separate pages for destination recommendations and accommodation recommendations.

## 6. Recommendation Methodology

The destination recommendation score uses the following weighted formula:

**Recommendation Score = (0.7 × Rating Score) + (0.3 × Review Popularity)**

The rating score is normalised using the average destination rating. Review popularity is scaled relative to the maximum review count in the dataset.

The system ranks eligible destinations according to their recommendation scores.

Accommodation recommendations use destination district information and text matching against accommodation names and addresses. When no local text matches are available, district-level fallback results may be returned.

## 7. Project Structure

```text
Tourist_Recommendation_System/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── models/
├── app/
│   ├── app.py
│   ├── recommender.py
│   ├── hotel_recommender.py
│   ├── templates/
│   │   ├── index.html
│   │   └── hotels.html
│   └── static/
├── test_hotel_mapping.py
├── requirements.txt
├── README.md
└── report/
```

## 8. Installation and Setup

### Prerequisites

- Python 3
- Git
- Visual Studio Code (recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/chamikarabandara/Tourist-Recommendation-System.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Tourist_Recommendation_System
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Ensure that the required processed datasets are available in `data/processed/`.

## 9. Running the Application

From the project root directory, run:

```bash
python app/app.py
```

Open the following URL in a web browser:

```text
http://127.0.0.1:5000
```

Use the destination page to explore recommendations. Visit the accommodation page to search for accommodation options associated with a selected destination.

## 10. Testing and Evaluation

The final testing process reported nine passed checks covering:

- Destination dataset quality
- Rating and recommendation score ranges
- Destination recommendation outputs
- Accommodation recommendation outputs
- Missing district mappings
- Bentota address matching
- Peradeniya accommodation matching
- Flask application functionality
- Missing-mapping warning behaviour

These checks evaluate data quality and system functionality. They do not establish that the recommendations accurately reflect real users' preferences.

## 11. Limitations

- Recommendations are based on available dataset fields and a weighted scoring approach.
- The system does not yet establish personalised recommendations from individual user profiles or historical user preferences.
- Accommodation data does not contain a complete set of prices or verified geographic coordinates.
- Some destination district mappings remain unverified.
- Accommodation matches based on names and addresses do not guarantee that a property is the nearest to a destination.
- The evaluation results are based on the implemented tests and do not demonstrate real-world recommendation accuracy.

## 12. Future Improvements

- Incorporate user preferences and travel requirements.
- Improve destination-to-accommodation matching using verified geographic coordinates and distance calculations.
- Add accommodation price and availability information where reliable data is available.
- Improve recommendation evaluation using user preference data and appropriate ranking metrics.
- Enhance the interface and provide more detailed explanations for recommendations.

## 13. Conclusion

This project demonstrates the development of a tourism recommendation application for Sri Lanka using Python, data analysis techniques, a weighted destination scoring approach, and Flask. It provides a foundation for further improvements towards more personalised and geographically accurate tourist destination and accommodation recommendations.

# Movie Recommendation System

# Overview

This project fetches movie data from the TMDB (The Movie Database) API and converts it into a structured dataset using Python and Pandas. The dataset will be used to build a Machine Learning-based Movie Recommendation System.

---

# Features

- Fetch movie data from TMDB API
- Convert JSON response into Pandas DataFrame
- Store data in CSV and JSON formats
- Data cleaning and preprocessing
- Build a recommendation engine using Machine Learning
- Future deployment as a web application

---

# Tech Stack

- Python
- Pandas
- Requests
- TMDB API
- Python Dotenv
- Git & GitHub

---

# Project Structure

```text
Movie_Recommendation_System-ML/
│
├── Backend/
│   └── SRC/
│       └── ingestion/
│           └── Tmdb1_client.py
│
├── data/
│   ├── tmdb_response.csv
│   └── tmdb_response.json
│
├── requirements.txt
├── README.md
├── .gitignore
```

# Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd Movie_Recommendation_System-ML
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file and add:

```env
TMDB_API_KEY=your_tmdb_api_key
BASE_URL=https://api.themoviedb.org/3
```

---

# Run the Project

```bash
python Backend/SRC/ingestion/Tmdb1_client.py
```

---

# Output

The project generates:

- `tmdb_response.json` → Raw API response
- `tmdb_response.csv` → Structured movie dataset

---

# Future Improvements

- Data Cleaning
- Feature Engineering
- Content-Based Recommendation System
- Collaborative Filtering
- Streamlit Web App
- Cloud Deployment

---

# Author

Anjali Verma

AI & Data Science Student
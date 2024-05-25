import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def display_modal_info(top_countries):
    modal_window = tk.Toplevel()
    modal_window.title("Top Countries Information")
    
    # Hide the modal window initially
    modal_window.withdraw()
    
    # Create labels to display country information in the modal window
    for i, (country, r2_score) in enumerate(top_countries, 1):
        tk.Label(modal_window, text=f"Country {i}: {country}, R^2 score: {r2_score}").pack()

    # Show the modal window
    modal_window.deiconify()

try:
    df = pd.read_csv('./documents/time_series_covid19_confirmed_global(1).csv') 
    models = {}

    for country in df['Country/Region'].unique():
        country_df = df[df['Country/Region'] == country]

        if len(country_df) < 2:
            continue 

        X = country_df.index.values.reshape(-1, 1)  
        y = country_df.iloc[:, 4:].sum(axis=1).values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        models[country] = {'model': model, 'r2_score': r2}

    if not models:
        print("No countries with sufficient data points to compute R^2 score.")
    else:
        # Sort countries based on R^2 score
        sorted_countries = sorted(models.items(), key=lambda x: x[1]['r2_score'], reverse=True)

        # Get top three countries
        top_three_countries = sorted_countries[:3]

        print("Top three countries with the highest R^2 score:")
        for country, score in top_three_countries:
            print(f"Country: {country}, R^2 score: {score['r2_score']}")

        # Display top three countries in a modal window
        display_modal_info(top_three_countries)

except Exception as e:
    print("An error occurred:", e)

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from clustering import display_clustering_modal  # Import the function from clustering.py
from graph_analytics import display_graph_analytics_modal
import visualization

def display_modal_info(top_countries):
    modal_window = tk.Toplevel()
    modal_window.title("Top Countries Information")
    
    # Create labels to display country information in the modal window
    for i, (country, r2_score) in enumerate(top_countries, 1):
        tk.Label(modal_window, text=f"Country {i}: {country}, R^2 score: {r2_score}").pack()

def show_predictive_modeling():
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

def show_clustering():
    # Call the function to display clustering results in a modal
    display_clustering_modal()

def show_graph_analytics():
    # Functionality for Graph Analytics
    display_graph_analytics_modal(root)

def show_visualization():
    
    visualization.main()
    
    # Functionality for Visualization

# Create the main window
root = tk.Tk()
root.title("COVID-19 Analysis")

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

# Add buttons for each functionality
predictive_modeling_button = tk.Button(button_frame, text="Predictive Modeling", command=show_predictive_modeling)
predictive_modeling_button.pack(fill=tk.X, padx=10, pady=5)

clustering_button = tk.Button(button_frame, text="Clustering", command=show_clustering)
clustering_button.pack(fill=tk.X, padx=10, pady=5)

graph_analytics_button = tk.Button(button_frame, text="Graph Analytics", command=show_graph_analytics)
graph_analytics_button.pack(fill=tk.X, padx=10, pady=5)

visualization_button = tk.Button(button_frame, text="Visualization", command=show_visualization)
visualization_button.pack(fill=tk.X, padx=10, pady=5)

# Start the GUI event loop
root.mainloop()
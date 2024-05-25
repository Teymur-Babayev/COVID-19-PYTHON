import tkinter as tk
from tkinter import simpledialog
from tkinter import Toplevel
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def display_graph_analytics_modal(root):
    def get_country_names():
        country_of_interest = simpledialog.askstring("Country of Interest", "Enter the name of the country in question:")
        neighboring_countries = []
        for i in range(3):
            neighbor = simpledialog.askstring(f"Neighboring Country {i+1}", f"Enter the name of neighboring country {i+1}:")
            neighboring_countries.append(neighbor)

        return country_of_interest, neighboring_countries

    # Load the DataFrame
    df = pd.read_csv('./documents/time_series_covid19_confirmed_global(1).csv')

    # Get country names from user input
    country_of_interest, neighboring_countries = get_country_names()

    # Store the selected country names
    selected_countries = [country_of_interest] + neighboring_countries

    # Filter the dataset to include only the data for the selected countries
    selected_country_data = df[df['Country/Region'].isin(selected_countries)]

    # Create a dictionary to store the current number of infected people for each selected country
    current_infected = {}
    for country in selected_countries:
        country_data = selected_country_data[selected_country_data['Country/Region'] == country]
        if not country_data.empty:
            current_infected[country] = country_data.iloc[:, -1].sum()
        else:
            current_infected[country] = 0  # Assuming no data available means 0 infections

    # Create a bar graph to visualize the number of infected people for each selected country
    plt.figure(figsize=(12, 8))
    countries = list(current_infected.keys())
    values = list(current_infected.values())
    bar_width = 0.4  # Adjust the width of the bars
    plt.bar(range(len(countries)), values, color='skyblue', width=bar_width)
    plt.xlabel('Country')
    plt.ylabel('Current Infected')
    plt.title('Number of Current Infected People in Selected Countries')
    plt.xticks(range(len(countries)), countries, rotation=45)  # Set country names as tick labels

    # Add labels for each bar
    for i, infected_count in enumerate(values):
        plt.text(i, infected_count + 0.05 * max(values), str(infected_count), ha='center', fontsize=10, color='red')

    plt.tight_layout()

    # Create a modal window to display the graph
    modal_window = Toplevel(root)
    modal_window.title("Graph Analytics")
    modal_window.geometry("900x800")

    # Embed the matplotlib figure in the modal window
    canvas = FigureCanvasTkAgg(plt.gcf(), master=modal_window)  # plt.gcf() gets the current figure
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a toolbar for navigation
    toolbar = NavigationToolbar2Tk(canvas, modal_window)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Function to close the modal window
    def close_modal():
        modal_window.destroy()

    # Add a close button
    close_button = tk.Button(modal_window, text="Close", command=close_modal)
    close_button.pack()

    modal_window.protocol("WM_DELETE_WINDOW", close_modal)  # Handle window close button

# This code will only execute when the file is run directly, not when imported as a module
if __name__ == "__main__":
    root = tk.Tk()
    display_graph_analytics_modal(root)
    root.mainloop()

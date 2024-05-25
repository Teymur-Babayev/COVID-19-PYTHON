import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def display_clustering_modal():
    # Load the DataFrame
    df = pd.read_csv('./documents/time_series_covid19_confirmed_global(1).csv')

    # Check potential columns for 'Country/Region'
    potential_country_columns = [col for col in df.columns if 'Country/Region' in col]

    # Select the first potential column for 'Country/Region'
    country_region_column = potential_country_columns[0]

    # Ensure there are no leading/trailing spaces in column name
    country_region_column = country_region_column.strip()

    # Check for missing values in numeric columns
    print("\nMissing Values in Numeric Columns:")
    print(df.select_dtypes(include='number').isnull().sum())

    # Filter out non-numeric columns
    numeric_columns = df.select_dtypes(include='number')

    # Drop missing values before calculating variance
    numeric_columns.dropna(axis=1, inplace=True)

    # Group by 'Country/Region' and calculate variance
    variance_per_country = numeric_columns.groupby(df[country_region_column]).var().mean(axis=1)

    print("\nVariance per Country:")
    print(variance_per_country)

    # Find the country with the highest variance
    country_highest_variance = variance_per_country.idxmax()

    # Filter the dataset to include only the data for the country with the highest variance
    country_data = df[df[country_region_column] == country_highest_variance]

    # Specify the date for which you want to display the number of infections
    selected_date = '3/9/23'  # Change this to the desired date

    # Get the number of infections for the selected date
    infections_for_selected_date = country_data[selected_date].iloc[0]

    # Perform K-Means clustering
    X = country_data.iloc[:, 4:]  # Exclude non-numeric columns and 'Country/Region'
    inertia = []

    # Determine the best value of K through iteration
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    # Plot the Elbow method to find the best K
    plt.plot(range(1, 11), inertia)
    plt.title('Elbow Method')
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')

    # Annotate with the name of the country and the number of infections for the selected date
    annotation_text = f'Highest Variance: {country_highest_variance}\nInfections on {selected_date}: {infections_for_selected_date}'
    plt.text(0.5, 0.9, annotation_text, transform=plt.gca().transAxes, fontsize=12)

    plt.show()

    # Based on the Elbow Method, choose the optimal K and perform clustering
    optimal_k = 3  
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    country_data['Cluster'] = kmeans.fit_predict(X)

    # Analyze the clusters and observe trends over time
    cluster_trends = country_data.groupby('Cluster').mean().T
    print("\nCluster Trends:")
    print(cluster_trends)

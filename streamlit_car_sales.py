import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the colorblind palette globally
sns.set_palette("colorblind")
plt.style.use("seaborn-colorblind")

# Load data
@st.cache_data
def load_data():
    car_details = pd.read_csv('car_details_df.csv')
    price_cardetails = pd.read_csv('price_cardetails_df.csv')
    return car_details, price_cardetails

car_details, price_cardetails = load_data()
merged_df = pd.merge(car_details, price_cardetails, on='Car_ID', how='inner')

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data Analysis", "Car Recommendation AI"])

# Data Analysis Page
if page == "Data Analysis":
    st.title("Car Sales Data Analysis")
    
    analysis_options = [
        "Most Common Car Brands", "Brand and Models", "Brand and Transmission Types", "Most Popular Brand by Location",
        "Average Mileage per Fuel Type", "Basic Statistical Summary", "Most Common Transmission Type in Recent Years",
        "Top 10 Locations with Most Cars Listed", "Count of Cars by Fuel Type", "Common Price Range for Each Car Model",
        "Most Expensive Car Models", "Correlation Between Car Age and Price", "Average Price of Automatic vs Manual Cars",
        "Top 5 Brands with Highest Resale Values", "Engine Size vs Average Price", "Average Resale Value by Fuel Type",
        "Average Price by Car Brand", "Transmission Type vs Number of Cars", "Depreciation: Average Price of Cars by Age",
        "Car Brands with the Best Mileage-to-Price Ratio", "Number of Cars Sold Each Year", "Price Trends Over Years",
        "EV Distribution by Location", "Transmission Type in Each Location", "EV Listings by Year"
    ]
    
    selected_analysis = st.selectbox("Select an analysis", analysis_options)
    
    if selected_analysis == "Most Common Car Brands":
        top_brands = car_details['Brand'].value_counts().head(5)
        st.bar_chart(top_brands)
    
    elif selected_analysis == "EV Distribution by Location":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_location = ev_cars["Location"].value_counts()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=ev_by_location.index, y=ev_by_location.values, hue=ev_by_location.index, palette="colorblind", legend=False)
        plt.title("EV Distribution by Location")
        plt.xlabel("Location")
        plt.ylabel("Number of EVs")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())
    
    elif selected_analysis == "EV Listings by Year":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_year = ev_cars["Year"].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        sns.barplot(x=ev_by_year.index, y=ev_by_year.values, hue=ev_by_year.index, palette="colorblind", legend=False)
        plt.title("EV Listings by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of EVs")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

    # Add other analysis blocks here...

# Car Recommendation AI Page
elif page == "Car Recommendation AI":
    st.title("Car Recommendation AI")
    
    # User inputs
    st.sidebar.header("Filter Options")
    location = st.sidebar.selectbox("Preferred Location", merged_df['Location'].unique())
    brand = st.sidebar.selectbox("Preferred Brand", merged_df['Brand'].unique())
    transmission = st.sidebar.selectbox("Preferred Transmission", merged_df['Transmission'].unique())
    
    # Price range filter
    min_price = st.sidebar.slider("Minimum Price (USD)", int(merged_df['Price_USD'].min()), int(merged_df['Price_USD'].max()))
    max_price = st.sidebar.slider("Maximum Price (USD)", int(merged_df['Price_USD'].min()), int(merged_df['Price_USD'].max()))
    
    # Filter data based on user inputs
    filtered_df = merged_df[(merged_df['Location'] == location) & 
                            (merged_df['Brand'] == brand) & 
                            (merged_df['Transmission'] == transmission) & 
                            (merged_df['Price_USD'] >= min_price) & 
                            (merged_df['Price_USD'] <= max_price)]
    
    if not filtered_df.empty:
        st.write(f"Recommended Cars in {location} for {brand} with {transmission} transmission:")
        st.dataframe(filtered_df[['Model', 'Year', 'Mileage_km', 'Price_USD']])
    else:
        st.write("No cars match your criteria. Please adjust your filters.")

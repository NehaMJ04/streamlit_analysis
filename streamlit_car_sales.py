import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    elif selected_analysis == "Brand and Models":
        brand_model_df = car_details.groupby("Brand")["Model"].unique().reset_index()
        st.write(brand_model_df)
    elif selected_analysis == "Brand and Transmission Types":
        brand_transmission_df = car_details.groupby("Brand")["Transmission"].value_counts().unstack().fillna(0)
        st.write(brand_transmission_df)
    elif selected_analysis == "Most Popular Brand by Location":
        popular_brands_by_location = car_details.groupby(["Location", "Brand"]).size().reset_index(name="Count")
        popular_brands = popular_brands_by_location.loc[popular_brands_by_location.groupby("Location")["Count"].idxmax()]
        st.write(popular_brands)
    elif selected_analysis == "Average Mileage per Fuel Type":
        avg_mileage = car_details.groupby('Fuel_Type')['Mileage_km'].mean()
        st.bar_chart(avg_mileage)
    elif selected_analysis == "Basic Statistical Summary":
        st.write(price_cardetails.describe())
        st.write(car_details.describe())
    elif selected_analysis == "Most Common Transmission Type in Recent Years":
        recent_transmission = car_details[car_details['Year'] >= 2020]['Transmission'].value_counts()
        st.bar_chart(recent_transmission)
    elif selected_analysis == "Top 10 Locations with Most Cars Listed":
        top_locations = car_details['Location'].value_counts().head(10)
        st.bar_chart(top_locations)
    elif selected_analysis == "Count of Cars by Fuel Type":
        fuel_counts = merged_df["Fuel_Type"].value_counts()
        st.bar_chart(fuel_counts)
    elif selected_analysis == "Common Price Range for Each Car Model":
        st.write(merged_df.groupby("Model")["Price_USD"].describe())
    elif selected_analysis == "Most Expensive Car Models":
        expensive_models = merged_df.groupby("Model")["Price_USD"].mean().sort_values(ascending=False).head(10)
        st.write(expensive_models)
    elif selected_analysis == "Correlation Between Car Age and Price":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        st.write(merged_df[["Car_Age", "Price_USD"]].corr())
    elif selected_analysis == "Average Price of Automatic vs Manual Cars":
        avg_price_transmission = merged_df.groupby("Transmission")["Price_USD"].mean()
        st.bar_chart(avg_price_transmission)
    elif selected_analysis == "Top 5 Brands with Highest Resale Values":
        resale_values = merged_df.groupby("Brand")["Price_USD"].median().sort_values(ascending=False).head(5)
        st.bar_chart(resale_values)
    elif selected_analysis == "Engine Size vs Average Price":
        eng = merged_df.groupby("Engine_cc")["Price_USD"].mean()
        st.bar_chart(eng)
    elif selected_analysis == "Average Resale Value by Fuel Type":
        resale_values = merged_df.groupby("Fuel_Type")["Price_USD"].median()
        st.bar_chart(resale_values)
    elif selected_analysis == "Average Price by Car Brand":
        price_by_brand = merged_df.groupby("Brand")["Price_USD"].mean()
        st.bar_chart(price_by_brand)
    elif selected_analysis == "Transmission Type vs Number of Cars":
        transmission_counts = merged_df["Transmission"].value_counts()
        st.bar_chart(transmission_counts)
    elif selected_analysis == "Depreciation: Average Price of Cars by Age":
        age_price = merged_df.groupby("Car_Age")["Price_USD"].mean()
        st.line_chart(age_price)
    elif selected_analysis == "Car Brands with the Best Mileage-to-Price Ratio":
        merged_df["Mileage_to_Price"] = merged_df["Mileage_km"] / merged_df["Price_USD"].replace(0, 1)
        brand_mileage_price_ratio = merged_df.groupby("Brand")["Mileage_to_Price"].mean()
        st.bar_chart(brand_mileage_price_ratio)
    elif selected_analysis == "Number of Cars Sold Each Year":
        yearly_sales = car_details["Year"].value_counts()
        st.bar_chart(yearly_sales)
    elif selected_analysis == "EV Distribution by Location":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_location = ev_cars["Location"].value_counts()
        st.bar_chart(ev_by_location)
    elif selected_analysis == "EV Listings by Year":
        ev_by_year = ev_cars["Year"].value_counts()
        st.bar_chart(ev_by_year)

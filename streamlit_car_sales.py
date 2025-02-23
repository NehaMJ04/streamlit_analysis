import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            top_brands, 
            x=top_brands.index, 
            y=top_brands.values, 
            labels={'x': 'Brand', 'y': 'Number of Cars'},
            title="Most Common Car Brands",
            text=top_brands.values
        )
        fig.update_traces(marker_color='#1f77b4')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Count of Cars by Fuel Type":
        fuel_counts = merged_df["Fuel_Type"].value_counts()
        
        # Create an interactive pie chart with Plotly
        fig = px.pie(
            fuel_counts, 
            values=fuel_counts.values, 
            names=fuel_counts.index, 
            title="Count of Cars by Fuel Type"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            fuel_counts, 
            x=fuel_counts.index, 
            y=fuel_counts.values, 
            labels={'x': 'Fuel Type', 'y': 'Number of Cars'},
            title="Count of Cars by Fuel Type",
            text=fuel_counts.values
        )
        fig.update_traces(marker_color='#1f77b4')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Average Mileage per Fuel Type":
        avg_mileage = car_details.groupby('Fuel_Type')['Mileage_km'].mean()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            avg_mileage, 
            x=avg_mileage.index, 
            y=avg_mileage.values, 
            labels={'x': 'Fuel Type', 'y': 'Average Mileage (km)'},
            title="Average Mileage per Fuel Type",
            text=avg_mileage.values
        )
        fig.update_traces(marker_color='#1f77b4')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Car Brands with the Best Mileage-to-Price Ratio":
        merged_df["Mileage_to_Price"] = merged_df["Mileage_km"] / merged_df["Price_USD"].replace(0, 1)
        brand_mileage_price_ratio = merged_df.groupby("Brand")["Mileage_to_Price"].mean().sort_values(ascending=False).head(10)
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            brand_mileage_price_ratio, 
            x=brand_mileage_price_ratio.index, 
            y=brand_mileage_price_ratio.values, 
            labels={'x': 'Brand', 'y': 'Mileage per Unit Price'},
            title="Car Brands with the Best Mileage-to-Price Ratio",
            text=brand_mileage_price_ratio.values.round(2)
        )
        fig.update_traces(marker_color='#1f77b4')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the list of ratios
        st.write("Mileage-to-Price Ratios by Brand:")
        st.write(brand_mileage_price_ratio)
    
    elif selected_analysis == "Price Trends Over Years":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        age_price = merged_df.groupby("Car_Age")["Price_USD"].mean()
        
        # Create an interactive line chart with Plotly
        fig = px.line(
            age_price, 
            x=age_price.index, 
            y=age_price.values, 
            labels={'x': 'Car Age (Years)', 'y': 'Average Price (USD)'},
            title="Price Trends Over Years",
            markers=True
        )
        fig.update_traces(line_color='green')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "EV Distribution by Location":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_location = ev_cars["Location"].value_counts()
        
        # Create an interactive pie chart with Plotly
        fig = px.pie(
            ev_by_location, 
            values=ev_by_location.values, 
            names=ev_by_location.index, 
            title="EV Distribution by Location"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Transmission Type in Each Location":
        transmission_by_location = car_details.groupby(["Location", "Transmission"]).size().reset_index(name="Count")
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            transmission_by_location, 
            x="Location", 
            y="Count", 
            color="Transmission", 
            labels={'x': 'Location', 'y': 'Number of Cars'},
            title="Transmission Types in Each Location",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "EV Listings by Year":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_year = ev_cars["Year"].value_counts().sort_index()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            ev_by_year, 
            x=ev_by_year.index, 
            y=ev_by_year.values, 
            labels={'x': 'Year', 'y': 'Number of EVs'},
            title="EV Listings by Year",
            text=ev_by_year.values
        )
        fig.update_traces(marker_color='#1f77b4')  # Use a colorblind-friendly color
        st.plotly_chart(fig, use_container_width=True)

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
    filtered_df = merged_df[
        (merged_df['Location'] == location) & 
        (merged_df['Brand'] == brand) & 
        (merged_df['Transmission'] == transmission) & 
        (merged_df['Price_USD'] >= min_price) & 
        (merged_df['Price_USD'] <= max_price)
    ]
    
    if not filtered_df.empty:
        st.write(f"Recommended Cars in {location} for {brand} with {transmission} transmission:")
        st.dataframe(filtered_df[['Model', 'Year', 'Mileage_km', 'Price_USD']])
    else:
        st.write("No cars match your criteria. Please adjust your filters.")

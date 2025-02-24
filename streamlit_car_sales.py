import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.colors

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
            text=top_brands.values,
            color=top_brands.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly # Colorblind-friendly palette
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Brand and Models":
        brand_model_df = car_details.groupby("Brand")["Model"].unique().reset_index()
        
        # Display the data in a table
        st.write("Brand and Models:")
        st.dataframe(brand_model_df)
    
    elif selected_analysis == "Brand and Transmission Types":
        brand_transmission_df = car_details.groupby("Brand")["Transmission"].unique().reset_index()
        
        # Display the data in a table
        st.write("Brand and Transmission Types:")
        st.dataframe(brand_transmission_df)
    
    elif selected_analysis == "Most Popular Brand by Location":
        popular_brands_by_location = car_details.groupby(["Location", "Brand"]).size().reset_index(name="Count")
        popular_brands = popular_brands_by_location.loc[popular_brands_by_location.groupby("Location")["Count"].idxmax()]
        
        # Display the data in a table
        st.write("Most Popular Brand by Location:")
        st.dataframe(popular_brands)
    
    elif selected_analysis == "Average Mileage per Fuel Type":
        avg_mileage = car_details.groupby('Fuel_Type')['Mileage_km'].mean()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            avg_mileage, 
            x=avg_mileage.index, 
            y=avg_mileage.values, 
            labels={'x': 'Fuel Type', 'y': 'Average Mileage (km)'},
            title="Average Mileage per Fuel Type",
            text=avg_mileage.values.round(2),
            color=avg_mileage.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Basic Statistical Summary":
        st.write("Price Dataset Description:")
        st.write(price_cardetails.describe())
        
        st.write("Car Details Dataset Description:")
        st.write(car_details.describe())
    
    elif selected_analysis == "Most Common Transmission Type in Recent Years":
        recent_transmission = car_details[car_details['Year'] >= 2020]['Transmission'].value_counts()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            recent_transmission, 
            x=recent_transmission.index, 
            y=recent_transmission.values, 
            labels={'x': 'Transmission Type', 'y': 'Number of Cars'},
            title="Most Common Transmission Type in Recent Years",
            text=recent_transmission.values,
            color=recent_transmission.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Top 10 Locations with Most Cars Listed":
        top_locations = car_details['Location'].value_counts().head(10)
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            top_locations, 
            x=top_locations.index, 
            y=top_locations.values, 
            labels={'x': 'Location', 'y': 'Number of Cars'},
            title="Top 10 Locations with Most Cars Listed",
            text=top_locations.values,
            color=top_locations.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Count of Cars by Fuel Type":
        fuel_counts = merged_df["Fuel_Type"].value_counts()
        
        # Create an interactive pie chart with Plotly
        fig = px.pie(
            fuel_counts, 
            values=fuel_counts.values, 
            names=fuel_counts.index, 
            title="Count of Cars by Fuel Type",
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Common Price Range for Each Car Model":
        price_summary = merged_df.groupby("Model")["Price_USD"].describe()
        
        # Display the data in a table
        st.write("Common Price Range for Each Car Model:")
        st.dataframe(price_summary)
    
    elif selected_analysis == "Most Expensive Car Models":
        expensive_models = merged_df.groupby("Model")["Price_USD"].mean().sort_values(ascending=False).head(10)
        
        # Display the data in a table
        st.write("Most Expensive Car Models:")
        st.dataframe(expensive_models)
    
    elif selected_analysis == "Correlation Between Car Age and Price":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        correlation = merged_df[["Car_Age", "Price_USD"]].corr()
        
        # Display the correlation matrix
        st.write("Correlation Between Car Age and Price:")
        st.write(correlation)
    
    elif selected_analysis == "Average Price of Automatic vs Manual Cars":
        avg_price_transmission = merged_df.groupby("Transmission")["Price_USD"].mean()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            avg_price_transmission, 
            x=avg_price_transmission.index, 
            y=avg_price_transmission.values, 
            labels={'x': 'Transmission Type', 'y': 'Average Price (USD)'},
            title="Average Price of Automatic vs Manual Cars",
            text=avg_price_transmission.values.round(2),
            color=avg_price_transmission.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Top 5 Brands with Highest Resale Values":
        resale_values = merged_df.groupby("Brand")["Price_USD"].median().sort_values(ascending=False).head(5)
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            resale_values, 
            x=resale_values.index, 
            y=resale_values.values, 
            labels={'x': 'Brand', 'y': 'Median Resale Price (USD)'},
            title="Top 5 Brands with Highest Resale Values",
            text=resale_values.values.round(2),
            color=resale_values.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Engine Size vs Average Price":
        eng = merged_df.groupby("Engine_cc")["Price_USD"].mean()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            eng, 
            x=eng.index, 
            y=eng.values, 
            labels={'x': 'Engine Size (cc)', 'y': 'Average Price (USD)'},
            title="Engine Size vs Average Price",
            text=eng.values.round(2),
            color=eng.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Average Resale Value by Fuel Type":
        resale_values = merged_df.groupby("Fuel_Type")["Price_USD"].median()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            resale_values, 
            x=resale_values.index, 
            y=resale_values.values, 
            labels={'x': 'Fuel Type', 'y': 'Median Resale Price (USD)'},
            title="Average Resale Value by Fuel Type",
            text=resale_values.values.round(2),
            color=resale_values.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Average Price by Car Brand":
        price_by_brand = merged_df.groupby("Brand")["Price_USD"].mean()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            price_by_brand, 
            x=price_by_brand.index, 
            y=price_by_brand.values, 
            labels={'x': 'Brand', 'y': 'Average Price (USD)'},
            title="Average Price by Car Brand",
            text=price_by_brand.values.round(2),
            color=price_by_brand.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Transmission Type vs Number of Cars":
        transmission_counts = merged_df["Transmission"].value_counts()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            transmission_counts, 
            x=transmission_counts.index, 
            y=transmission_counts.values, 
            labels={'x': 'Transmission Type', 'y': 'Number of Cars'},
            title="Transmission Type vs Number of Cars",
            text=transmission_counts.values,
            color=transmission_counts.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "Depreciation: Average Price of Cars by Age":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        age_price = merged_df.groupby("Car_Age")["Price_USD"].mean()
        
        # Create an interactive line chart with Plotly
        fig = px.line(
            age_price, 
            x=age_price.index, 
            y=age_price.values, 
            labels={'x': 'Car Age (Years)', 'y': 'Average Price (USD)'},
            title="Depreciation: Average Price of Cars by Age",
            markers=True,
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
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
            text=brand_mileage_price_ratio.values.round(2),
            color=brand_mileage_price_ratio.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display the list of ratios
        st.write("Mileage-to-Price Ratios by Brand:")
        st.write(brand_mileage_price_ratio)
    
    elif selected_analysis == "Number of Cars Sold Each Year":
        yearly_sales = car_details["Year"].value_counts().sort_index()
        
        # Create an interactive bar chart with Plotly
        fig = px.bar(
            yearly_sales, 
            x=yearly_sales.index, 
            y=yearly_sales.values, 
            labels={'x': 'Year', 'y': 'Number of Cars'},
            title="Number of Cars Sold Each Year",
            text=yearly_sales.values,
            color=yearly_sales.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
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
            markers=True,
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif selected_analysis == "EV Distribution by Location":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_location = ev_cars["Location"].value_counts()
        
        # Create an interactive pie chart with Plotly
        fig = px.pie(
            ev_by_location, 
            values=ev_by_location.values, 
            names=ev_by_location.index, 
            title="EV Distribution by Location",
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
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
            barmode='group',
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
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
            text=ev_by_year.values,
            color=ev_by_year.index,  # Use color for better distinction
            color_discrete_sequence=plotly.colors.qualitative.Plotly  # Colorblind-friendly palette
        )
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

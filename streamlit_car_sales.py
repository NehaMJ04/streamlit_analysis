import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the colorblind palette globally
sns.set_palette("colorblind")  # Use Seaborn's colorblind-friendly palette

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
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(top_brands, color="#1f77b4")  # Use a colorblind-friendly color
    
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
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(avg_mileage, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Basic Statistical Summary":
        st.write("Price Dataset Description:")
        st.write(price_cardetails.describe())
        st.write("Car Details Dataset Description:")
        st.write(car_details.describe())
    
    elif selected_analysis == "Most Common Transmission Type in Recent Years":
        recent_transmission = car_details[car_details['Year'] >= 2020]['Transmission'].value_counts()
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(recent_transmission, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Top 10 Locations with Most Cars Listed":
        top_locations = car_details['Location'].value_counts().head(10)
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(top_locations, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Count of Cars by Fuel Type":
        fuel_counts = merged_df["Fuel_Type"].value_counts()
        
        # Create a pie chart with Seaborn's colorblind palette
        plt.figure(figsize=(8, 8))
        plt.pie(fuel_counts, labels=fuel_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("colorblind"))
        plt.title("Count of Cars by Fuel Type")
        st.pyplot(plt.gcf())
    
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
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(avg_price_transmission, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Top 5 Brands with Highest Resale Values":
        resale_values = merged_df.groupby("Brand")["Price_USD"].median().sort_values(ascending=False).head(5)
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(resale_values, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Engine Size vs Average Price":
        eng = merged_df.groupby("Engine_cc")["Price_USD"].mean()
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(eng, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Average Resale Value by Fuel Type":
        resale_values = merged_df.groupby("Fuel_Type")["Price_USD"].median()
        
        # Create a pie chart
        plt.figure(figsize=(4, 4))
        plt.pie(resale_values, labels=resale_values.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("colorblind"))
        plt.title("Average Resale Value by Fuel Type (Pie Chart)")
        st.pyplot(plt.gcf())
        
        # Create a bar chart
        st.bar_chart(resale_values, color="#1f77b4")
        st.write("Average Resale Value by Fuel Type (Bar Chart)")
    elif selected_analysis == "Average Price by Car Brand":
        price_by_brand = merged_df.groupby("Brand")["Price_USD"].mean()
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(price_by_brand, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Transmission Type vs Number of Cars":
        transmission_counts = merged_df["Transmission"].value_counts()
        
        # Create a pie chart with Seaborn's colorblind palette
        plt.figure(figsize=(8, 8))
        plt.pie(transmission_counts, labels=transmission_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("colorblind"))
        plt.title("Transmission Type vs Number of Cars")
        st.pyplot(plt.gcf())
    
    elif selected_analysis == "Depreciation: Average Price of Cars by Age":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        age_price = merged_df.groupby("Car_Age")["Price_USD"].mean()
        
        # Use Seaborn's colorblind palette for Streamlit's native line chart
        st.line_chart(age_price, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Car Brands with the Best Mileage-to-Price Ratio":
        merged_df["Mileage_to_Price"] = merged_df["Mileage_km"] / merged_df["Price_USD"].replace(0, 1)
        brand_mileage_price_ratio = merged_df.groupby("Brand")["Mileage_to_Price"].mean().sort_values(ascending=False).head(10)
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(brand_mileage_price_ratio, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Number of Cars Sold Each Year":
        yearly_sales = car_details["Year"].value_counts().sort_index()
        
        # Use Seaborn's colorblind palette for Streamlit's native bar chart
        st.bar_chart(yearly_sales, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "Price Trends Over Years":
        merged_df["Car_Age"] = 2024 - merged_df["Year"]
        age_price = merged_df.groupby("Car_Age")["Price_USD"].mean()
        
        # Use Seaborn's colorblind palette for Streamlit's native line chart
        st.line_chart(age_price, color="#1f77b4")  # Use a colorblind-friendly color
    
    elif selected_analysis == "EV Distribution by Location":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_location = ev_cars["Location"].value_counts()
        
        # Create a pie chart with Seaborn's colorblind palette
        plt.figure(figsize=(8, 8))
        plt.pie(ev_by_location, labels=ev_by_location.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("colorblind"))
        plt.title("EV Distribution by Location")
        st.pyplot(plt.gcf())
    
    elif selected_analysis == "Transmission Type in Each Location":
        transmission_by_location = car_details.groupby(["Location", "Transmission"]).size().reset_index(name="Count")
        
        # Create a Seaborn bar plot with the colorblind palette
        plt.figure(figsize=(12, 6))
        sns.barplot(x="Location", y="Count", hue="Transmission", data=transmission_by_location, palette="colorblind")
        plt.title("Transmission Types in Each Location")
        plt.xlabel("Location")
        plt.ylabel("Number of Cars")
        plt.xticks(rotation=45)
        plt.legend(title="Transmission Type")
        
        # Display the plot in Streamlit
        st.pyplot(plt.gcf())
    
    elif selected_analysis == "EV Listings by Year":
        ev_cars = car_details[car_details["Fuel_Type"].str.contains("Electric", case=False, na=False)]
        ev_by_year = ev_cars["Year"].value_counts().sort_index()
        
        # Create a bar chart with Seaborn's colorblind palette
        plt.figure(figsize=(10, 5))
        sns.barplot(x=ev_by_year.index, y=ev_by_year.values, palette="colorblind")
        plt.title("EV Listings by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of EVs")
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

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

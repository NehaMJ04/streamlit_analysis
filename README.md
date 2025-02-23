# Car Sales Analysis Dashboard

This project integrates **Google Colab analysis** with **Streamlit** to visualize car sales data.

## 🚀 Features
- Load and display **cleaned car sales data**
- **Interactive charts** for price trends, brand popularity, and mileage
- **LocalTunnel support** for running Streamlit in Google Colab

## 📌 How to Run in Google Colab
1. **Install dependencies**:  
   ```bash
   !pip install streamlit
   !npm install -g localtunnel
   ```
2. **Run Streamlit in the background**:  
   ```bash
   !streamlit run app.py &>/content/logs.txt &
   ```
3. **Expose the app using LocalTunnel**:  
   ```bash
   !npx localtunnel --port 8501
   ```
4. **Click the LocalTunnel link** to access your app.

## 📂 Folder Structure
```
streamlit_colab_analysis/
│-- app.py                # Streamlit app (Main File)
│-- car_sales_analysis.py  # Data Analysis Script from Colab
│-- cleaned_car_details_df.csv      # Cleaned CSV File 1
│-- cleaned_price_cardetails_df.csv # Cleaned CSV File 2
│-- requirements.txt      # Python dependencies
│-- README.md             # Project documentation
```

import streamlit as st
import pandas as pd

# Reading in the CO2 dataset
df = pd.read_csv("CO2_emission.csv")

# Removing columns I do not need for the dashboard
df = df.drop(columns=["country_code", "Indicator Name"], errors="ignore")

# Getting only the year columns
year_columns = [col for col in df.columns if col.isdigit()]

# Changing the dataset from wide format to long format
df_long = df.melt(
    id_vars=["Country Name", "Region"],
    value_vars=year_columns,
    var_name="Year",
    value_name="CO2"
)

# Basic cleaning
df_long = df_long.dropna()
df_long["Year"] = df_long["Year"].astype(int)

# Dashboard title
st.title("🌍 Global CO2 Emissions Dashboard")
st.write("This dashboard explores CO2 emissions per capita across different countries and regions.")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filters")

region = st.sidebar.selectbox(
    "Select Region",
    sorted(df_long["Region"].unique())
)

region_data = df_long[df_long["Region"] == region]

country = st.sidebar.selectbox(
    "Select Country",
    sorted(region_data["Country Name"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df_long["Year"].min()),
    int(df_long["Year"].max()),
    (2000, 2019)
)

# Filtering the data based on user choices
filtered_df = df_long[
    (df_long["Region"] == region) &
    (df_long["Country Name"] == country) &
    (df_long["Year"] >= year_range[0]) &
    (df_long["Year"] <= year_range[1])
]

# Main numbers at the top
if not filtered_df.empty:
    latest_value = filtered_df.sort_values("Year")["CO2"].iloc[-1]
    average_value = filtered_df["CO2"].mean()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Latest CO2 Value", round(latest_value, 2))

    with col2:
        st.metric("Average CO2 Value", round(average_value, 2))

# Line chart for selected country
st.subheader(f"CO2 Emissions Over Time for {country}")
st.line_chart(filtered_df.set_index("Year")["CO2"])

st.write(
    "This graph shows how CO2 emissions changed over time for the selected country. "
    "It helps compare whether emissions increased, decreased, or stayed fairly stable."
)

st.markdown("---")

# Bar chart for highest emitting countries
latest_year = df_long["Year"].max()

top_df = df_long[df_long["Year"] == latest_year] \
    .sort_values(by="CO2", ascending=False) \
    .head(10)

st.subheader(f"Top 10 Countries by CO2 Emissions in {latest_year}")
st.bar_chart(top_df.set_index("Country Name")["CO2"])

st.write(
    "This chart shows the countries with the highest CO2 emissions per capita in the latest year of the dataset."
)

st.markdown("---")

# Showing the filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)
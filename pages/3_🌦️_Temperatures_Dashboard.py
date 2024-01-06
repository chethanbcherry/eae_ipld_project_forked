# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st


# ----- Page configs -----
st.set_page_config(
    page_title="<Chethan Balappa> Portfolio",
    page_icon="📊",
)


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities (with some cleaning and modifications).")


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path)  # TODO: Ex 3.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id" Ex. 3.1. is asking in the comment to set the index column to "show_id" but that's an error copied from the 2nd project, you only need to put the data_path in the pd.read_csv() function, nothing else.Ex 3.1. I ask you to first load the dataset into a DataFrame, and after that to display its first 5 rows. So, make sure that the dataset is fully loaded into temps_df and you only apply the .head(5) to later display the 5 initial rows, but do not convert the temps_df DataFrame to only those 5 initial row

    if temps_df is not None:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df  # a Pandas DataFrame


temps_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----

# TODO: Ex 3.2: Create a new column called `AvgTemperatureCelsius` that contains the temperature in Celsius degrees.
temps_df["AvgTemperatureCelsius"] = round ((temps_df["AvgTemperatureFahrenheit"]-32)*5/9,1)       # uncomment this line to complete it


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 3.3: How many different cities are there? Provide a list of them.
unique_cities_list = temps_df['City'].unique()
num_unique_cities = len(unique_cities_list)

# TODO: Ex 3.4: Which are the minimum and maximum dates?
min_date = temps_df['Date'].min()
max_date =  temps_df['Date'].max()

# TODO:  Ex 3.5: What are the global minimum and maximum temperatures? Find the city and the date of each of them.


min_temp_row = temps_df.loc[temps_df['AvgTemperatureCelsius'].idxmin()]
max_temp_row = temps_df.loc[temps_df['AvgTemperatureCelsius'].idxmax()]

min_temp = min_temp_row['AvgTemperatureCelsius']
max_temp = max_temp_row['AvgTemperatureCelsius']

min_temp_city = min_temp_row['City']
min_temp_date = min_temp_row['Date']

max_temp_city = max_temp_row['City']
max_temp_date = max_temp_row['Date']



# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])
if unique_cities_list is not None:
    cols1[0].dataframe(pd.Series(unique_cities_list, name="Cities"), use_container_width=True)
else:
    cols1[0].write("⚠️ You still need to develop the Ex 3.3.")

if min_date is not None and max_date is not None:

    cols1[2].write("#")

    min_temp_text = f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C
    *{min_temp_city} on {min_temp_date}*
    """
    cols1[2].write(min_temp_text)

    cols1[2].write("#")

    max_temp_text = f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C
    *{max_temp_city} on {max_temp_date}*
    """
    cols1[2].write(max_temp_text)

else:
    cols1[2].write("⚠️ You still need to develop the Ex 3.5.")


# ----- Plotting the temperatures over time for the selected cities -----

st.write("##")
st.header("Comparing the Temperatures of the Cities")

if unique_cities_list is not None:
    # Getting the list of cities to compare from the user
    selected_cities = st.multiselect("Select the cities to compare:", unique_cities_list, default=["Buenos Aires", "Dakar"], max_selections=4)

    cols2 = st.columns([6, 1, 6])

    start_date = cols2[0].date_input("Select the start date:", pd.to_datetime("2009-01-01").date())     # Getting the start date from the user
    end_date = cols2[2].date_input("Select the end date:", pd.to_datetime("2018-12-31").date())         # Getting the end date from the user

else:
    st.subheader("⚠️ You still need to develop the Ex 3.3.")

if unique_cities_list is not None and len(selected_cities) > 0:

    c = st.container(border=True)

    # TODO: Ex 3.7: Plot the temperatures over time for the selected cities for the selected time period,
    # every city has to be its own line with a different color.

    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
        city_df = temps_df.query('City ==@city')             
        city_df_period = city_df.query('Date>@start_date & Date<@end_date')      
        plt.plot(city_df_period["Date"], city_df_period["AvgTemperatureCelsius"], label = f"Temperature of {city}")            
    plt.title(f"Temperature of {selected_cities}") 
    plt.xlabel("Timestamp")  
    plt.ylabel("Temperature ˚C")  

    plt.legend()

    plt.show()
    
    c.pyplot(fig)



    # TODO: Make a histogram of the temperature reads of a list of selected cities, for the selected time period, 
    # every city has to be its own distribution with a different color.

    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:          
        city_df=temps_df.query('City ==@city')        
        city_df_period = city_df.query('Date>@start_date & Date<@end_date')     
        plt.hist(city_df['AvgTemperatureCelsius'], bins=20, edgecolor='white', alpha=0.6, label=f'AVG °C in {city}')               

    plt.title(f' Histogram  {city} ({start_date} to {end_date})')  # TODO
    plt.xlabel('Temperature (°C)') # TODO
    plt.ylabel('Frequency') # TODO
    plt.legend()
    plt.show()

    c.pyplot(fig)










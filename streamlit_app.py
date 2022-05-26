import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Hello....')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(my_fruit_list)

#Display Fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  #streamlit.write('The user entered ', fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get infromation")
  else:
    fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)
    #just write the data to the screen -> streamlit.text(fruityvice_response.json()) 
    #Take the json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

 
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
# To fetch one data --> my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Allow end user to add a fruit to the list
fruit_choice = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding', fruit_choice)
my_cur.execute("INSERT INTO fruit_load_list (fruit_name) VALUES ('"+fruit_choice+"')")







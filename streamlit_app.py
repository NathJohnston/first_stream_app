# Import statements
import streamlit
import pandas
import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#choose the Fruit Name Column as the Index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Lets's add a pick list here so they can pick the fruit they want to include
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
# Pre-populate the list with some fruit
# streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on the page
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

# Create the repeatable code block Function
def get_fruitvice_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)   
   # take the json version of response and normalise it
   fruityvice_normalised = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalised

#New Section to display furuityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
   else:     
      # output it to the screen as a table
      back_from_function = get_fruitvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:
    streamlit.error()

streamlit.write('The user entered', fruit_choice)


#don't run anything past here while we troubleshoot
streamlit.stop()


# Move the Fruit Load List Query and Load into a Button Action
# streamlit.text("Hello from Snowflake:")
# streamlit.text("The fruit load list contains:")
streamlit.header("The fruit load list contains:")

#Snowflake-related functions
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("SELECT * FROM fruit_load_list")
      return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows = get_fruit_list()
   streamlit.dataframe(my_data_rows)

# Add a second textbox
add_my_fruit= streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)


# Adding data to the Snowflake table
# This code will not work correctlt
my_cur.execute("INSERT INTO fruit_load_list VALUES ('from steamlit')")

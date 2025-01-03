# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your customized smoothie!!
    """
)
# option =st.selectbox("What is your favorite fruit?", ('Banana','Strawberry','Peach'))
# st.write('Your favorite fruit is',option)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:"
    , my_dataframe)


if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string +=fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        sf_df=st.dataframe (data=smoothiefroot_response.json(), use_container_width = True)
    name_on_order = st.text_input('Name on Smoothie') 
    st.write('The name on your smoothie will be: ',name_on_order)
    
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    st.write(my_insert_stmt)
  
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert :
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! '+ name_on_order, icon="✅")


        
    #st.write(ingredients_string)


    

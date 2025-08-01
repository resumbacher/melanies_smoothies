# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """)

name_on_order=st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

#option=st.selectbox(
#    'What is your favourite fruit?',
#    ('Banana','Strawberries', 'Peaches'))

#st.write('Your favourite fruit is:',option)

cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
#my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
#st.data(dataframe(pd_df)
#st.stop()

ingredients_list=st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

#st.write(ingredients_list)
if ingredients_list:
    #st.text(ingredients_list)

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME']==fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', searchon, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response=requests.get("https://fruityvice.com/api/fruit/all" + fruit_chosen)
        #smoothiefroot_response=requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)
#alter table SMOOTHIES.PUBLIC.ORDERS add column name_on_order varchar(100);
    my_insert_stmt = """ 
    insert into smoothies.public.orders(ingredients, name_on_order) 
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    
    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")


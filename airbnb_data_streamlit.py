import streamlit as st
import pandas as pd
import folium 
from streamlit_folium import st_folium
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

st.set_page_config(page_title= "Airbnb",
                   page_icon= '🏨',
                   layout= "wide",
                   initial_sidebar_state='expanded')   



table=pd.read_csv("Airbnb_data.csv")


countryname=[]
country_list=table["country"].unique()
for i in country_list:
    countryname.append(i)

roomtype=[]
room_list=table["room_type"].unique()
for i in room_list:
     roomtype.append(i)
    
    
def country(country_name):
    country=table[table["country"]==country_name]
    return country
def display_info(country,lat,long):
    details=country[(country["latitude"]==lat) & (country["longitude"]==long)]
    return(details)
def map(name):
    map=folium.Map(location=[name.latitude.mean(),name.longitude.mean()],zoom_start=12)
    for index, location_info in name.iterrows():
       popup_content = f"latitude: {location_info['latitude']}<br>"
       popup_content += f"longitude: {location_info['longitude']}<br>"
       popup_content += f"Room Type: {location_info['room_type']}<br>"
       popup_content += f"Review Score: {location_info['review_scores']}<br>"
       popup_content += f"Price: {location_info['price']}"
       folium.Marker([location_info["latitude"], location_info["longitude"]],popup=folium.Popup(popup_content, max_width=300),icon=folium.Icon(icon="glyphicon glyphicon-home")).add_to(map)
    return(map) 
def avg_country_price(colour):
     con_price=table.groupby("country")["price_usd"].mean().to_frame().reset_index()
     fig=px.bar(con_price,x='country',y='price_usd')
     fig.update_traces(marker_color=colour)
     fig.update_layout(width=400,height=250)
     return fig
def avg_roomtype_price(country_name,colour):
    if country_name!='all':
        room_con=table[table["country"].isin(country_name)]
        room_con_price=room_con.groupby(["country","room_type"])["price_usd"].mean().to_frame().reset_index()
        fig1=px.bar(room_con_price,x="room_type",y='price_usd',color='country',barmode='group',height=400)
        fig1.update_layout(width=400,height=350)
        fig1.update_traces(marker_color=colour)
        return fig1     
    else:   
      room_con_price=table.groupby(["country","room_type"])["price_usd"].mean().to_frame().reset_index()
      fig1=px.bar(room_con_price,x="room_type",y='price_usd',color='country',barmode='group',height=400)
      fig1.update_layout(width=400,height=350)
      return fig1
def avg_property_price(country_name,room_type):
    if country_name!='all' and room_type=='all':
        property_con=table[table["country"].isin(country_name)]
        property_con_price=property_con.groupby(["country","property_type"])["price_usd"].mean().to_frame().reset_index()
        fig2=px.bar(property_con_price,x="property_type",y='price_usd',color='country',barmode='group',height=400)
        fig2.update_layout(width=400,height=350)
        
        return fig2
    elif country_name!='all' and room_type!='all':
        property_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        property_con_price=property_con.groupby(["country","room_type","property_type"])["price_usd"].mean().to_frame().reset_index() 
        fig2=px.bar(property_con_price,x="property_type",y='price_usd',color='country',barmode='group',height=400)
        fig2.update_layout(width=400,height=350)
        
        return fig2
    else:   
      property_con_price=table.groupby(["country","property_type"])["price_usd"].mean().to_frame().reset_index()
      fig2=px.bar(property_con_price,x="property_type",y='price_usd',color='country',barmode='group',height=400)
      fig2.update_layout(width=400,height=350)
      return fig2 
def min_max_price(country_name,room_type):
    if country_name!='all' and room_type=='all':
        min_max_con=table[table["country"].isin(country_name)]
        min_max_price=min_max_con.groupby(["country"])["price_usd"].agg(['max','min']).reset_index()
        fig3=px.box(min_max_price,x="country",y=['max','min'],color='country',height=400)
        fig3.update_layout(width=400,height=350)
        return fig3
    elif country_name!='all' and room_type!='all':
        min_max_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        min_max_price=min_max_con.groupby(["country","room_type"])["price_usd"].agg(['max','min']).reset_index() 
        fig3=px.box(min_max_price,x="country",y=['max','min'],color='country',height=400)
        fig3.update_layout(width=400,height=350)
        return fig3
    else:   
      min_max_price=table.groupby(["country"])["price_usd"].agg(['max','min']).reset_index()
      fig3=px.box(min_max_price,x="country",y=['max','min'],color='country',height=400)
      fig3.update_layout(width=400,height=350)
      return fig3 
def reviews_price(country_name,room_type):
    if country_name!='all' and room_type=='all':
        review_con=table[table["country"].isin(country_name)]
        fig4=px.scatter(review_con,x="number_of_reviews",y="price_usd",color='country',height=400)
        fig4.update_layout(width=400,height=350)
        return fig4
    elif country_name!='all' and room_type!='all':
        review_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        fig4=px.scatter(review_con,x="number_of_reviews",y="price_usd",color='country',height=400)
        fig4.update_layout(width=400,height=350)
        return fig4
    else:   
      fig4=px.scatter(table,x="number_of_reviews",y="price_usd",color='country',height=400)
      fig4.update_layout(width=400,height=350)
      return fig4 
def availability_location(country_name,room_type):
    if country_name!='all' and room_type=='all':
        ava_con=table[table["country"].isin(country_name)]
        fig5=px.box(ava_con,x="country",y="availability_365",color='country',height=400)
        fig5.update_layout(width=400,height=350)
        return fig5
    elif country_name!='all' and room_type!='all':
        ava_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        fig5=px.box(ava_con,x="country",y="availability_365",color='country',height=400)
        fig5.update_layout(width=400,height=350)
        return fig5
    else:   
      fig5=px.box(table,x="country",y="availability_365",color='country',height=400)
      fig5.update_layout(width=400,height=350)
      return fig5 
def Top_host(country_name,room_type):
    if country_name!='all' and room_type=='all':
        host_con=table[table["country"].isin(country_name)]
        host_table=host_con[["_id","country","host_name","number_of_reviews","availability_365","review_scores"]]
        table1= host_table.sort_values(by=["number_of_reviews"],ascending=False).head(5)
        return table1
    elif country_name!='all' and room_type!='all':
        host_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        host_table=host_con[["_id","country","host_name","number_of_reviews","availability_365","review_scores"]]
        table1= host_table.sort_values(by=["number_of_reviews"],ascending=False).head(5)
        return table1
    else:   
        host_table=table[["_id","country","host_name","number_of_reviews","availability_365","review_scores"]]
        table1= host_table.sort_values(by=["number_of_reviews"],ascending=False).head(5)
        return table1
def total_host(country_name,room_type,colour):
    if country_name!='all' and room_type=='all':
        host_total=table[table["country"].isin(country_name)]
        count=len(host_total["host_name"].unique())
        data_card1=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card1.update_layout(width=70,height=100)
        return data_card1
    elif country_name!='all' and room_type!='all':
        host_total=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        count=len(host_total["host_name"].unique())
        data_card1=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card1.update_layout(width=70,height=100)
        return data_card1
    else:   
        count=len(table["host_name"].unique())
        data_card1=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card1.update_layout(width=70,height=100)
        return data_card1
def total_reviews(country_name,room_type,colour):
    if country_name!='all' and room_type=='all':
        reviews_total=table[table["country"].isin(country_name)]
        total=reviews_total["number_of_reviews"].sum()
        data_card2=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=total,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card2.update_layout(width=100,height=100)
        return data_card2
    elif country_name!='all' and room_type!='all':
        reviews_total=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        total=reviews_total["number_of_reviews"].sum()
        data_card2=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=total,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card2.update_layout(width=100,height=100)
        return data_card2
    else:   
        reviews_total=table[["_id","country","host_name","number_of_reviews","availability_365",]]
        total=reviews_total["number_of_reviews"].sum()
        data_card2=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=total,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card2.update_layout(width=100,height=100)
        return data_card2
def review_score(country_name,room_type):
    if country_name!='all' and room_type=='all':
        review_con=table[table["country"].isin(country_name)]
        table2=review_con.groupby('review_scores')['number_of_reviews']. sum().to_frame().reset_index().sort_values(by=["number_of_reviews"], ascending =False).head(10)
        return table2
    elif country_name!='all' and room_type!='all':
        review_con=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        table2= review_con.groupby('review_scores')['number_of_reviews']. sum().to_frame().reset_index().sort_values(by=["number_of_reviews"], ascending =False).head(10)
        return table2
    else:   
        table2= table.groupby('review_scores')['number_of_reviews']. sum().to_frame().reset_index().sort_values(by=["number_of_reviews"], ascending =False).head(10)
        return table2
def room_type(country_name,room_type,colour):
    if country_name!='all' and room_type=='all':
        room_total=table[table["country"].isin(country_name)]
        count= room_total["room_type"].count()
        data_card3=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card3.update_layout(width=70,height=100)
        return data_card3
    elif country_name!='all' and room_type!='all':
        room_total=table[(table["country"].isin(country_name))& (table["room_type"].isin(room_type))  ]
        count=room_total["room_type"].count()
        data_card3=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card3.update_layout(width=70,height=100)
        return data_card3
    else:   
        count=table["room_type"].count()
        data_card3=go.Figure(go.Indicator(
        mode="number",
        number={'font':{'size':30,'color':colour}},
        value=count,
        domain={'x': [0, 1], 'y': [0, 1]}))
        data_card3.update_layout(width=70,height=100)
        return data_card3
page = st.sidebar.selectbox("Select", ["About","Airbnb_listing","Data visualization"], index=0)
if page=="About":
  
  aa=Image.open("airbnb.png")
  st.image(aa)
  st.title("Welcome to the Airbnb listing and Data Visualization  tool")
  if st.button("Overview"):
      
    st.write(''' The Airbnb listing and  Data Visualization  tool is a user-friendly
             web application built to visualize and explore data 
             elated to booking  processed through Airbnb.Leveraging the power of Streamlit and Plotly,Folium.This tool provides an interactive and intuitive interface 
             for users to gain insights into Airbnb listings data and trends.''')
    st.header("Key Features")
    st.markdown(''' 
                - Airbnb Listing 
                - Data Visualization
                - User-Friendly Interface
                - Customization
                - Insightful Analytics''')
    st.header("Technology List ")
    st.markdown(''' 
                - Python
                - Plotly
                - Folium
                - Mongodb
                - Streamlit''')
    st.header("Tutorial")
    st.write('''To start exploring listing data with 
             the Airbnb Data Visualization and Exploration tool, 
             simply navigate through the various visualization options 
             available in the sidebar menu. Use the provided filters to 
             customize your analysis and gain valuable insights into 
             airbnb trends and patterns.''') 
if page=="Airbnb_listing": 
        with st.sidebar:
                st.title('Airbnb_listing')
                selected_country=st.selectbox('select a country',countryname, index=None)
                country_table=country(selected_country)
                filter_option=st.selectbox('Action',("show listing","apply filter"),index=None)
                if filter_option=="apply filter":
                                selected_minimum_price= st.number_input("Minimum_price", min_value=int(country_table["price"].min()),value=int(country_table["price"].min()) )
                                selected_maximum_price= st.number_input("Maximum_price", max_value=int(country_table["price"].max()),value=int(country_table["price"].max()) )
                                selected_room_type=st.multiselect('Select a Room Type',roomtype)
                                propertytype=[]
                                property_list=country_table["property_type"].unique()
                                for i in property_list:
                                    propertytype.append(i)
                                selected_property_type=st.multiselect('Select a Property Type',propertytype)
                                selected_min_review= st.number_input("Minimum Review Score", min_value=country_table["review_scores"].min(),value=country_table["review_scores"].min())
                                selected_max_review= st.number_input("Maximum Review Score", max_value=country_table["review_scores"].max(),value=country_table["review_scores"].max())
                                selected_bedroom_min= st.number_input("Minimum bedrooms", min_value=country_table["bedrooms"].min(), value=country_table["bedrooms"].min())
                                selected_bedroom_max= st.number_input("Maximum bedrooms", max_value=country_table["bedrooms"].max(), value=country_table["bedrooms"].max())
                                selected_beds_min= st.number_input("Minimum beds", min_value=country_table["beds"].min(),value=country_table["beds"].min())
                                selected_beds_max= st.number_input("Maximum beds",max_value=country_table["beds"].max(),value=country_table["beds"].max())
                                selected_bathrooms_min= st.number_input("Minimum bathrooms", min_value=country_table["bathrooms"].min(),value=country_table["bathrooms"].min())
                                selected_bathrooms_max= st.number_input("Maximum bathrooms",max_value=country_table["bathrooms"].max(),value=country_table["bathrooms"].max())
                                availabilty_list = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
                                selected_availability = st.selectbox('Select a availability days',availabilty_list,index=0 )
                                if selected_availability=='availability_30':
                                    selected_days_min= st.number_input("Minimum number of days", min_value=0, value=0)
                                    selected_days_max= st.number_input("Maximum number of days",max_value=30, value=0)
                                elif selected_availability=='availability_60':
                                    selected_days_min= st.number_input("Minimum number of days", min_value=0, value=0)
                                    selected_days_max= st.number_input("Maximum number of days",max_value=60, value=60)
                                elif selected_availability=='availability_90':
                                    selected_days_min= st.number_input("Minimum number of days", min_value=0, value=0)
                                    selected_days_max= st.number_input("Maximum number of days",max_value=90, value=90)
                                elif selected_availability=='availability_365':
                                    selected_days_min= st.number_input("Minimum number of days", min_value=0, value=0)
                                    selected_days_max= st.number_input("Maximum number of days",max_value=365, value=365)             
        if selected_country is not None and filter_option=="apply filter":
          if selected_room_type  and selected_property_type :
             filter_table=country_table[(country_table["price"].between(selected_minimum_price,selected_maximum_price))& country_table['room_type'].isin(selected_room_type) & country_table['property_type'].isin(selected_property_type) &
                                    country_table["review_scores"].between(selected_min_review,selected_max_review)& (country_table["bedrooms"].between(selected_bedroom_min,selected_bedroom_max)) & (country_table["beds"].between(selected_beds_min,selected_beds_max)) &
                                    (country_table["bathrooms"].between(selected_bathrooms_min,selected_bathrooms_max))&(country_table[selected_availability].between(selected_days_min,selected_days_max))] 
             map_filter_listing = map(filter_table)
             st_folium(map_filter_listing, width=1000,height=550)
             st.markdown("please select location in Map then enter the latitude & longitude to get full details about location")
             lat=st.number_input("Enter the latitude value", value=0.00000)
             long=st.number_input("Enter the longitude value", value=0.00000)
             detail_data=display_info(country_table,lat,long)
             if len(detail_data)!=0:
                   st.table(detail_data)
         
        elif selected_country is not None and filter_option=="show listing":
              map_listing = map(country_table) 
              st_folium(map_listing, width=1000,height=550)
              st.markdown("please select location in Map then enter the latitude & longitude to get full details about location")
              lat=st.number_input("Enter the latitude value", value=0.00000)
              long=st.number_input("Enter the longitude value", value=0.00000)
              detail_data=display_info(country_table,lat,long)
              if len(detail_data)!=0:
                    st.table(detail_data)
                   
if page=="Data visualization":
  with st.sidebar:
    selected_country=st.multiselect('select a country',countryname)
    selected_room_type=st.multiselect('Select a Room Type',roomtype)
    color_theme_list = ['blue', 'tan', 'green', 'HotPink', 'Indigo', 'steelblue', 'red', 'orange', 'aqua',"Reds"]
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list,index=0)
  col=st.columns((4.5,4.5),gap='medium')
  with col[0]:
    st.markdown("Avg Price by Country in USD")
    graph1=avg_country_price(selected_color_theme)
    st.plotly_chart(graph1)
    if selected_country and len(selected_room_type)==0 :
        st.markdown("Room_type Count")
        graph11=room_type(selected_country,"all",selected_color_theme)
        st.plotly_chart(graph11) 
        st.markdown("Avg Price by RoomType in USD")
        graph2=avg_roomtype_price(selected_country,selected_color_theme)
        st.plotly_chart(graph2)    
        st.markdown("Avg Price by propertyType in USD")
        graph3=avg_property_price(selected_country,'all')
        st.plotly_chart(graph3) 
        st.markdown("Minimum&Maximum Price by country")
        graph4=min_max_price(selected_country,'all')
        st.plotly_chart(graph4)   
    elif selected_country and selected_room_type:
        st.markdown("Room_type count")
        graph11=room_type(selected_country,selected_room_type,selected_color_theme)
        st.plotly_chart(graph11)
        st.markdown("Avg Price by RoomType in USD")
        graph2=avg_roomtype_price(selected_country,selected_color_theme)
        st.plotly_chart(graph2)
        st.markdown("Avg Price by propertyType in USD")
        graph3=avg_property_price(selected_country,selected_room_type)
        st.plotly_chart(graph3)
        st.markdown("Minimum&Maximum Price by country& roomtype")
        graph4=min_max_price(selected_country,selected_room_type)
        st.plotly_chart(graph4)   
          
    else:
        st.markdown("Room Type Count")
        graph11=room_type('all',"all",selected_color_theme)
        st.plotly_chart(graph11)
        st.markdown("Avg Price by RoomType in USD")
        graph2=avg_roomtype_price("all",selected_color_theme)
        st.plotly_chart(graph2)
        st.markdown("Avg Price by propertyType in USD")
        graph3=avg_property_price('all','all')
        st.plotly_chart(graph3)
        st.markdown("Minimum&Maximum Price by country")
        graph4=min_max_price('all','all')
        st.plotly_chart(graph4)
  with col[1]:
       if selected_country and len(selected_room_type)==0 :
        st.markdown("Number of Reviews vs Price")
        graph5=reviews_price(selected_country,"all")
        st.plotly_chart(graph5)
        st.markdown("Availability by country")
        graph6=availability_location(selected_country,"all")
        st.plotly_chart(graph6)
        st.markdown("Busiest Host")
        graph7=Top_host(selected_country,"all")
        st.table(graph7)
        col=st.columns((1.5,1.5),gap='medium')
        with col[0]:
            st.markdown("Host Count")
            graph8=total_host(selected_country,"all",selected_color_theme)
            st.plotly_chart(graph8)
        with col[1]:
            st.markdown("Review Count")
            graph9=total_reviews(selected_country,"all",selected_color_theme)
            st.plotly_chart(graph9)
        st.markdown("review_scores")
        graph10=review_score(selected_country,"all")
        st.table(graph10) 
                
       elif selected_country and selected_room_type:
        st.markdown("Number of Reviews vs Price")
        graph5=reviews_price(selected_country,selected_room_type)
        st.plotly_chart(graph5)
        st.markdown("Availability by country")
        graph6=availability_location(selected_country,selected_room_type)
        st.plotly_chart(graph6)
        st.markdown("Busiest Host")
        graph7=Top_host(selected_country,selected_room_type)
        st.table(graph7)
        col=st.columns((1.5,1.5),gap='medium')
        with col[0]: 
            st.markdown("Host count")
            graph8=total_host(selected_country,selected_room_type,selected_color_theme)
            st.plotly_chart(graph8)
        with col[1]: 
            st.markdown("Review count")
            graph9=total_reviews(selected_country,selected_room_type,selected_color_theme)
            st.plotly_chart(graph9) 
        st.markdown("Reviews_scores")
        graph10=review_score(selected_country,selected_room_type)
        st.table(graph10)
                
       else:
        st.markdown("Number of Reviews vs Price")
        graph5=reviews_price("all",'all')
        st.plotly_chart(graph5)
        st.markdown("Availability by country")
        graph6=availability_location('all',"all")
        st.plotly_chart(graph6)
        st.markdown("Busiest Host")
        graph7=Top_host('all',"all")
        st.table(graph7)   
        col=st.columns((1,1),gap='medium')
        with col[0]: 
            st.markdown("Host Count")
            graph8=total_host('all',"all",selected_color_theme)
            st.plotly_chart(graph8)
        with col[1]: 
            st.markdown("Review Count")
            graph9=total_reviews('all',"all",selected_color_theme)
            st.plotly_chart(graph9)
        st.markdown("Review Score")
        graph10=review_score('all',"all")
        st.table(graph10) 
       
    
    
        
             
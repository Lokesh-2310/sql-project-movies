import streamlit as st
import pandas as pd
import numpy as np
from dbhelper import MyDatabase
import requests
from PIL import Image
from io import BytesIO

db=MyDatabase()

st.set_page_config(page_title='Movies Here', page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)

user_choice=st.sidebar.selectbox('Select option',['Select','Top Movies','Genre','Released Year','By director name','About Project'])

if user_choice=='Select':
    st.header("""
    "The whole aspect of cinema and film festivals should be a moment to come together and celebrate art and humanity." 
    """)

elif user_choice=='Top Movies':
    url,name,year,score,votes,gross=db.overall_top_movies()
    df=pd.DataFrame({'Url':url,'Movie Name':name,'Released Year':year,'MetaScore':score,'Votes':votes,'Gross':gross}).sort_values(by='MetaScore',ascending=False)
    df=df[df['MetaScore']>85]
    size=df.shape[0]
    i=0
    st.header("Top {} Movies Collections".format(size))
    while(i!=size):
        col1,col2=st.columns(2)
        with col1:
            try:
                response = requests.get(df.iloc[i,0])
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                st.image(image, caption='Poster',width=150)
            except Exception as e:
                st.text(f"No image found")
            st.write("Movie Name: " + df.iloc[i, 1])
            st.write("Released Year: "+str(df.iloc[i,2]))
            st.write("MetaScore: " + str(df.iloc[i, 3]))
        with col2:
            if i!=size:
                try:
                    response = requests.get(df.iloc[i+1, 0])
                    response.raise_for_status()
                    image = Image.open(BytesIO(response.content))
                    st.image(image, caption='Poster', width=150)
                except Exception as e:
                    st.text(f"No image found")
                st.write("Movie Name: "+df.iloc[i+1, 1])
                st.write("Released Year: " + str(df.iloc[i + 1, 2]))
                st.write("MetaScore: " + str(df.iloc[i+1, 3]))
        st.divider()
        i=i+2



elif user_choice=='Genre':
    st.header("Genre")
    sub_choice=st.sidebar.selectbox("On which basis?",['Select','Released Year','Top Movie in Genre'])


    if user_choice=='Genre' and sub_choice=='Select':
        genres = db.get_genre()
        options = st.multiselect(
            'Choose the genres',
            genres,
            ['Drama'],
            placeholder="You can choose upto 3 genres",
            max_selections=3
        )
        if len(options)==0:
            st.subheader("Please select one genre")
        else:
            movie_name,genre_name,runtime=db.get_movie_list_by_genre(options)
            num=len(movie_name)
            st.subheader("{} Result Found !".format(num))
            dic={'Movie Name':movie_name,'Genre':genre_name,'Runtime(in hrs)':runtime}
            df=pd.DataFrame(dic,index=range(1,len(movie_name)+1))
            df=df.sort_values(by=['Movie Name','Runtime(in hrs)'])
            df.insert(0,column='S.No',value=range(1,len(movie_name)+1))
            # df.rename(columns={'level_0':'S.No'})
            st.dataframe(df,use_container_width=True,hide_index=True)



    elif user_choice=='Genre' and sub_choice=='Released Year':
        col1,col2=st.columns(2)
        year_list=db.get_year()
        genre_list=db.get_genre()
        year=None
        genre=None
        with col1:
            genre=st.selectbox("Choose the genre:",genre_list)
        with col2:
            year = st.selectbox("Choose the year:",year_list)

        name,time=db.get_year_genre_movie(genre,int(year))
        if len(name)==0:
            st.subheader("No such combination exists!".format(len(name)))
        else:
            st.subheader("{} Result Found!".format(len(name)))
            df=pd.DataFrame({'Movie Name':name,'Runtime (in hrs)':time})
            st.dataframe(df,hide_index=True,use_container_width=True)


    elif user_choice=='Genre' and sub_choice=='Top Movie in Genre':
        genre_list=db.get_genre()
        genre_choice=st.selectbox("Choose the genre",genre_list)
        name,year,score,votes,gross=db.top_genre_movies(genre_choice)
        df=pd.DataFrame({'Movie Name':name,'MetaScore':score,'Year of release':year})
        df=df.sort_values(by='MetaScore',ascending=False)
        if df.shape[0]>=10:
            st.subheader("Top 10 Movies Of {} Genre".format(genre_choice))
            st.dataframe(df.head(10),hide_index=True,use_container_width=True)
        else:
            st.subheader("Top {} Movies Of {} Genre".format(df.shape[0],genre_choice))
            st.dataframe(df,hide_index=True,use_container_width=True)



elif user_choice=='Released Year':
    st.header("On basis of Year")
    year_list=db.get_year()
    year_choice=st.selectbox("Choose year",year_list)
    name,score,genre=db.movie_by_year(year_choice)
    st.subheader("{} Result Found!".format(len(name)))
    df=pd.DataFrame({'Movie Name':name,'Genre':genre,'MetaScore':score}).sort_values(by='MetaScore',ascending=False)
    st.dataframe(df,hide_index=True,use_container_width=True)



elif user_choice=='By director name':
    st.header("On basis of Director")
    subchoice=st.sidebar.selectbox("Choose option:",['Select','Top director movies'])
    dirname=db.director_name()
    if subchoice=='Select':
        dir_choice=st.selectbox('Choose director name',dirname)
        name,year,time,score=db.get_movies_by_director_name(dir_choice)
        df=pd.DataFrame({"Movie Name":name,'Released Year':year,"Runtime":time,"Score":score}).sort_values(by='Score',ascending=False)
        st.dataframe(df,hide_index=True,use_container_width=True)
    elif subchoice=='Top director movies':
        name,year,time,dirname=db.top_director_movies()
        df = pd.DataFrame({"Movie Name": name, 'Released Year': year,"Director":dirname})
        st.dataframe(df, hide_index=True, use_container_width=True)

elif user_choice=='About Project':
    st.header("Project Workflow:")
    st.write("""
1.Database Setup:
Create the necessary tables in the SQL database.
Import the movie dataset into the database.

2.Data Cleaning and Exploration:
Use pandas to clean and explore the data.
Identify any data quality issues and address them.

3.SQL Queries and Integration:
Write SQL queries to retrieve relevant data.
Integrate SQL queries with pandas for further data processing.

4.Analysis and Visualization:
Use pandas for statistical analysis.
Create interactive visualizations using Streamlit.

5.User Interface Development:
Design a Streamlit web application with an intuitive interface.
Implement dynamic elements for user interaction.

6.Testing and Refinement:
Test the application with sample queries and user scenarios.
Refine the interface and functionality based on user feedback.
    """)






#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:38:08 2020

@author: nella
"""

import streamlit as st
import pandas as pd
import random
import numpy as np
import altair as alt
import geopandas as gpd
import json
import pandas_bokeh
pandas_bokeh.output_notebook()

def main():
    
    color_list = ['SlateGray', 'LightBlue', ' Brown', 'Sienna',' LightSteelBlue', 'CadetBlue', 'Teal', 'Coral', 'LightSalmon','IndianRed']
    n = random.randint(0,len(color_list)-1)
    coloris = color_list[n]
    region = gpd.read_file('Régions_Sngal.shp')
    departement = gpd.read_file('Département_sn.shp')
    reg = region.to_crs('EPSG:4326')
    dep = departement.to_crs('EPSG:4326')
    @st.cache(allow_output_mutation=True)
    def load_data_raw():
        df = pd.read_excel('coord_region.xlsx')
        return df
    
    def altair_chart(df, vertical_axis, coloris, titre):
        hist = alt.Chart(df).mark_bar(size=25).encode(x = alt.X('Region', sort = '-y'), y = vertical_axis, color = alt.value(coloris)).properties(
            width = alt.Step(50), height = 400, title = titre ).interactive()
        st.altair_chart(hist, use_container_width=True)
        return
            
    def checkbox_filtering(df, vertical_axis, choice_order):
        size = df.shape[0]
        choice = st.slider(f'Choose a number', min_value = 1, max_value = size , value = 3)
        class_data = data.sort_values(by = vertical_axis, ascending = choice_order)
        class_data = class_data.loc[0:choice-1,:]
        return class_data
    
    def base_map(reg, dep, coloris):
       first=reg.plot_bokeh(figsize=(1000,800), color='LightBlue', show_figure=False, legend="Senegal Regions", show_colorbar=False)
       second=dep.plot_bokeh(figure=first, legend="Senegal Dep", color='CadetBlue', show_figure=False, hovertool_string="""<h1>@NAME_1</h1>""")
       return second
    
    def layer_map(df_gpd, background, vertical_axis, coloris):
        marker = ["circle", "square", "triangle",  "circle_cross", "square_cross"]
        n = random.randint(0,len(marker)-1)
        mark = marker[n]
        final_map=df_gpd.plot_bokeh(figure=background, color=coloris, legend=vertical_axis, size=vertical_axis, hovertool_string=f"""<h3>Value: @{vertical_axis}</h3>""",marker=mark)
        st.bokeh_chart(final_map)
        return 

    def Homepage():
        
        st.image('data:image/jpeg;base64,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',
                 use_column_width=True)
        st.markdown("> A Dashboard for Covid in Senegal")
        st.write('This Dashbord was produced by Geomatica. Check the menu on the left side to display data')
        st.write('The expertise developed by Géomatica Services covers several types of needs, in particular: Design, Deployment and Administration of GIS / IDG Infrastructures')
        st.write('Expertise in the production, analysis and enhancement of spatial data: collection, BD management, DBMS, cartography, Webmapping, datvisualization')
        st.write('Management of geomatics projects and development of observation, analysis and monitoring systems for territories')
        st.write('environments (Web development, online mapping, programming')
        return 
    
    def display_raw (df):
        #Displaying Dataframe
        st.subheader('Senegal Covid Data')
        if st.checkbox('Raw Data'):
            st.dataframe(df.astype('object'))
        return 
        
    def graph_visualisation(df, coloris):
        #Displaying population distribution
        to_display = ['Population','Confirmed','Recovered', 'Dead', 'Ill', 'Summary']
        st.subheader('Data Distribution Graph')
        feature = st.selectbox("What would you like to display?", to_display )
        if feature == to_display[0]:
            st.subheader('Population Distribution Graph')
            titre = 'Number of inhabitants per Region'
            altair_chart(df, feature, coloris, titre)        
            #Choose to display n highest populated Region
            if st.checkbox('Display n highest populated Region'):
               choice_order = False
               filtered_data = checkbox_filtering(df, feature, choice_order)
               altair_chart(filtered_data, feature, coloris, titre)
        elif feature == to_display[1]:
            st.subheader('Confirmed Cases Distribution Graph')
            titre = 'Number of confirmed cses per Region'
            altair_chart(df, feature, coloris, titre)        
            #Choose to display n highest populated Region
            if st.checkbox('Display n highest infected Region'):
               choice_order = False
               filtered_data = checkbox_filtering(df, feature, choice_order)
               altair_chart(filtered_data, feature, coloris, titre)
        elif feature == to_display[2]:
            st.subheader('Recovered Distribution Graph')
            titre = 'Number of recovered cases per Region'
            altair_chart(df, feature, coloris, titre)        
            #Choose to display n highest populated Region
            if st.checkbox('Display n Region with high recovering rate'):
               choice_order = False
               filtered_data = checkbox_filtering(df, feature, choice_order)
               altair_chart(filtered_data, feature, coloris, titre)
        elif feature == to_display[3]:
            st.subheader('Death Distribution Graph')
            titre = 'Number of death cases per Region'
            altair_chart(df, feature, coloris, titre)        
            #Choose to display n highest populated Region
            if st.checkbox('Display n Region with high death rate'):
               choice_order = False
               filtered_data = checkbox_filtering(df, feature, choice_order)
               altair_chart(filtered_data ,feature, coloris, titre) 
        elif feature == to_display[4]:
            st.subheader('Ill Distribution Graph')
            titre = 'Number of ill cases per Region'
            altair_chart(df, feature, coloris, titre)        
            #Choose to display n highest populated Region
            if st.checkbox('Display n Region with high illness rate'):
               choice_order = False
               filtered_data = checkbox_filtering(df, feature, choice_order)
               altair_chart(filtered_data ,feature, coloris, titre) 
        else:
            st.subheader('Data Summary Graph')
            df_sum = df.drop(columns=['Longitude','Latitude'])
            df_sum['Population'] =  df_sum['Population'] // 10000
            df_sum = pd.melt(df_sum, id_vars="Region", var_name="Classe", value_name=" Total Population")
            alt.Chart(df_sum).mark_bar().encode(
            x='Region',
            y='Total Population',
            color ='Classe')
        return
   
    def map_visualisation(df_gpd, coloris):
 	
        #Displaying population distribution
        to_display = ['Population','Confirmed','Recovered', 'Dead', 'Ill']
        st.subheader('Data Geographical Map')
        background = base_map(reg,dep,coloris)
        feature = st.selectbox("What would you like to display?", to_display )
        if feature == to_display[0]:
            st.subheader('Population Map')
            final_map = df_gpd.plot_bokeh(figure=background, color='darkred', legend=feature, size=20, hovertool_string=f"""<h3>Population: @{feature}</h3>""",marker='circle')
            st.bokeh_chart(final_map)
        elif feature == to_display[1]:
            st.subheader('Confirmed Cases Map')
            final_map = df_gpd.plot_bokeh(figure=background, color='Indianred', legend=feature, size=25, hovertool_string=f"""<h3>Population: @{feature}</h3>""",marker='triangle')
            st.bokeh_chart(final_map)
        elif feature == to_display[2]:
            st.subheader('Recovered Map')
            final_map = df_gpd.plot_bokeh(figure=background, color='Crimson', legend=feature, size=15, hovertool_string=f"""<h3>Population: @{feature}</h3>""",marker='circle')
            st.bokeh_chart(final_map)
        elif feature == to_display[3]:
            st.subheader('Dead Map')
            final_map = df_gpd.plot_bokeh(figure=background, color='Crimson', legend=feature, size=10, hovertool_string=f"""<h3>Population: @{feature}</h3>""",marker='triangle')
            st.bokeh_chart(final_map)
        elif feature == to_display[4]:
            st.subheader('Ill Map')
            final_map = df_gpd.plot_bokeh(figure=background, color='Maroon', legend=feature, size=15, hovertool_string=f"""<h3>Population: @{feature}</h3>""",marker='circle')
            st.bokeh_chart(final_map)
        else:
            st.bokeh_chart(background)
        return
    
    
    st.sidebar.image('https://www.geomatica-services.com/wp-content/uploads/2019/08/IMG_7964.jpg',
                     use_column_width=True)
    st.sidebar.title('Welcome to Geomatica')
    for i in range(3):
        st.sidebar.title(' ')
    st.sidebar.title("Menu")
    app_mode = st.sidebar.selectbox("Please select a page", ["Homepage",
                                                             "Data Exploration",
                                                             "Data Distribution",
                                                             "Map Visualization",])
    data = load_data_raw()

    if app_mode == 'Homepage':
        Homepage()
    elif app_mode == "Data Exploration":
        display_raw(load_data_raw().astype('str'))
    elif app_mode == "Data Distribution":
        data_dist = load_data_raw()
        graph_visualisation(data, coloris)
    elif app_mode == "Map Visualization":
        data_gpd = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.Longitude, data.Latitude))
        data_gpd.crs = 'EPSG:4326'
        map_visualisation(data_gpd, coloris)

    return
    	
    
if __name__ == "__main__":
    main()

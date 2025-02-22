import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px

import json  

API_URL = "http://localhost:8000/req/"  

st.title(" Dive into the Story of the Unsinkable Ship 🚢")


query=st.text_input("Asq Question related to Titanic Ship ")


def show_response(api_url,query):
    while(query):
        response = requests.get(API_URL+query)
        
        if response.status_code == 200:
            data = response.json()  
            st.write(f"### {query}:")
            st.write(data)
            break
            #st.json(data)  # Display JSON response
        else:
            st.error(f"Failed to fetch data. Status Code: {response.status_code}")
            break
# show_response(API_URL,query)

def detect_chart_type(query: str):
    query = query.lower()
    chart_keywords = {
        "histogram": ["histogram", "histogram age distribution","histogram show "],
        "bar_chart": ["bar chart", "bar chart passengers by port distribution Show"],
        "scatter_plot": ["scatter plot", "scatter plot age vs fare"," scatter plot man vs woman"],
        "box_plot": ["box plot", "fare distribution"],
        "pie_chart": ["pie chart", "pie chart  distribution","pie chart peoples of titanic"],
    }

    for chart_type, keywords in chart_keywords.items():
        if any(keyword in query for keyword in keywords):
            return chart_type

    return None  # No chart detected


# show_response(API_URL,query)






def draw_graphs(api_url, query):
    response = requests.get(api_url + query)
    context = detect_chart_type(query)
    print(context)

    if response.status_code == 200:
        data = response.json() if isinstance(response.json(), dict) else json.loads(response.json())
        st.write("Raw API Response:", data)  # Debugging: Show raw data
        st.write(response.headers.get("Content-Type",""))
        try:
           
            if context=="histogram":
                # Extract values correctly
                age_bins = data.get("x_axis", [])  # X-axis values
                frequencies = data.get("y_axis", [])  # Y-axis values
                # Create the histogram
                fig, ax = plt.subplots()
                st.write(f"Explanation: {data.get('explanation' )}")
                ax.bar(age_bins, frequencies, width=1.0, edgecolor='blue')
                ax.set_xlabel("X-axis (Bins)")
                ax.set_ylabel("Y-axis (Frequency)")
                ax.set_title(f"{context}")

                # Display the plot in Streamlit
                st.pyplot(fig)
                st.write(data["mean"])
            elif context=="scatter_plot":
                x_values = data.get("x_axis", [])  
                y_values = data.get("y_axis", [])  

                # Create Scatter Plot
                fig, ax = plt.subplots()
                ax.scatter(x_values, y_values, color='blue', edgecolor='black')
                st.write(f"Eplanation: {data.get('explanation' )}")

                ax.set_xlabel("X-axis (Bins)")
                ax.set_ylabel("Y-axis (Frequency)")
                ax.set_title(f" {context}")
                ax.grid(True)

                # Display the plot in Streamlit
                st.pyplot(fig)

                # Show additional statistical data
                st.write(f"Mean: {data.get('mean', 'N/A')}")
                st.write(f"Median: {data.get('median', 'N/A')}")
                st.write(f"Mode: {data.get('mode', 'N/A')}")
            elif context=="bar_chart":
                    x_values = data.get("x_axis", [])
                    y_values = data.get("y_axis", [])
                    # Create a Matplotlib figure with two subplots (Scatter Plot + Bar Chart)
                    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

                    st.write(f"Explanation: {data.get('explanation', 'No explanation available')}")
                    # Scatter Plot
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.bar(x_values, y_values, color='green', edgecolor='black')
                    ax.set_xlabel("X-axis (Categories)")
                    ax.set_ylabel("Y-axis (Values)")
                    ax.set_title(f" {context}")
                    ax.grid(axis="y")

                    # Display the plots in Streamlit
                    st.pyplot(fig)
            elif context=="pie_chart":
                x_values = data.get("x_axis", [])
                y_values = data.get("y_axis", [])

                # Create a Matplotlib figure for Bar Chart
                
                # Display Bar Chart in Streamlit
                

                # Create a Pie Chart
                fig_pie, ax_pie = plt.subplots()
                ax_pie.pie(y_values, labels=x_values, autopct="%1.1f%%", colors=plt.cm.Paired.colors, startangle=90)
                ax_pie.set_title(f"{query}")

                # Display Pie Chart in Streamlit
                st.pyplot(fig_pie)


        
        except Exception as e:
            st.write(e)

    



    
    

if query:
    if detect_chart_type(query)!=None:
        draw_graphs(API_URL,query)
    else:
        show_response(API_URL,query)
            
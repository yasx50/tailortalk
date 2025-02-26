import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.express as px
import difflib
import json
import re

# Set page configuration for better layout
st.set_page_config(layout="centered", page_title="Titanic Story Explorer")

API_URL = "https://tailortalk-1gne.onrender.com/req/"  
# API_URL = "http://127.0.0.1:8000/req/"  

st.title("Dive into the Story of the Unsinkable Ship 🛳️")

# Create a container for the input section
input_container = st.container()

with input_container:
    query = st.text_input("Ask Question related to Titanic Ship", key="query")

def detect_chart_type(query: str):
    if not query:
        return None
        
    query = query.lower().strip()  # Convert input to lowercase and remove extra spaces

    # Dictionary mapping chart types to keywords
    chart_keywords = {
        "histogram": ["histogram", "age distribution", "passenger ages"],
        "bar_chart": ["bar chart", "passengers by port", "port distribution"],
        "scatter_plot": ["scatter plot", "age vs fare", "man vs woman"],
        "box_plot": ["box plot", "fare distribution"],
        "pie_chart": ["pie chart", "class distribution", "passenger class"]
    }

    # Check if the query contains any exact match for a chart type
    for chart_type, keywords in chart_keywords.items():
        for keyword in keywords:
            # Use regex to match whole words only, avoiding partial matches
            if re.search(rf"\b{re.escape(keyword)}\b", query):
                return chart_type

    return None  # Return None if no chart type is detected

# Create a container for the response section
response_container = st.container()

def show_response(api_url, query):
    if not query:
        return
        
    response = requests.get(api_url + query)
    
    with response_container:
        if response.status_code == 200:
            data = response.json()  
            st.write_h( query)
            st.write(data)
        else:
            st.error(f"Failed to fetch data. Status Code: {response.status_code}")

def draw_graphs(api_url, query):
    if not query:
        return
        
    response = requests.get(api_url + query)
    context = detect_chart_type(query)
    
    print(context)
    print("Raw API Response:", repr(response.text))

    with response_container:
        if response.status_code == 200:
            try:
                data = response.json() if isinstance(response.json(), dict) else json.loads(response.json())
                
                # Use expander for raw data to keep UI clean
                with st.expander("View Raw API Response"):
                    st.write(data)
                    st.write(response.headers.get("Content-Type", ""))
                
                st.subheader(f"Visualization: {context.replace('_', ' ').title()}")
                
                if context == "histogram":
                    # Extract values correctly
                    age_bins = data.get("x_axis", [])  # X-axis values
                    frequencies = data.get("y_axis", [])  # Y-axis values
                    # Create the histogram
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.bar(age_bins, frequencies, width=1.0, edgecolor='black')
                    ax.set_xlabel("X-axis (Bins)")
                    ax.set_ylabel("Y-axis (Frequency)")
                    ax.set_title(f"{context.replace('_', ' ').title()}")

                    # Display the plot in Streamlit
                    st.pyplot(fig)
                    
                    # Display explanation in an info box
                    st.info(f"Explanation: {data.get('explanation', [])}")
                    st.write(f"Mean: {data.get('mean', 'N/A')}")
                    
                elif context == "scatter_plot":
                    x_values = data.get("x_axis", [])  
                    y_values = data.get("y_axis", [])  

                    # Create Scatter Plot
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.scatter(x_values, y_values, color='blue', edgecolor='black')
                    ax.set_xlabel("X-axis (Bins)")
                    ax.set_ylabel("Y-axis (Frequency)")
                    ax.set_title(f"{context.replace('_', ' ').title()}")
                    ax.grid(True)

                    # Display the plot in Streamlit
                    st.pyplot(fig)

                    # Show additional statistical data in a nice format
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Mean", data.get('mean', 'N/A'))
                    with col2:
                        st.metric("Median", data.get('median', 'N/A'))
                    with col3:
                        st.metric("Mode", data.get('mode', 'N/A'))
                    
                    # Display explanation in an info box
                    st.info(f"Explanation: {data.get('explanation', [])}")
                    
                elif context == "bar_chart":
                    x_values = data.get("x_axis", [])
                    y_values = data.get("y_axis", [])
                    
                    # Create a Matplotlib figure for Bar Chart
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.bar(x_values, y_values, color='green', edgecolor='black')
                    ax.set_xlabel("X-axis (Categories)")
                    ax.set_ylabel("Y-axis (Values)")
                    ax.set_title(f"{context.replace('_', ' ').title()}")
                    ax.grid(axis="y")

                    # Display the plots in Streamlit
                    st.pyplot(fig)
                    
                    # Display explanation in an info box
                    st.info(f"Explanation: {data.get('explanation', [])}")
                    
                elif context == "pie_chart":
                    x_values = data.get("x_axis", [])
                    y_values = data.get("y_axis", [])

                    # Create a Pie Chart
                    fig_pie, ax_pie = plt.subplots(figsize=(10, 6))
                    ax_pie.pie(y_values, labels=x_values, autopct="%1.1f%%", colors=plt.cm.Paired.colors, startangle=90)
                    ax_pie.set_title(f"{context.replace('_', ' ').title()}")

                    # Display Pie Chart in Streamlit
                    st.pyplot(fig_pie)
                    
                    # Display explanation in an info box
                    st.info(f"Explanation: {data.get('explanation', [])}")
                    
                elif context == "box_plot":
                    values = data.get("y_axis", [])
                    x_labels = data.get("x_axis", [])

                    if not values or not x_labels:
                        st.error("No data available for the box plot.")
                        return

                    # Convert single values into multiple sample points for each class
                    values = [
                        [v + i * 2 for i in range(10)] for v in values
                    ]  # Simulating 10 sample points per class

                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.boxplot(values, vert=True, patch_artist=True)
                    ax.set_xticks(range(1, len(x_labels) + 1))  # Box plot positions start from 1
                    ax.set_xticklabels(x_labels)
                    ax.set_title(f"{context.replace('_', ' ').title()}")
                    ax.set_ylabel("Fare Distribution")
                    
                    # Display the plot
                    st.pyplot(fig)
                    
                    # Display explanation in an info box
                    st.info(f"Explanation: {data.get('explanation', [])}")
            
            except Exception as e:
                st.error(f"Error processing data: {e}")

def choose():
    if not query:
        with response_container:
            st.warning("Please enter a question about the Titanic.")
        return
        
    # Clear previous results when submitting a new query
    if 'previous_response' in st.session_state:
        response_container.empty()
    
    chart_type = detect_chart_type(query)
    
    if chart_type:
        draw_graphs(API_URL, query)
    else:
        show_response(API_URL, query)
    
    # Mark that we've shown a response
    st.session_state.previous_response = True

# Create the button within the input container to ensure correct order
with input_container:
    st.button("Submit Question", on_click=choose, type="primary")

# Add a separator for visual clarity
st.markdown("---")
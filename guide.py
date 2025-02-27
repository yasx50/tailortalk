import streamlit as st

# Set page config
st.set_page_config(page_title="Titanic AI Guide", page_icon="🚢", layout="wide")

# Title & Description
st.title("🛳️ Titanic AI Agent - How to Use")
st.markdown("""
Welcome to the **Titanic AI Agent!** This guide will help you understand how to interact with the AI effectively. 

Use **clear and structured prompts** to get the best responses.
""")

# Sidebar for quick navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Jump to:", ["Getting Started", "Best Practices", "Example Prompts", "Visualizations Guide"])

# Section 1: Getting Started
if page == "Getting Started":
    st.header("🚀 Getting Started")
    st.write("""
    The Titanic AI Agent can analyze Titanic dataset trends, answer questions, and generate visuals.
    
    **Steps to use:**
    1. Type your question in the input box.
    2. Be specific with what you need (e.g., summary stats, graphs).
    3. If requesting a visualization, mention the type (e.g., histogram, bar chart, box plot).
    """)

# Section 2: Best Practices
elif page == "Best Practices":
    st.header("✅ Best Practices for Better Results")
    st.write("""
    To get the most accurate and useful responses, follow these best practices:
    
    🔹 **Be Specific** → Instead of "Show Titanic stats", ask "Show survival rate by class." \n
    🔹 **Request Visuals Correctly** → Specify the type (histogram, bar chart, etc.). \n
    🔹 **Use Filters** → Example: "Show survival rate for passengers under 18." \n
    🔹 **Ask for Comparisons** → Example: "Compare survival rates of male and female passengers." \n
    🔹 **Explore Trends** → Example: "How does fare affect survival chances?"
    """)

# Section 3: Example Prompts
elif page == "Example Prompts":
    st.header("💡 Example Prompts")
    st.write("Use these prompts to interact effectively with the Titanic AI Agent:")

    st.code('''How many passengers were in each class?''')
    st.code('''Show the age distribution of Titanic passengers with a histogram.''')
    st.code('''How do ticket prices differ between survivors and non-survivors?.''')
    st.code(''' relationship between age and fare with a scatter plot.''')
    st.code('''How many survivors were there in each class?''')
    st.code('''Display a pie chart of survival percentages.''')


# Section 4: Visualizations Guide
elif page == "Visualizations Guide":
    st.header("📊 Visualizations Guide")
    st.write("To request a visualization, specify the type in your prompt:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Histogram")
        st.write("Use when analyzing distributions (e.g., age).")
        st.code('''Analyze the age distribution of Titanic passengers with a histogram visualization.''')
        
        st.subheader("Bar Chart")
        st.write("Use for categorical comparisons (e.g., survival rate by class).")
        st.code('''Show survival rates by passenger class in a bar chart.''')
        
        st.subheader("Box Plot")
        st.write("Use for showing distribution and outliers (e.g., fare distribution).")
        st.code('''Conduct a statistical analysis of fare distribution by passenger class using a box plot visualization.''')
    
    with col2:
        st.subheader("Scatter Plot")
        st.write("Use for relationships between two variables (e.g., fare vs. age).")
        st.code(''' - Display a scatter plot comparing male and female passengers based on age and fare.
''')
        
        st.subheader("Pie Chart")
        st.write("Use for proportions (e.g., percentage of passengers who survived).")
        st.code('''Perform a comprehensive breakdown of passenger survival rates using a pie chart visualization.''')

st.sidebar.info("💡 Tip: The more detailed your prompt, the better the response!")
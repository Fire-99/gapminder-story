# CHECKPOINT 1: hello, Streamlit run: streamlit run 01_hello.py
import streamlit as st
import plotly.express as px

st.title("Global Development Explorer")
st.write("Life expectancy and income for 142 countries, 1952–2007.")

df = px.data.gapminder()
st.dataframe(df)


########################################################################## CHECKPOINT 2: Plotly Chart in Streamlit

import streamlit as st
import plotly.express as px

st.title("Global Development Explorer")
st.write("Life expectancy and income for 142 countries, 1952-2007.")

# Load dataset
df = px.data.gapminder()

# Filter data for 2007
df_2007 = df[df["year"] == 2007]

# Create scatter plot
fig = px.scatter(
    df_2007,
    x="gdpPercap",
    y="lifeExp",
    hover_name="country",
    color="continent",
    size="pop",
    log_x=True
)

# Display chart
st.plotly_chart(fig, use_container_width=True)



################################################################### CHECKPOINT 3: Streamlit Widgets

import streamlit as st
import plotly.express as px

# App title
st.title("Global Development Explorer")

# Load Gapminder dataset
df = px.data.gapminder()

# Continent dropdown
continent = st.selectbox(
    "Continent",
    ["All"] + sorted(df["continent"].unique())
)

# Year slider
years = sorted(df["year"].unique())

year = st.select_slider(
    "Year",
    options=years,
    value=2007
)

# Filter dataset by year
filtered = df[df["year"] == year]

# Filter dataset by continent
if continent != "All":
    filtered = filtered[filtered["continent"] == continent]

# Create interactive scatter plot
fig = px.scatter(
    filtered,
    x="gdpPercap",
    y="lifeExp",
    hover_name="country",
    color="continent",
    size="pop",
    log_x=True,
    size_max=50,
    range_y=[25, 90]
)

# Display Plotly chart
st.plotly_chart(fig, use_container_width=True)



##################################################################### CHECKPOINT 4: Sidebar + KPI Metrics in Columns

import streamlit as st
import plotly.express as px

# Step 1: Application title
st.title("Global Development Explorer")

# Step 2: Load Gapminder dataset
df = px.data.gapminder()

# Step 3: Sidebar widgets
continent = st.sidebar.selectbox(
    "Continent",
    ["All"] + sorted(df["continent"].unique())
)

year = st.sidebar.select_slider(
    "Year",
    options=sorted(df["year"].unique()),
    value=2007
)

# Step 4: Filter data by year
filtered = df[df["year"] == year]

# Step 5: Filter data by continent
if continent != "All":
    filtered = filtered[filtered["continent"] == continent]

# Step 6: Create three KPI columns
col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries",
    len(filtered)
)

col2.metric(
    "Avg life expectancy",
    f"{filtered['lifeExp'].mean():.1f} yrs"
)

col3.metric(
    "Median GDP per capita",
    f"${filtered['gdpPercap'].median():,.0f}"
)

# Step 7: Create interactive scatter plot
fig = px.scatter(
    filtered,
    x="gdpPercap",
    y="lifeExp",
    hover_name="country",
    color="continent",
    size="pop",
    log_x=True,
    size_max=50,
    range_y=[25, 90],
    title=f"GDP per Capita vs Life Expectancy ({year})",
    labels={
        "gdpPercap": "GDP per Capita (USD)",
        "lifeExp": "Life Expectancy (Years)",
        "pop": "Population"
    }
)

# Step 8: Display chart
st.plotly_chart(fig, use_container_width=True)

############################################## DEMO: caching. Move the slider with and without @st.cache_data
import time
import streamlit as st
import plotly.express as px

@st.cache_data # try commenting this line out
def load_data():
    time.sleep(3) # pretend this is a slow database
    return px.data.gapminder()

df = load_data()
year = st.slider("Year", 1952, 2007, 2007, step=5)
st.write(f"{len(df[df['year'] == year])} countries in {year}")

########################################### CHECKPOINT 5: a Story tab (author-driven) + an Explore tab (reader-driven)

# CHECKPOINT 5: Story Tab + Explore Tab

import streamlit as st
import plotly.express as px

# Step 1: Configure the Streamlit page
st.set_page_config(
    page_title="Global Development Explorer",
    layout="wide"
)

# Step 2: Load the Gapminder dataset
@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

# Step 3: Application title
st.title("Global Development Explorer")

# Step 4: Create two tabs
story, explore = st.tabs(["The story", "Explore it yourself"])

# ------------------------------
# TAB 1: THE STORY
# ------------------------------

with story:

    st.header("Asia gained 24 years of life expectancy since 1952")

    # Calculate average life expectancy by continent and year
    by_continent = df.groupby(
        ["continent", "year"],
        as_index=False
    )["lifeExp"].mean()

    # Create line chart
    fig = px.line(
        by_continent,
        x="year",
        y="lifeExp",
        color="continent",
        labels={
            "lifeExp": "Average life expectancy (years)",
            "year": "Year"
        },
        title="Life Expectancy Trends by Continent (1952-2007)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        "Every continent improved, but **Asia** experienced "
        "a substantial increase in average life expectancy "
        "between 1952 and 2007."
    )

    st.caption(
        "Source: Gapminder, via plotly.express. "
        "Unweighted country averages."
    )

# ------------------------------
# TAB 2: EXPLORE IT YOURSELF
# ------------------------------

with explore:

    st.header("Explore Global Development")

    # Continent dropdown
    continent = st.selectbox(
        "Select Continent",
        ["All"] + sorted(df["continent"].unique())
    )

    # Year slider
    year = st.select_slider(
        "Select Year",
        options=sorted(df["year"].unique()),
        value=2007
    )

    # Filter dataset
    filtered = df[df["year"] == year]

    if continent != "All":
        filtered = filtered[
            filtered["continent"] == continent
        ]

    # Display KPI metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Countries",
        len(filtered)
    )

    col2.metric(
        "Average Life Expectancy",
        f"{filtered['lifeExp'].mean():.1f} years"
    )

    col3.metric(
        "Median GDP per Capita",
        f"${filtered['gdpPercap'].median():,.0f}"
    )

    # Interactive scatter plot
    fig2 = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True,
        size_max=50,
        range_y=[25, 90],
        title=f"GDP vs Life Expectancy ({year})",
        labels={
            "gdpPercap": "GDP per Capita (USD)",
            "lifeExp": "Life Expectancy (Years)",
            "pop": "Population"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)

##############################################################################

# CHECKPOINT 5: Explore Tab

with explore:

    left, right = st.columns([1, 3])

    # Continent dropdown with unique key
    continent = left.selectbox(
        "Continent",
        ["All"] + sorted(df["continent"].unique()),
        key="checkpoint5_continent"
    )

    # Year slider with unique key
    year = left.select_slider(
        "Year",
        options=sorted(df["year"].unique()),
        value=2007,
        key="checkpoint5_year"
    )

    # Filter data by selected year
    filtered = df[df["year"] == year]

    # Filter data by selected continent
    if continent != "All":
        filtered = filtered[
            filtered["continent"] == continent
        ]

    # Create location description
    place = "the world" if continent == "All" else continent

    # Display KPI metric
    left.metric(
        "Avg life expectancy",
        f"{filtered['lifeExp'].mean():.1f} yrs"
    )

    # Display dynamic narrative
    right.markdown(
        f"In **{year}**, the **{len(filtered)}** countries "
        f"in **{place}** had an average life expectancy "
        f"of **{filtered['lifeExp'].mean():.1f} years**."
    )

    # Create interactive scatter plot
    fig = px.scatter(
        filtered,
        x="gdpPercap",
        y="lifeExp",
        hover_name="country",
        color="continent",
        size="pop",
        log_x=True,
        size_max=50,
        range_y=[25, 90],
        title=f"GDP vs Life Expectancy ({year})"
    )

    # Display chart
    right.plotly_chart(
        fig,
        use_container_width=True
    )

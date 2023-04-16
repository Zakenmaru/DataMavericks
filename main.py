import pandas as pd
import streamlit as st
from PIL import Image


# Define function for the first tab
def Lineups():
    st.header("Lineups")

    teams = ["Dallas Mavericks", "Los Angeles Lakers", "Golden State Warriors", "Brooklyn Nets"]
    selected_team = st.selectbox("Select a team", teams, index=0)

    if selected_team == "Dallas Mavericks":
        st.markdown("Current Team: **Dallas Mavericks** (click to change)")
    elif selected_team == "Los Angeles Lakers":
        st.markdown("Current Team: **Los Angeles Lakers** (click to change)")
    elif selected_team == "Golden State Warriors":
        st.markdown("Current Team: **Golden State Warriors** (click to change)")
    else:
        st.markdown("Current Team: **Brooklyn Nets** (click to change)")

    # Define the table headers
    headers = ["Player Name", "Position", "Height(ft\"in)", "Weight(lbs)", "Info"]

    # TEAM TABLE - Dallas Mavericks
    if selected_team == "Dallas Mavericks":
        # Define the data for the first row
        data = {
            "Player Name": "Luka Doncic",
            "Position": "PG",
            "Height(ft\"in)": "6'7\"",
            "Weight(lbs)": 230,
            "Info": "Lorem ipsum dolor sit amet"
        }
    # TODO - Fill in more possible teams and their players
    else:
        data = {
            "Player Name": "Check Back Later!",
            "Position": "Nonexistent",
            "Height(ft\"in)": "5'12\"",
            "Weight(lbs)": 100,
            "Info": "Under Construction"
        }
    # Create a list of data that contains the first row and the remaining rows with ellipses
    data_list = [data] + [{"...": "..." for _ in range(len(headers))} for _ in range(9)]

    # Create a Pandas DataFrame object from the list of data and the headers
    df = pd.DataFrame(data_list, columns=headers)

    # Display the table in Streamlit
    st.table(df)



# Define function for the second tab
def Matchups():
    st.header("Matchups")
    Players_1 = ["Luka Doncic", "Kyrie Irving", "Justin Holiday", "Theo Pinson", "Jaden Hardy", "Dwight Powell",
                 "Josh Green", "Tim Hardaway Jr.", "Markieff Morris", "Frank Ntilikina", "Reggie Bullock",
                 "Christian Wood", "Maxi Kleber", "Davis Bertans", "Javale McGee"]
    Players_2 = ["Bryant Test", "Papa's pizzeria", "Gray Domino", "Black Velvet", "Chcolate Coating"]
    st.write(f"<span style='color: blue'><b>Select Player 1</b></span>", unsafe_allow_html=True)
    selected_player_1 = st.selectbox(" ",Players_1, index=0)
    st.write(f"<span style='color: red'><b>Select Player 2</b></span>", unsafe_allow_html=True)
    selected_player_2 = st.selectbox(" ", Players_2, index=0)
    # TODO - Pull up selected_player_1's stats and selected_player_2's stats and run algorithmic magic on them woo
    # pit players against each other and run probability of p1 beating p2
    estimated_chance = 99.875

    # after doing that, put them next to each other using an automatically pulled image
    # TODO - make getting the image automatic, either by mapping or something else
    fighter1_image = Image.open("images/luka.png")
    fighter2_image = Image.open("images/testbryant.png")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.image(fighter1_image)

    with col2:
        st.markdown(
            "<div style='text-align:center'><span style='color:blue; font-size: 72px;'>V.</span><span style='color:red; font-size: 72px;'>S.</span></div>", unsafe_allow_html=True)

    with col3:
        st.image(fighter2_image)

    st.subheader("Prediction")
    st.write(f"<span style='color: blue'>{selected_player_1}</span> has a <b>{str(estimated_chance)}%</b> chance of beating <span style='color: red'>{selected_player_2}</span>", unsafe_allow_html=True)




# Define function for the third tab
def Shooting_Calculator():
    st.header("Shooting Calculator")
    st.write("This is the content for Shooting Calculator.")
    # Add more code here for custom functionality


def Log_Off():
    st.header("Log Off")


# Define the Streamlit app layout
st.set_page_config(page_title="Data Mavericks", layout="wide")
st.sidebar.image("images/mavs.png", width=200) # Add an image to the sidebar
st.sidebar.title("DataMavericks")
tabs = ["Lineups", "Matchups", "Shooting Calculator"]
selected_tab = st.sidebar.radio("Navigation", tabs, index=0)

# Run the appropriate function based on the selected tab
if selected_tab == "Lineups":
    Lineups()
elif selected_tab == "Matchups":
    Matchups()
elif selected_tab == "Shooting Calculator":
    Shooting_Calculator()
else:
    Log_Off()
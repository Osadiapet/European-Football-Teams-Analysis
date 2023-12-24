import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import plotly.express as px
import os


matplotlib.use('Agg')  # Use the 'Agg' backend for saving figures
import warnings
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)


# Configure Streamlit
st.set_page_config(page_title="European Football Analysis", page_icon="⚽")

#layout="wide"
# Load the data
# Get the current directory path
current_dir = os.getcwd()

# Creating a list containing all dataset names
list_of_names = ['Country', 'League', 'Player', 'Team', 'Team_Attributes', 'Player_Attributes', 'Match']

# Create an empty list for datasets
dataframe_list = []
# Appending datasets into the list
for name in list_of_names:
    file_path = os.path.join(current_dir, name + '.csv')
    df = pd.read_csv(file_path)
    dataframe_list.append(df)

#calling each of the datasets 
countries=dataframe_list[0]
league=dataframe_list[1]
players=dataframe_list[2]
teams=dataframe_list[3]
team_attributes=dataframe_list[4]
player_attributes=dataframe_list[5]
matches=dataframe_list[6]

# Main page title and description
st.title("Football Analytics Explorer - European Football Analysis (2008-2016)")
st.write(
    "Welcome to the European Football Data Analysis app. The world of football is not just about goals and cheers; it's a realm where data and insights can elevate the game. \
    Our project takes you on a journey through a treasure trove of football data, encompassing more than 25,000 matches, 10,000 players, and 11 European countries' \
        top championships, spanning from the 2008/2009 season to 2015/2016. Sourced from EA Sports' FIFA video game series. Explore the intricate relationship between team playing attributes \
              and match outcomes with Football Analytics Explorer."
)

# Data Wrangling section
st.header("Teams Analysis")
st.write("Let's start by exploring the teams.")

teams_data = pd.merge(team_attributes, teams, on='team_api_id', how='inner')

#lets convert the date columnd to the correct data type 
teams_data['date'] = pd.to_datetime(teams_data['date'])

# Show first rows of the data
if st.checkbox("Show Teams Data"):
    # Join team_attributes with teams on team_api_id
    st.dataframe(teams_data.head())

# Number of players in the dataset
if st.checkbox('Show Number of Teams'):
    num_teams = teams_data['team_api_id'].nunique()
    st.write(f"Number of teams in the dataset: {num_teams}")


# Descriptive statistics
st.write("Descriptive Statistics of Teams Attributes.")
if st.checkbox("Show Descriptive Statistics"):
    st.write(teams_data[['defenceAggression', 'defenceTeamWidth', 'defencePressure',  'buildUpPlayPassing','chanceCreationCrossing',
                        'chanceCreationShooting',  'chanceCreationPassing', 'buildUpPlaySpeed']].describe())


# Select the variables we want to plot
variables_to_plot = ['defenceAggression', 'defenceTeamWidth', 'defencePressure',
                     'buildUpPlayPassing', 'chanceCreationCrossing',
                     'chanceCreationShooting', 'chanceCreationPassing', 'buildUpPlaySpeed']

# Create a Streamlit app
st.write("Histogram of Team Attribute")

# Select a variable to plot
selected_variable = st.selectbox("Select a team numerical attribute to show distribution", variables_to_plot)

# Check if any variable has been selected
if selected_variable:
    # Display histogram
    st.subheader(f"Histogram of {selected_variable}")
    plt.figure(figsize=(10, 6))
    plt.hist(teams_data[selected_variable], bins=20, alpha=0.7, edgecolor='black', color='dodgerblue')
    plt.xlabel("Values")
    plt.ylabel("Frequency")
    plt.title(f"Histogram of {selected_variable}")
    st.pyplot()


# List of categorical variables
categorical_variables = [
    'buildUpPlaySpeedClass', 'buildUpPlayDribblingClass', 'buildUpPlayPassingClass',
    'buildUpPlayPositioningClass', 'chanceCreationPassingClass', 'chanceCreationCrossingClass',
    'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressureClass',
    'defenceAggressionClass', 'defenceTeamWidthClass', 'defenceDefenderLineClass',
]

# Create a Streamlit app
st.write("Select a team categorical attribute to Show Distribution")

# Select a categorical variable to plot
selected_variable = st.selectbox("Select a variable to plot", categorical_variables)

# Check if any variable has been selected
if selected_variable:
    # Create a bar chart
    st.subheader(f"Bar Chart for {selected_variable}")
    variable_counts = teams_data[selected_variable].value_counts(normalize = True)*100
    plt.figure(figsize=(10, 6))
    plt.bar(variable_counts.index, variable_counts.values, color='dodgerblue')
    plt.xlabel(selected_variable)
    plt.ylabel("Frequency")
    plt.title(f"Bar Chart for {selected_variable}")
    plt.xticks(rotation=45)
    st.pyplot()


# Create a Streamlit app
st.write("Teams Attributes Correlation Heatmap")

# Checkbox to show the heatmap
show_heatmap = st.checkbox("Show Correlation Heatmap for Teams Attributes")

# Check if the user selected the checkbox
if show_heatmap:
    st.subheader("Correlation Heatmap of Teams Attributes")
    st.write("Explore the relationships between numerical team attributes.")
    
    # Create a heatmap of numerical attribute correlations
    plt.figure(figsize=(16, 14))
    sns.heatmap(teams_data[variables_to_plot].corr(), cmap='coolwarm', annot=True, fmt='.2f')
    plt.title("Heatmap Showing Relationship Between Numerical Team Attributes")
    st.pyplot()


# Create a Streamlit app
st.subheader("Top 10 Teams by Team Attribute")

# Dropdown to select a player attribute
attribute_options = ['defenceAggression', 'defenceTeamWidth', 'defencePressure',
                     'buildUpPlayPassing', 'chanceCreationCrossing',
                     'chanceCreationShooting', 'chanceCreationPassing', 'buildUpPlaySpeed']

selected_attribute = st.selectbox("Select a team attribute", [''] + attribute_options)

if selected_attribute:
    # Calculate the average of the selected attribute for each player
    top_teams = teams_data.groupby(['team_long_name']).agg({
        selected_attribute: 'mean'
    }).reset_index()

    # Sort the player data by the average of the selected attribute in descending order
    top_teams = top_teams.sort_values(by=selected_attribute, ascending=False).head(10)

    # Display the top 10 players with the highest average score in the selected attribute
    st.subheader(f"Top 10 Teams with Highest {selected_attribute}")
    st.table(top_teams)

    # Create a bar chart to visualize the top 10 players
    fig, ax = plt.subplots(figsize=(10, 6))
    top_teams.plot(x='team_long_name', y=selected_attribute, kind='bar', ax=ax, color='tomato')
    plt.xlabel("Team Name")
    plt.ylabel(selected_attribute)
    plt.title(f"Top 10 Teams with Highest {selected_attribute}")
    st.pyplot(fig)
else:
    st.warning("Please select a team attribute to view the top teams based on attribute selected.")


# matches data
st.title('Analysis on Matches')

matches_data = matches[['id', 'country_id', 'league_id',  'season', 'stage', 'date', 'match_api_id', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal']]


#lets convert the date columnd to the correct data type 
matches_data['date'] = pd.to_datetime(matches_data['date'])

#creating a new column for home and away teams goals difference
matches_data['HomeTeamGD']=matches_data['home_team_goal']-matches_data['away_team_goal']  
matches_data['AwayTeamGD']=matches_data['away_team_goal']-matches_data['home_team_goal']
#creating a column for drwan matches 
matches_data['Draw']=matches_data['home_team_goal']==matches_data['away_team_goal']


#adding a column for teams match status 
def match_status(initial = 0):
    if initial > 0:
        return 'W'
    elif initial == 0:
        return 'D'
    else:
        return 'L'
matches_data['HomeResults'] = matches_data['HomeTeamGD'].apply(match_status)
matches_data['AwayResults'] = matches_data['AwayTeamGD'].apply(match_status)

#calculating points for teams (win=3, draw=1, lose=0)
def match_status2(initial2 = 'w'):
    if initial2 =='W':
        return 3
    elif initial2 =='D':
        return 1
    else:
        return 0
matches_data['HTPoints'] = matches_data['HomeResults'].apply(match_status2)
matches_data['ATPoints'] = matches_data['AwayResults'].apply(match_status2)

#counting the number of wins for each team
def check_wins(wins='W'):
    
    if wins=='W':
        
        return 1
    else:
        return 0
    
matches_data['HomeWin'] = matches_data['HomeResults'].apply(check_wins)
matches_data['AwayWin'] = matches_data['AwayResults'].apply(check_wins)


# Show first rows of the data
if st.checkbox("Show Matches Data"):

    st.dataframe(matches_data.head())

# Number of matches in the dataset
if st.checkbox('Show Number of Matches in the Dataset'):
    num_matches = matches_data['match_api_id'].nunique()
    st.write(f"Number of matches in the dataset: {num_matches}")


# Descriptive statistics
st.write("Descriptive Statistics of Matchres.")
if st.checkbox("Show Descriptive Statistics of Matches"):
    st.write(matches_data.describe())



# Join matches data with home team information to get match results for each team
matches_home = teams_data.merge(matches_data, left_on='team_api_id', right_on='home_team_api_id', how='inner')

# Join matches data with home team information to get match results for each team
matches_away = teams_data.merge(matches_data, left_on='team_api_id', right_on='away_team_api_id', how='inner')

# Concatenate home and away matches data into one dataframe
all_matches = pd.concat([matches_home, matches_away], ignore_index=True)

# Group the data by 'team ap id' and remove duplicates in the 'date' column for each team
all_matches = all_matches.groupby('team_api_id').apply(lambda group: group.drop_duplicates(subset=['date_y'])).reset_index(drop=True)

matches_home = teams_data.merge(matches_data, left_on='team_api_id', right_on='home_team_api_id', how='inner')



# List of independent variables
independent_vars = ['buildUpPlaySpeedClass', 'buildUpPlayDribblingClass', 'buildUpPlayPassingClass',
                    'buildUpPlayPositioningClass', 'chanceCreationPassingClass', 'chanceCreationCrossingClass',
                    'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressureClass',
                    'defenceAggressionClass', 'defenceTeamWidthClass', 'defenceDefenderLineClass']

# Streamlit app
st.subheader("Impact of Team Playing Attribute on Home Matches Results")

# Add text to the app
st.write("The statistical tests performed on various team playing attributes have provided insights into their statistical significance in relation to match outcomes (Win, Draw, Loss). \
         This suggests that these attributes are not influenced by mere chance, but they have a meaningful impact on whether a team wins, draws, or loses a match")

# Dropdown to select the variable
selected_variable = st.selectbox("Select a Variable:", independent_vars)

# Plot the heatmap when a variable is selected
if selected_variable:
    plt.figure(figsize=(8, 8))
    crosstab = pd.crosstab(matches_home[selected_variable], matches_home['HomeResults'], normalize=True) * 100
    sns.heatmap(crosstab, annot=True, fmt=".2f", cmap="YlGnBu")
    plt.title(f'{selected_variable} vs. HomeResults')
    plt.xlabel('HomeResults')
    plt.ylabel(selected_variable)

    # Add text about the values in the heatmap
    st.write(f"The values in the heatmap represent the percentage distribution of match outcomes (Win, Draw, Loss) based on the selected variable and Home Results.")

    # Show the plot in Streamlit
    st.pyplot(plt)



away_independent_vars = ['buildUpPlaySpeedClass', 'buildUpPlayDribblingClass', 'buildUpPlayPassingClass',
                    'buildUpPlayPositioningClass', 'chanceCreationPassingClass', 'chanceCreationCrossingClass',
                    'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressureClass',
                    'defenceAggressionClass', 'defenceTeamWidthClass', 'defenceDefenderLineClass']

st.subheader("Impact of Variables on Away Matches Results")

# Dropdown to select the variable
away_selected_variable = st.selectbox("Select Variable:", away_independent_vars)

# Plot the heatmap when a variable is selected
if away_selected_variable:
    plt.figure(figsize=(8, 8))
    crosstab = pd.crosstab(matches_away[away_selected_variable], matches_away['AwayResults'], normalize=True) * 100
    sns.heatmap(crosstab, annot=True, cmap="YlGnBu")
    plt.title(f'{away_selected_variable} vs. AwayResults')
    plt.xlabel('Away Results')
    plt.ylabel(away_selected_variable)

    # Show the plot in Streamlit
    st.pyplot(plt)


# Display your name in the sidebar
st.sidebar.write("Developed by Simon-Peter Osadiapét")

# Display your picture next to your name
picture = "osadiapet.jpg"  
st.sidebar.image(picture, use_column_width=True, caption="Simon-Peter Osadiapét")

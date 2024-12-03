import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set wide page and add app title
st.set_page_config(page_title="IPL Granular Data Analysis (2008 - 2024)", layout="wide", initial_sidebar_state='expanded')

# Load datasets (matches, deliveries)
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# Map old team names to new team names (Team Name Normalization)
team_name_mapping = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Deccan Chargers": "Sunrisers Hyderabad"
    # Add more name changes as needed
}

# Apply team name normalization to the dataset
matches['team1'] = matches['team1'].replace(team_name_mapping)
matches['team2'] = matches['team2'].replace(team_name_mapping)
matches['winner'] = matches['winner'].replace(team_name_mapping)
matches['toss_winner'] = matches['toss_winner'].replace(team_name_mapping)
deliveries['batting_team'] = deliveries['batting_team'].replace(team_name_mapping)
deliveries['bowling_team'] = deliveries['bowling_team'].replace(team_name_mapping)


# Sidebar for navigation and filters
st.sidebar.image("https://www.hindustantimes.com/ht-img/img/2024/04/12/550x309/IPL_Elections_Poll_Symbol_Party_Fun_Viral_1712913503946_1712913511352.jpg", width=300)
st.sidebar.title("🏏 IPL Data Explorer")


# Helper function for Select All functionality
def add_select_all_option(options, select_all_label="Select All"):
    if select_all_label not in options:
        options.insert(0, select_all_label)
    return options

# Seasons Dropdown
seasons = sorted(matches['season'].unique())
seasons = add_select_all_option(seasons)  # Add 'Select All' to seasons dropdown
season_selected = st.sidebar.multiselect("Select Seasons", seasons, default="Select All")

if "Select All" in season_selected or not season_selected:
    season_selected = matches['season'].unique()  # Select all if 'Select All' is chosen

# Teams Dropdown (including name changes)
teams = sorted(matches['team1'].unique())  # Both team1 and team2 contain all teams
teams = add_select_all_option(teams)  # Add 'Select All' to teams dropdown
team_selected = st.sidebar.multiselect("Select Teams", teams, default="Select All")

if "Select All" in team_selected or not team_selected:
    team_selected = matches['team1'].unique()  # Select all teams if 'Select All' is chosen

# Venues Dropdown
venues = sorted(matches['venue'].unique())
venues = add_select_all_option(venues)  # Add 'Select All' to venues dropdown
venue_selected = st.sidebar.multiselect("Select Venues", venues, default="Select All")

if "Select All" in venue_selected or not venue_selected:
    venue_selected = matches['venue'].unique()  # Select all venues if 'Select All' is chosen

# Filter matches based on sidebar input
filtered_matches = matches[(matches['season'].isin(season_selected)) & 
                           (matches['team1'].isin(team_selected) | matches['team2'].isin(team_selected)) &
                           (matches['venue'].isin(venue_selected))]
filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]

page = st.sidebar.selectbox("Navigate", ["Overview", "Team Analytics", "Player Stats", "Seasonal Analysis", "Detailed Match Data", "Venue Stats"])


# Overview Page
if page == "Overview":
    st.title("IPL Granular Data Analysis (2008 - 2024)")
    st.write("Explore **every aspect** of IPL from 2008 to 2024 in this detailed app. From team statistics, player performance, season trends, to venue analysis—everything is covered!")
    
    # High-Level Stats
    st.write("### Overall IPL Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Matches", len(matches))
    col2.metric("Total Runs", deliveries['total_runs'].sum())
    col3.metric("Total Wickets", deliveries[deliveries['dismissal_kind'].notna()]['dismissal_kind'].count())
    col4.metric("Total Players", deliveries['batter'].nunique())

    # Show filtered matches and deliveries data on user request
    if st.checkbox("Show filtered match data"):
        st.write(filtered_matches)
    if st.checkbox("Show filtered delivery data"):
        st.write(filtered_deliveries)

# Team Analytics Page
elif page == "Team Analytics":
    st.title("Team Performance Analytics")

    # Wins by Teams
    st.write("### Team Wins and Performance")
    team_wins = filtered_matches['winner'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=team_wins.values, y=team_wins.index, palette="coolwarm", ax=ax)
    ax.set_title("Total Wins by Teams (Filtered)", fontsize=16)
    ax.set_xlabel("Number of Wins")
    ax.set_ylabel("Teams")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, str(int(i.get_width())), fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)
    
    # Batting Performance of Teams
    st.write("### Total Runs Scored by Each Team")
    team_runs = filtered_deliveries.groupby('batting_team')['total_runs'].sum()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=team_runs.values, y=team_runs.index, palette="Blues", ax=ax)
    ax.set_title("Total Runs by Teams", fontsize=16)
    ax.set_xlabel("Total Runs")
    ax.set_ylabel("Teams")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, str(int(i.get_width())), fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)

    # Advanced Stats: Win Margins
    st.write("### Win Margins: Runs vs. Wickets")
    win_by_runs = filtered_matches[filtered_matches['result'] == 'runs']['result_margin']
    win_by_wickets = filtered_matches[filtered_matches['result'] == 'wickets']['result_margin']

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    sns.histplot(win_by_runs, bins=20, color='lightcoral', ax=ax[0])
    ax[0].set_title("Win by Runs", fontsize=14)
    ax[0].set_xlabel("Win Margin (Runs)")
    ax[0].set_ylabel("Frequency")
    
    sns.histplot(win_by_wickets, bins=10, color='skyblue', ax=ax[1])
    ax[1].set_title("Win by Wickets", fontsize=14)
    ax[1].set_xlabel("Win Margin (Wickets)")
    ax[1].set_ylabel("Frequency")
    
    st.pyplot(fig)

# Player Stats Page
elif page == "Player Stats":
    st.title("Detailed Player Statistics")
    
    # Top Run Scorers
    st.write("### Top Run Scorers")
    top_scorers = filtered_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_scorers.values, y=top_scorers.index, palette="magma", ax=ax)
    ax.set_title("Top 10 Batsmen (Filtered)", fontsize=16)
    ax.set_xlabel("Total Runs")
    ax.set_ylabel("Batsmen")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, str(int(i.get_width())), fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)

    # Top Wicket Takers
    st.write("### Top Wicket Takers")
    top_wicket_takers = filtered_deliveries[filtered_deliveries['dismissal_kind'].notna()]
    top_wicket_takers = top_wicket_takers.groupby('bowler')['dismissal_kind'].count().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=top_wicket_takers.values, y=top_wicket_takers.index, palette="cividis", ax=ax)
    ax.set_title("Top 10 Bowlers (Filtered)", fontsize=16)
    ax.set_xlabel("Wickets Taken")
    ax.set_ylabel("Bowlers")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, str(int(i.get_width())), fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)

    # Strike Rates (Granular)
    st.write("### Batsman Strike Rates (Filtered)")
    batsman_balls = filtered_deliveries.groupby('batter')['ball'].count()
    batsman_strike_rate = (top_scorers / batsman_balls * 100).sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=batsman_strike_rate.values, y=batsman_strike_rate.index, palette="inferno", ax=ax)
    ax.set_title("Top Batsmen by Strike Rate", fontsize=16)
    ax.set_xlabel("Strike Rate")
    ax.set_ylabel("Batsmen")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, f"{i.get_width():.2f}", fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)

# Season Analysis Page
elif page == "Seasonal Analysis":
    st.title("Seasonal Trends & Statistics")

    # Season-wise Match Count
    st.write("### Matches per Season")
    matches_per_season = filtered_matches.groupby('season')['id'].count()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.lineplot(x=matches_per_season.index, y=matches_per_season.values, marker='o', ax=ax)
    ax.set_title("Matches Played per Season", fontsize=16)
    ax.set_xlabel("Season")
    ax.set_ylabel("Number of Matches")
    
    # Adding data labels to line plot
    for i in range(matches_per_season.size):
        ax.text(matches_per_season.index[i], matches_per_season.values[i], str(matches_per_season.values[i]), fontsize=10, ha='center', va='bottom')
    
    st.pyplot(fig)
    
    # Season-wise Total Runs
    st.write("### Total Runs per Season")
    runs_per_season = filtered_deliveries.groupby('match_id')['total_runs'].sum().reset_index()
    runs_per_season = runs_per_season.merge(filtered_matches[['id', 'season']], left_on='match_id', right_on='id')
    total_runs_season = runs_per_season.groupby('season')['total_runs'].sum()
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.lineplot(x=total_runs_season.index, y=total_runs_season.values, marker='o', color='green', ax=ax)
    ax.set_title("Total Runs per Season", fontsize=16)
    ax.set_xlabel("Season")
    ax.set_ylabel("Total Runs")
    
    # Adding data labels to line plot
    for i in range(total_runs_season.size):
        ax.text(total_runs_season.index[i], total_runs_season.values[i], str(total_runs_season.values[i]), fontsize=10, ha='center', va='bottom')
    
    st.pyplot(fig)

# Venue Stats Page
elif page == "Venue Stats":
    st.title("Venue Performance")
    
    # Matches Played at Each Venue
    st.write("### Matches Played at Different Venues")
    matches_per_venue = filtered_matches['venue'].value_counts()
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=matches_per_venue.values, y=matches_per_venue.index, palette="crest", ax=ax)
    ax.set_title("Matches Played per Venue", fontsize=16)
    ax.set_xlabel("Number of Matches")
    ax.set_ylabel("Venues")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, str(int(i.get_width())), fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)
    
    # Average Runs at Each Venue
    st.write("### Average Runs Scored at Venues")
    venue_runs = filtered_deliveries.groupby('match_id')['total_runs'].sum().reset_index()
    venue_runs = venue_runs.merge(filtered_matches[['id', 'venue']], left_on='match_id', right_on='id')
    avg_runs_per_venue = venue_runs.groupby('venue')['total_runs'].mean().sort_values(ascending=False)
    
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x=avg_runs_per_venue.values, y=avg_runs_per_venue.index, palette="plasma", ax=ax)
    ax.set_title("Average Runs per Venue", fontsize=16)
    ax.set_xlabel("Average Runs")
    ax.set_ylabel("Venues")
    
    # Adding data labels to each bar
    for i in ax.patches:
        ax.text(i.get_width() + 3, i.get_y() + 0.5, f"{i.get_width():.2f}", fontsize=12, color='black', ha='left')
    
    st.pyplot(fig)

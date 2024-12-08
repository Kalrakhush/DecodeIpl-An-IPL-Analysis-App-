import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
# Set wide page and add app title
st.set_page_config(page_title="IPL Granular Data Analysis (2008 - 2024)", layout="wide", initial_sidebar_state='expanded')

# Load datasets (matches, deliveries)
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    matches['date'] = pd.to_datetime(matches['date'])
    return matches, deliveries

matches, deliveries = load_data()

# Map old team names to new team names (Team Name Normalization)
team_name_mapping = {
    "Delhi Daredevils": "Delhi Capitals",
    "Kings XI Punjab": "Punjab Kings",
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Deccan Chargers": "Sunrisers Hyderabad",
    "Gujarat Lions":"Gujarat Titans",
    "Royal Challengers Bangalore":"Royal Challengers Bengaluru",
    # Add more name changes as needed
}

venue_mapping = {
    # M Chinnaswamy Stadium
    "M Chinnaswamy Stadium": "M Chinnaswamy Stadium",
    "M.Chinnaswamy Stadium": "M Chinnaswamy Stadium",
    "M Chinnaswamy Stadium, Bengaluru": "M Chinnaswamy Stadium",
    
    # Punjab Cricket Association IS Bindra Stadium
    "Punjab Cricket Association Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali": "Punjab Cricket Association IS Bindra Stadium",
    "Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh": "Punjab Cricket Association IS Bindra Stadium",
    
    # Arun Jaitley Stadium
    "Feroz Shah Kotla": "Arun Jaitley Stadium",
    "Arun Jaitley Stadium": "Arun Jaitley Stadium",
    "Arun Jaitley Stadium, Delhi": "Arun Jaitley Stadium",
    
    # Wankhede Stadium
    "Wankhede Stadium": "Wankhede Stadium",
    "Wankhede Stadium, Mumbai": "Wankhede Stadium",
    
    # Eden Gardens
    "Eden Gardens": "Eden Gardens",
    "Eden Gardens, Kolkata": "Eden Gardens",
    
    # Sawai Mansingh Stadium
    "Sawai Mansingh Stadium": "Sawai Mansingh Stadium",
    "Sawai Mansingh Stadium, Jaipur": "Sawai Mansingh Stadium",
    
    # Rajiv Gandhi International Stadium
    "Rajiv Gandhi International Stadium": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal": "Rajiv Gandhi International Stadium",
    "Rajiv Gandhi International Stadium, Uppal, Hyderabad": "Rajiv Gandhi International Stadium",
    
    # MA Chidambaram Stadium
    "MA Chidambaram Stadium": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk": "MA Chidambaram Stadium",
    "MA Chidambaram Stadium, Chepauk, Chennai": "MA Chidambaram Stadium",
    
    # Dr DY Patil Sports Academy
    "Dr DY Patil Sports Academy": "Dr DY Patil Sports Academy",
    "Dr DY Patil Sports Academy, Mumbai": "Dr DY Patil Sports Academy",
    
    # Narendra Modi Stadium
    "Sardar Patel Stadium, Motera": "Narendra Modi Stadium",
    "Narendra Modi Stadium, Ahmedabad": "Narendra Modi Stadium",
    
    # Himachal Pradesh Cricket Association Stadium
    "Himachal Pradesh Cricket Association Stadium": "Himachal Pradesh Cricket Association Stadium",
    "Himachal Pradesh Cricket Association Stadium, Dharamsala": "Himachal Pradesh Cricket Association Stadium",
    
    # Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium
    "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow": "Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium",
    
    # Barsapara Cricket Stadium
    "Barsapara Cricket Stadium, Guwahati": "Barsapara Cricket Stadium",
    
    # Vidarbha Cricket Association Stadium
    "Vidarbha Cricket Association Stadium, Jamtha": "Vidarbha Cricket Association Stadium",
    
    # Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium",
    "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium, Visakhapatnam": "Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium",
    
    # Maharashtra Cricket Association Stadium
    "Maharashtra Cricket Association Stadium": "Maharashtra Cricket Association Stadium",
    "Maharashtra Cricket Association Stadium, Pune": "Maharashtra Cricket Association Stadium",
    
    # Green Park
    "Green Park": "Green Park",
    
    # Brabourne Stadium
    "Brabourne Stadium": "Brabourne Stadium",
    "Brabourne Stadium, Mumbai": "Brabourne Stadium",
    
    # Shaheed Veer Narayan Singh International Stadium
    "Shaheed Veer Narayan Singh International Stadium": "Shaheed Veer Narayan Singh International Stadium",
    
    # JSCA International Stadium Complex
    "JSCA International Stadium Complex": "JSCA International Stadium Complex",
    
    # Sheikh Zayed Stadium
    "Sheikh Zayed Stadium": "Sheikh Zayed Stadium",
    "Zayed Cricket Stadium, Abu Dhabi": "Sheikh Zayed Stadium",
    
    # Sharjah Cricket Stadium
    "Sharjah Cricket Stadium": "Sharjah Cricket Stadium",
    
    # Dubai International Cricket Stadium
    "Dubai International Cricket Stadium": "Dubai International Cricket Stadium",
    
    # Newlands
    "Newlands": "Newlands",
    
    # St George's Park
    "St George's Park": "St George's Park",
    
    # Kingsmead
    "Kingsmead": "Kingsmead",
    
    # SuperSport Park
    "SuperSport Park": "SuperSport Park",
    
    # Buffalo Park
    "Buffalo Park": "Buffalo Park",
    
    # New Wanderers Stadium
    "New Wanderers Stadium": "New Wanderers Stadium",
    
    # De Beers Diamond Oval
    "De Beers Diamond Oval": "De Beers Diamond Oval",
    
    # OUTsurance Oval
    "OUTsurance Oval": "OUTsurance Oval",
    
    # Barabati Stadium
    "Barabati Stadium": "Barabati Stadium",
    
    # Nehru Stadium
    "Nehru Stadium": "Nehru Stadium",
    
    # Holkar Cricket Stadium
    "Holkar Cricket Stadium": "Holkar Cricket Stadium",
    
    # Maharaja Yadavindra Singh International Cricket Stadium
    "Maharaja Yadavindra Singh International Cricket Stadium, Mullanpur": "Maharaja Yadavindra Singh International Cricket Stadium",
    
    # Saurashtra Cricket Association Stadium
    "Saurashtra Cricket Association Stadium": "Saurashtra Cricket Association Stadium"
}




# Apply team name normalization to the dataset
matches['team1'] = matches['team1'].replace(team_name_mapping)
matches['team2'] = matches['team2'].replace(team_name_mapping)
matches['winner'] = matches['winner'].replace(team_name_mapping)
matches['toss_winner'] = matches['toss_winner'].replace(team_name_mapping)
deliveries['batting_team'] = deliveries['batting_team'].replace(team_name_mapping)
deliveries['bowling_team'] = deliveries['bowling_team'].replace(team_name_mapping)

# Apply venue name normalization to the dataset
matches['venue'] = matches['venue'].replace(venue_mapping)

# Sidebar for navigation and filters
st.sidebar.image("https://www.hindustantimes.com/ht-img/img/2024/04/12/550x309/IPL_Elections_Poll_Symbol_Party_Fun_Viral_1712913503946_1712913511352.jpg", width=300)
st.sidebar.title("🏏 IPL Data Explorer")

# Helper function for Select All functionality
def handle_select_all(selected_items, all_items, select_all_label="Select All"):
    if select_all_label in selected_items:
        return all_items
    return selected_items

# Sidebar: Use expander to make large sections collapsible
with st.sidebar.expander("Filters", expanded=True):
    # Seasons Dropdown (add search functionality and better handling for 'Select All')
    seasons = sorted(matches['season'].unique())
    season_selected = st.multiselect("Select Seasons", ["Select All"] + seasons, default="Select All", help="Search or select seasons")
    season_selected = handle_select_all(season_selected, seasons)
    
    # Teams Dropdown
    teams = sorted(matches['team1'].unique())
    team_selected = st.multiselect("Select Teams", ["Select All"] + teams, default="Select All", help="Search or select teams")
    team_selected = handle_select_all(team_selected, teams)
    
    # Remove any duplicate venue names after mapping and ensure only unique venues
    venues = sorted(matches['venue'].unique())

    # Sidebar: Venues Dropdown (to save space for long lists and ensure no duplicates)
    venue_selected = st.multiselect("Select Venues", ["Select All"] + venues, default="Select All", help="Search or select venues")
    venue_selected = handle_select_all(venue_selected, venues)




# Clear All Button
if st.sidebar.button("Clear All Filters"):
    season_selected = seasons
    team_selected = teams
    venue_selected = venues
# Filter matches based on selected venues
filtered_matches = matches[
    (matches['season'].isin(season_selected)) & 
    ((matches['team1'].isin(team_selected)) | (matches['team2'].isin(team_selected))) & 
    (matches['venue'].isin(venue_selected))
]

filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]

# Handle 'Overview' navigation page
page = st.sidebar.selectbox("Navigate", ["Overview", "Team Analytics", "Player Stats", "Seasonal Analysis", "Detailed Match Data", "Venue Stats"])

if page == "Overview":
    st.title("DecodeIPL")
    st.write("Explore **every aspect** of IPL from 2008 to 2024 in this detailed app. From team statistics, player performance, season trends, to venue analysis—everything is covered!")

    # High-Level Stats (filtered)
    st.write("### IPL Statistics")
    col1, col2, col3, col4 = st.columns(4)

    # Calculate metrics using filtered_matches and filtered_deliveries
    col1.metric("Total Matches", len(filtered_matches))
    col2.metric("Total Runs", filtered_deliveries['total_runs'].sum())
    col3.metric("Total Wickets", filtered_deliveries[filtered_deliveries['dismissal_kind'].notna()]['dismissal_kind'].count())
    col4.metric("Total Players", filtered_deliveries['batter'].nunique())

    # Interactive Team, Player, Venue connections (filtered data)
    st.write("### Interactive Filters")

    # Style for smaller text
    small_text_style = """
        <style>
        .small-text {
            font-size: 14px; /* You can adjust the size here */
        }
        </style>
    """

    # Inject custom style
    st.markdown(small_text_style, unsafe_allow_html=True)

    # Display the filtered team, venue, and season selections with small font
    st.markdown(f"<p class='small-text'>Matches for selected Teams: {', '.join(team_selected)}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='small-text'>Matches at selected Venues: {', '.join(venue_selected)}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='small-text'>Seasons: {', '.join(map(str, season_selected))}</p>", unsafe_allow_html=True)


    # Dynamic Data Tables based on user input
    st.write("### Filtered Matches and Deliveries")
    if st.checkbox("Show filtered match data"):
        st.write(filtered_matches[['id', 'season', 'team1', 'team2', 'venue', 'winner']])
    
    if st.checkbox("Show filtered delivery data"):
        st.write(filtered_deliveries[['match_id', 'over', 'ball', 'batter', 'bowler', 'total_runs', 'dismissal_kind']])
    


elif page == "Team Analytics":
    st.title("Team Performance Analytics")

    # High-Level Metrics for Selected Teams
    st.write("### Team Statistics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Selected Teams", len(team_selected))
    col2.metric("Selected Venues", len(venue_selected))
    col3.metric("Selected Seasons", len(season_selected))
    col4.metric("Total Matches", len(filtered_matches))

    st.write("### Metrics for Selected Teams")
    for team in team_selected:
        team_data = filtered_matches[(filtered_matches['team1'] == team) | (filtered_matches['team2'] == team)]
        total_matches = len(team_data)
        team_wins = team_data['winner'].value_counts().get(team, 0)
        team_runs = filtered_deliveries[filtered_deliveries['batting_team'] == team]['total_runs'].sum()
        team_wickets = filtered_deliveries[
            (filtered_deliveries['bowling_team'] == team) & (filtered_deliveries['dismissal_kind'].notna())
        ]['dismissal_kind'].count()

        st.write(f"**{team}**")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Matches", total_matches)
        col2.metric("Wins", team_wins)
        col3.metric("Total Runs", team_runs)
        col4.metric("Wickets Taken", team_wickets)
    # Head-to-Head Analysis for Multiple Teams
    st.write("### Head-to-Head Analysis (Multiple Teams)")
    selected_teams = st.multiselect("Select Teams", options=team_selected, default=team_selected[:2])

    if len(selected_teams) > 1:
        # Filter matches for selected teams
        h2h_data = filtered_matches[
            (filtered_matches['team1'].isin(selected_teams)) & (filtered_matches['team2'].isin(selected_teams))
        ]
        
        # Create a DataFrame for H2H statistics (only focusing on wins)
        h2h_stats = []
        for team1 in selected_teams:
            for team2 in selected_teams:
                if team1 != team2:
                    matches_between = h2h_data[
                        ((h2h_data['team1'] == team1) & (h2h_data['team2'] == team2)) |
                        ((h2h_data['team1'] == team2) & (h2h_data['team2'] == team1))
                    ]
                    total_matches = len(matches_between)
                    team1_wins = matches_between['winner'].value_counts().get(team1, 0)
                    team2_wins = matches_between['winner'].value_counts().get(team2, 0)
                    
                    h2h_stats.append({
                        "Team 1": team1,
                        "Team 2": team2,
                        "Total Matches": total_matches,
                        "Team 1 Wins": team1_wins,
                        "Team 2 Wins": team2_wins
                    })
        
        h2h_df = pd.DataFrame(h2h_stats)
        st.write("#### Head-to-Head Data Summary")
        st.write(h2h_df)

                # Prepare data for head-to-head wins comparison
        h2h_long = pd.DataFrame({
            'Team 1': h2h_df['Team 1'],
            'Team 2': h2h_df['Team 2'],
            'Team 1 Wins': h2h_df['Team 1 Wins'],
            'Team 2 Wins': h2h_df['Team 2 Wins']
        })

        # Melt the dataframe to have wins for both teams in a single column
        h2h_long = h2h_long.melt(
            id_vars=["Team 1", "Team 2"], 
            value_vars=["Team 1 Wins", "Team 2 Wins"], 
            var_name="Win Type", 
            value_name="Wins"
        )

        # Extract team names from 'Win Type' to indicate the actual winning team
        h2h_long['Winning Team'] = h2h_long.apply(
            lambda row: row['Team 1'] if 'Team 1 Wins' in row['Win Type'] else row['Team 2'], axis=1
        )

        # Create the Altair chart for side-by-side bars for each team in the head-to-head matchups
        st.write("#### Head-to-Head Wins Comparison (Interactive)")

        chart = alt.Chart(h2h_long).mark_bar().encode(
            x=alt.X('Winning Team:N', title='Team', sort=selected_teams),
            y=alt.Y('Wins:Q', title='Number of Wins'),
            color=alt.Color('Winning Team:N', scale=alt.Scale(scheme='tableau10'), legend=alt.Legend(title="Winning Team")),
            column=alt.Column('Team 2:N', title='Opponent', header=alt.Header(labelOrient='bottom')),
            tooltip=['Team 1', 'Team 2', 'Winning Team', 'Wins']
        ).properties(
            title="Head-to-Head Wins Comparison for Selected Teams",
            width=200,
            height=300
        )

        st.altair_chart(chart, use_container_width=True)



    # Venue-Wise Winning Percentage
    st.write("### Winning Percentage by Venue")
    venue_wins = filtered_matches.groupby(['venue', 'winner']).size().unstack(fill_value=0)
    venue_wins['Total Matches'] = venue_wins.sum(axis=1)
    # Calculate Total Matches and Win %
    venue_wins['Total Matches'] = venue_wins.sum(axis=1)

    # Calculate Win % for each team
    win_percentage = venue_wins.iloc[:, :-1].div(venue_wins['Total Matches'], axis=0) * 100
    win_percentage['Total Matches'] = venue_wins['Total Matches']

    # Add percentages back to the original DataFrame
    venue_wins = pd.concat([venue_wins, win_percentage.add_suffix(' (%)')], axis=1)


    st.dataframe(venue_wins)

    # Boundary Analysis
    st.write("### Boundary Analysis: Fours and Sixes")
    boundary_data = filtered_deliveries.groupby('batting_team')[['batsman_runs']].apply(
        lambda x: (x == 4).sum() + (x == 6).sum()
    )
    st.bar_chart(boundary_data.rename(columns={0: 'Boundaries'}))

    # Economy Rate
    st.write("### Team Bowling Economy Rate")
    economy_data = filtered_deliveries.groupby('bowling_team').apply(
        lambda x: x['total_runs'].sum() / (x['over'].nunique() or 1)
    )
    st.bar_chart(economy_data)

    # Toss Impact Analysis (Enhanced)
    st.write("### Toss Impact on Team Performance")
    toss_data = filtered_matches.groupby(['toss_winner', 'winner']).size().reset_index(name='count')
    toss_data = toss_data.pivot('toss_winner', 'winner', 'count').fillna(0)

    toss_data = toss_data.apply(lambda row: row / row.sum() * 100 if row.sum() > 0 else row, axis=1)
    toss_chart = alt.Chart(toss_data.reset_index().melt('toss_winner')).mark_bar().encode(
        x=alt.X('toss_winner:N', title="Toss Winner"),
        y=alt.Y('value:Q', title="Winning Percentage"),
        color='winner:N',
        tooltip=['toss_winner', 'winner', 'value']
    ).properties(width=700, height=400, title="Toss Impact on Team Performance")

    st.altair_chart(toss_chart, use_container_width=True)

    # Runs Consistency Analysis
    st.write("### Consistency in Runs")
    thresholds = [150, 200]
    consistency_data = {f"Above {threshold} Runs": [] for threshold in thresholds}
    consistency_data["Team"] = []

    for team in team_selected:
        team_scores = filtered_deliveries[filtered_deliveries['batting_team'] == team].groupby('match_id')['total_runs'].sum()
        for threshold in thresholds:
            consistency_data[f"Above {threshold} Runs"].append((team_scores >= threshold).sum())
        consistency_data["Team"].append(team)

    consistency_df = pd.DataFrame(consistency_data)
    st.dataframe(consistency_df.set_index("Team"))

    # Wins vs Runs Analysis
    st.write("### Wins vs. Total Runs Analysis")
    team_stats = filtered_matches.groupby('winner').size().reset_index(name='wins')
    team_runs = filtered_deliveries.groupby('batting_team')['total_runs'].sum().reset_index(name='runs')
    merged_stats = team_stats.merge(team_runs, left_on='winner', right_on='batting_team').drop(columns=['batting_team'])
    merged_stats = merged_stats.rename(columns={'winner': 'Team'})

    wins_vs_runs_chart = alt.Chart(merged_stats).mark_circle(size=200).encode(
        x=alt.X('wins', title="Total Wins"),
        y=alt.Y('runs', title="Total Runs"),
        color='Team',
        tooltip=['Team', 'wins', 'runs']
    ).properties(width=700, height=400, title="Wins vs. Runs by Teams (Interactive)")

    st.altair_chart(wins_vs_runs_chart, use_container_width=True)


elif page == "Player Stats":
    st.title("Detailed Player Statistics")

    # Top Run Scorers with Altair
    st.write("### Top Run Scorers")
    top_scorers = filtered_deliveries.groupby('batter')['batsman_runs'].sum().reset_index().sort_values(by='batsman_runs', ascending=False).head(10)
    
    top_scorers_chart = alt.Chart(top_scorers).mark_bar().encode(
        x=alt.X('batsman_runs:Q', title="Total Runs"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'batsman_runs:Q']
    ).properties(
        title="Top 10 Batsmen by Runs"
    )
    st.altair_chart(top_scorers_chart, use_container_width=True)

    # Top Wicket Takers with Altair
    st.write("### Top Wicket Takers")
    top_wicket_takers = filtered_deliveries[filtered_deliveries['dismissal_kind'].notna()]
    top_wicket_takers = top_wicket_takers.groupby('bowler')['dismissal_kind'].count().reset_index().sort_values(by='dismissal_kind', ascending=False).head(10)
    
    top_wicket_takers_chart = alt.Chart(top_wicket_takers).mark_bar().encode(
        x=alt.X('dismissal_kind:Q', title="Wickets Taken"),
        y=alt.Y('bowler:N', title="Bowler", sort='-x'),
        color=alt.Color('bowler:N', legend=None),
        tooltip=['bowler:N', 'dismissal_kind:Q']
    ).properties(
        title="Top 10 Bowlers by Wickets"
    )
    st.altair_chart(top_wicket_takers_chart, use_container_width=True)

    # Batsman Strike Rates with Altair
    st.write("### Batsman Strike Rates")
    batsman_balls = filtered_deliveries.groupby('batter')['ball'].count()
    batsman_strike_rate = (top_scorers.set_index('batter')['batsman_runs'] / batsman_balls * 100).reset_index().sort_values(by=0, ascending=False).head(10)
    batsman_strike_rate = batsman_strike_rate.rename(columns={0: 'strike_rate'})
    
    strike_rate_chart = alt.Chart(batsman_strike_rate).mark_bar().encode(
        x=alt.X('strike_rate:Q', title="Strike Rate"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'strike_rate:Q']
    ).properties(
        title="Top 10 Batsmen by Strike Rate"
    )
    st.altair_chart(strike_rate_chart, use_container_width=True)

    # Top 10 Batsmen by Fours
    st.write("### Top 10 Batsmen by Fours")
    batsman_fours = filtered_deliveries[filtered_deliveries['batsman_runs'] == 4].groupby('batter').size().reset_index(name='fours')
    batsman_runs = filtered_deliveries.groupby('batter')['total_runs'].sum().reset_index(name='runs')

    batsman_stats = pd.merge(batsman_fours, batsman_runs, on='batter', how='left')

    batsman_fours_sorted = batsman_stats.sort_values(by='fours', ascending=False).head(10)

    fours_chart = alt.Chart(batsman_fours_sorted).mark_bar().encode(
        x=alt.X('fours:Q', title="Fours"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'fours:Q']
    ).properties(
        title="Top 10 Batsmen by Fours"
    )
    st.altair_chart(fours_chart, use_container_width=True)

    # Top 10 Batsmen by Sixes
    st.write("### Top 10 Batsmen by Sixes")
    batsman_sixes = filtered_deliveries[filtered_deliveries['batsman_runs'] == 6].groupby('batter').size().reset_index(name='sixes')
    batsman_runs = filtered_deliveries.groupby('batter')['total_runs'].sum().reset_index(name='runs')

    batsman_stats = pd.merge(batsman_sixes, batsman_runs, on='batter', how='left')

    batsman_sixes_sorted = batsman_stats.sort_values(by='sixes', ascending=False).head(10)

    sixes_chart = alt.Chart(batsman_sixes_sorted).mark_bar().encode(
        x=alt.X('sixes:Q', title="Sixes"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'sixes:Q']
    ).properties(
        title="Top 10 Batsmen by Sixes"
    )
    st.altair_chart(sixes_chart, use_container_width=True)

    # Batsman Strike Rate
    st.write("### Top 10 Batsmen by Strike Rate")
    batsman_balls = filtered_deliveries.groupby('batter')['ball'].count().reset_index(name='balls')
    batsman_runs = filtered_deliveries.groupby('batter')['total_runs'].sum().reset_index(name='runs')

    batsman_stats = pd.merge(batsman_runs, batsman_balls, on='batter')

    batsman_stats['strike_rate'] = (batsman_stats['runs'] / batsman_stats['balls']) * 100

    batsman_strike_rate_sorted = batsman_stats.sort_values(by='strike_rate', ascending=False).head(10)

    strike_rate_chart = alt.Chart(batsman_strike_rate_sorted).mark_bar().encode(
        x=alt.X('strike_rate:Q', title="Strike Rate"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'strike_rate:Q']
    ).properties(
        title="Top 10 Batsmen by Strike Rate"
    )
    st.altair_chart(strike_rate_chart, use_container_width=True)

    # Top 10 Batsmen by Average
    st.write("### Top 10 Batsmen by Average")
    batsman_dismissals = filtered_deliveries[filtered_deliveries['dismissal_kind'].notnull()].groupby('batter').size().reset_index(name='dismissals')

    batsman_stats = pd.merge(batsman_runs, batsman_dismissals, on='batter', how='left')

    batsman_stats['average'] = batsman_stats['runs'] / batsman_stats['dismissals']

    batsman_average_sorted = batsman_stats.sort_values(by='average', ascending=False).head(10)

    average_chart = alt.Chart(batsman_average_sorted).mark_bar().encode(
        x=alt.X('average:Q', title="Batting Average"),
        y=alt.Y('batter:N', title="Batsman", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'average:Q']
    ).properties(
        title="Top 10 Batsmen by Batting Average"
    )
    st.altair_chart(average_chart, use_container_width=True)

    # Average Runs per Over (Dynamic for each Player)
    st.write("### Average Runs per Over")
    runs_per_over = filtered_deliveries.groupby(['over', 'batter'])['total_runs'].sum().reset_index()
    runs_per_over_avg = runs_per_over.groupby('batter')['total_runs'].mean().reset_index().sort_values(by='total_runs', ascending=False).head(10)

    runs_per_over_chart = alt.Chart(runs_per_over_avg).mark_bar().encode(
        x=alt.X('total_runs:Q', title="Average Runs per Over"),
        y=alt.Y('batter:N', title="Batter", sort='-x'),
        color=alt.Color('batter:N', legend=None),
        tooltip=['batter:N', 'total_runs:Q']
    ).properties(
        title="Top 10 Batsmen by Average Runs per Over"
    )
    st.altair_chart(runs_per_over_chart, use_container_width=True)

    # Bowler Economy Rates for Bowlers (New Analysis)
    st.write("### Bowler Economy Rate")
    bowler_runs = filtered_deliveries.groupby('bowler')['total_runs'].sum().reset_index()
    bowler_balls = filtered_deliveries.groupby('bowler')['ball'].count().reset_index()

    bowler_stats = pd.merge(bowler_runs, bowler_balls, on='bowler')

    bowler_stats['economy_rate'] = bowler_stats['total_runs'] / (bowler_stats['ball'] / 6)

    bowler_economy_rate = bowler_stats.sort_values(by='economy_rate').head(10)

    economy_rate_chart = alt.Chart(bowler_economy_rate).mark_bar().encode(
        x=alt.X('economy_rate:Q', title="Economy Rate"),
        y=alt.Y('bowler:N', title="Bowler", sort='-x'),
        color=alt.Color('bowler:N', legend=None),
        tooltip=['bowler:N', 'economy_rate:Q']
    ).properties(
        title="Top 10 Bowlers by Economy Rate"
    )
    st.altair_chart(economy_rate_chart, use_container_width=True)

    # Top 10 Bowlers by Wickets
    st.write("### Top 10 Bowlers by Wickets")
    bowler_wickets = filtered_deliveries[filtered_deliveries['dismissal_kind'].notnull()].groupby('bowler').size().reset_index(name='wickets')

    bowler_stats = pd.merge(bowler_stats, bowler_wickets, on='bowler', how='left')

    bowler_wickets_sorted = bowler_stats.sort_values(by='wickets', ascending=False).head(10)

    wickets_chart = alt.Chart(bowler_wickets_sorted).mark_bar().encode(
        x=alt.X('wickets:Q', title="Wickets"),
        y=alt.Y('bowler:N', title="Bowler", sort='-x'),
        color=alt.Color('bowler:N', legend=None),
        tooltip=['bowler:N', 'wickets:Q']
    ).properties(
        title="Top 10 Bowlers by Wickets"
    )
    st.altair_chart(wickets_chart, use_container_width=True)

# bowler vs Batsman comparison
    # Step 1: Add selectbox for selecting specific batters and bowlers
    unique_batters = filtered_deliveries['batter'].unique()
    unique_bowlers = filtered_deliveries['bowler'].unique()

    selected_batter = st.selectbox('Select a Batter', unique_batters)
    selected_bowler = st.selectbox('Select a Bowler', unique_bowlers)

    # Step 2: Filter deliveries for the selected batter and bowler
    selected_deliveries = filtered_deliveries[
        (filtered_deliveries['batter'] == selected_batter) &
        (filtered_deliveries['bowler'] == selected_bowler)
    ]

    # Batsman Stats Calculation
    batsman_balls = selected_deliveries.groupby('batter')['ball'].count().reset_index(name='balls')
    batsman_runs = selected_deliveries.groupby('batter')['total_runs'].sum().reset_index(name='runs')
    batsman_stats = pd.merge(batsman_runs, batsman_balls, on='batter')

    batsman_stats['strike_rate'] = (batsman_stats['runs'] / batsman_stats['balls']) * 100

    batsman_dismissals = selected_deliveries[selected_deliveries['dismissal_kind'].notnull()].groupby('batter').size().reset_index(name='dismissals')
    batsman_stats = pd.merge(batsman_stats, batsman_dismissals, on='batter', how='left')
    batsman_stats['average'] = batsman_stats['runs'] / batsman_stats['dismissals']
    batsman_stats['average'] = batsman_stats['average'].fillna(0)

    batsman_comparison = batsman_stats[['batter', 'runs', 'strike_rate', 'average', 'dismissals']]

    # Bowler Stats Calculation
    bowler_balls = selected_deliveries.groupby('bowler')['ball'].count().reset_index(name='balls')
    bowler_runs_conceded = selected_deliveries.groupby('bowler')['total_runs'].sum().reset_index(name='runs_conceded')
    bowler_stats = pd.merge(bowler_balls, bowler_runs_conceded, on='bowler')

    bowler_stats['economy_rate'] = (bowler_stats['runs_conceded'] / (bowler_stats['balls'] / 6))
    bowler_wickets = selected_deliveries[selected_deliveries['dismissal_kind'].notnull()].groupby('bowler').size().reset_index(name='wickets')
    bowler_stats = pd.merge(bowler_stats, bowler_wickets, on='bowler', how='left')
    bowler_stats['wickets'] = bowler_stats['wickets'].fillna(0)

    bowler_comparison = bowler_stats[['bowler', 'economy_rate', 'wickets']]

    # Combine Batsman and Bowler Data for Comparison
    combined_data = pd.DataFrame({
        'Category': ['Runs', 'Strike Rate', 'Average', 'Dismissals', 'Economy Rate'],
        selected_batter: [
            batsman_stats['runs'].values[0], 
            batsman_stats['strike_rate'].values[0], 
            batsman_stats['average'].values[0], 
            batsman_stats['dismissals'].values[0], 
            None   # Economy Rate is for bowler
        ],
        selected_bowler: [
            None,  # Runs is for batsman
            None,  # Strike Rate is for batsman
            None,  # Average is for batsman
            None,  # Dismissals is for batsman
            bowler_stats['economy_rate'].values[0]
        ]
    })

    # Step 3: Batsman vs Bowler Comparison Chart (Advanced Visuals with Altair)
    comparison_chart = alt.Chart(combined_data.melt(id_vars='Category', var_name='Player', value_name='Value')).mark_bar().encode(
        x=alt.X('Value:Q', title='Performance Metric'),
        y=alt.Y('Category:N', title="Statistic"),
        color='Player:N',
        tooltip=['Category', 'Value']
    ).properties(
        title=f"Batsman vs Bowler Comparison: {selected_batter} vs {selected_bowler}",
        width=600,
        height=300
    ).interactive()

    st.altair_chart(comparison_chart, use_container_width=True)

    # Step 4: Consistency in Runs (Above Thresholds)
    st.write("### Consistency in Runs (Above Thresholds)")

    thresholds = [50, 100, 150]
    consistency_data = {f"Above {threshold} Runs": [] for threshold in thresholds}
    consistency_data["Player"] = []

    # Calculate consistency for each player
    for player in filtered_deliveries['batter'].unique():
        player_runs = filtered_deliveries[filtered_deliveries['batter'] == player].groupby('match_id')['total_runs'].sum()
        for threshold in thresholds:
            consistency_data[f"Above {threshold} Runs"].append((player_runs >= threshold).sum())
        consistency_data["Player"].append(player)

    consistency_df = pd.DataFrame(consistency_data)

    # Select a player for consistency visualization
    selected_player = st.selectbox('Select a Player for Consistency Analysis', unique_batters)

    player_consistency = consistency_df[consistency_df['Player'] == selected_player]

    # Step 5: Consistency Chart using Altair
    consistency_chart = alt.Chart(player_consistency.melt(id_vars='Player', var_name='Threshold', value_name='Matches')).mark_bar().encode(
        x='Threshold:N',
        y='Matches:Q',
        color='Threshold:N',
        tooltip=['Matches']
    ).properties(
        title=f"Consistency of {selected_player} in Scoring Above Run Thresholds",
        width=400,
        height=500
    ).interactive()

    st.altair_chart(consistency_chart, use_container_width=True)

    # Step 6: Show Consistency Data in Table
    st.write("### Consistency Data")
    st.dataframe(consistency_df.set_index("Player"))
elif page == "Seasonal Analysis":
    st.title("Seasonal Performance Analysis")

    # Merge deliveries with matches to include season data
    deliveries_with_season = deliveries.merge(matches[['id', 'season']], left_on='match_id', right_on='id', how='left')

    # 1. Team Performance (Wins by Season)
    st.subheader("1. Team Performance (Wins by Season)")
    team_wins_by_season = filtered_matches.groupby(['season', 'winner']).size().reset_index(name='wins')

    # Improved: Changed chart to bar for better readability in a categorical axis like 'season'
    win_chart = alt.Chart(team_wins_by_season).mark_bar().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('wins:Q', title='Total Wins'),
        color='winner:N',
        tooltip=['season', 'winner', 'wins']
    ).properties(width=800, height=400, title="Team Wins by Season")

    st.altair_chart(win_chart, use_container_width=True)

    # 2. Seasonal Runs and Wickets Trends
    st.subheader("2. Seasonal Runs and Wickets Trends")
    runs_by_season = deliveries_with_season.groupby(['season'])['total_runs'].sum().reset_index()
    wickets_by_season = deliveries_with_season[deliveries_with_season['dismissal_kind'].notna()].groupby(['season'])['dismissal_kind'].count().reset_index()

    # Combine runs and wickets for the dual-axis chart
    combined_data = pd.merge(runs_by_season, wickets_by_season, on='season')
    combined_data.rename(columns={'total_runs': 'Total Runs', 'dismissal_kind': 'Total Wickets'}, inplace=True)

    # Improved: Separated the two metrics into lines for clarity, labeled axes with unique scales
    runs_line = alt.Chart(combined_data).mark_line(point=True, color='blue').encode(
        x=alt.X('season:O', title="Season"),
        y=alt.Y('Total Runs:Q', title="Total Runs"),
        tooltip=['season', 'Total Runs']
    )

    wickets_line = alt.Chart(combined_data).mark_line(point=True, color='red').encode(
        x=alt.X('season:O', title="Season"),
        y=alt.Y('Total Wickets:Q', title="Total Wickets", axis=alt.Axis(grid=False)),
        tooltip=['season', 'Total Wickets']
    )

    combined_chart = alt.layer(runs_line, wickets_line).resolve_scale(
        y='independent'  # Separate scales for runs and wickets
    ).properties(width=800, height=400, title="Total Runs and Wickets by Season")

    st.altair_chart(combined_chart, use_container_width=True)

    # 3. Batting and Bowling Consistency by Season
    st.subheader("3. Batting and Bowling Consistency by Season")

    # Improved: Added a filter to show top performers in each season for better focus
    top_batsmen = deliveries_with_season.groupby(['season', 'batter'])['batsman_runs'].sum().reset_index()
    top_batsmen = top_batsmen.groupby('season').apply(lambda x: x.nlargest(10, 'batsman_runs')).reset_index(drop=True)

    # Heatmap for batting performances
    batting_heatmap = alt.Chart(top_batsmen).mark_rect().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('batter:N', title='Batter'),
        color=alt.Color('batsman_runs:Q', scale=alt.Scale(scheme='blues')),
        tooltip=['batter', 'season', 'batsman_runs']
    ).properties(width=800, height=400, title="Top 10 Batting Performances (Total Runs by Season)")

    st.altair_chart(batting_heatmap, use_container_width=True)

    # 4. Seasonal Boundaries (Fours and Sixes)
    st.subheader("4. Seasonal Boundaries (Fours and Sixes)")
    boundaries = deliveries_with_season[deliveries_with_season['batsman_runs'].isin([4, 6])]
    boundary_stats = boundaries.groupby(['season', 'batsman_runs']).size().reset_index(name='count')

    # Improved: Combined both fours and sixes into a single chart for easy comparison
    boundary_chart = alt.Chart(boundary_stats).mark_bar().encode(
        x=alt.X('season:O', title="Season"),
        y=alt.Y('count:Q', title="Total Boundaries"),
        color=alt.Color('batsman_runs:N', scale=alt.Scale(scheme='set1'), title="Boundary Type"),
        tooltip=['season', 'batsman_runs', 'count']
    ).properties(width=800, height=400, title="Fours and Sixes by Season")

    st.altair_chart(boundary_chart, use_container_width=True)

    # 5. Top Performers by Season
    st.subheader("5. Top Performers by Season")

    # Improved: Added top 5 players for better focus
    top_batsmen_leaderboard = deliveries_with_season.groupby(['season', 'batter'])['batsman_runs'].sum().reset_index()
    top_batsmen_leaderboard = top_batsmen_leaderboard.groupby('season').apply(lambda x: x.nlargest(5, 'batsman_runs')).reset_index(drop=True)

    st.dataframe(top_batsmen_leaderboard)

        # 6. Strike Rate vs Economy Rate by Season
    st.subheader("6. Strike Rate vs Economy Rate (Batsmen vs Bowlers)")

    # Calculate strike rate for batsmen
    batter_strike_rate = deliveries_with_season.groupby(['season', 'batter']).apply(
        lambda x: (x['batsman_runs'].sum() / x.shape[0]) * 100
    ).reset_index(name='strike_rate')

    # Calculate economy rate for bowlers
    bowler_economy_rate = deliveries_with_season.groupby(['season', 'bowler']).apply(
        lambda x: x['total_runs'].sum() / (x['over'].nunique() or 1)
    ).reset_index(name='economy_rate')

    # Ensure 'economy_rate' is numeric
    bowler_economy_rate['economy_rate'] = pd.to_numeric(bowler_economy_rate['economy_rate'], errors='coerce')

    # Combine both batting and bowling statistics
    combined_stats = pd.merge(batter_strike_rate, bowler_economy_rate, on='season', how='inner')

    # Create scatter plot for Strike Rate vs Economy Rate
    scatter_chart = alt.Chart(combined_stats).mark_circle(size=80, opacity=0.7).encode(
        x=alt.X('strike_rate:Q', title="Strike Rate (Batsmen)", scale=alt.Scale(zero=False)),  # Explicitly defining it as quantitative
        y=alt.Y('economy_rate:Q', title="Economy Rate (Bowlers)", scale=alt.Scale(zero=False)),  # Explicitly defining it as quantitative
        color=alt.Color('season:N', legend=alt.Legend(title='Season')),  # Categorical color by season
        tooltip=['batter', 'strike_rate', 'economy_rate', 'season'],  # Enhanced tooltip to show batter and season
    ).properties(
        width=800,
        height=500,
        title="Strike Rate vs Economy Rate by Season"
    )

    # Add trend line to the scatter plot
    trend_line = scatter_chart.transform_regression(
        'strike_rate', 'economy_rate', method='linear'
    ).mark_line(color='red', size=2, opacity=0.6)

    # Combine the scatter plot with trend line without applying configuration to the combined chart
    final_chart = scatter_chart + trend_line

    # Apply chart configurations (title and axis styling)
    final_chart = final_chart.configure_title(
        fontSize=16, font='Arial', anchor='start', fontWeight='bold'
    ).configure_axis(
        labelFontSize=12, titleFontSize=14
    )

    # Show the final chart
    st.altair_chart(final_chart, use_container_width=True)


#Detailed match Analysis
elif page == "Detailed Match Data":
    st.title("Detailed Match Data")

    # Filter matches based on user-selected teams and seasons
    st.write("### Select Teams and Season for Match Details")
    selected_season = st.selectbox("Select Season", sorted(matches['season'].unique()), index=0, key="season_selectbox")
    teams = sorted(matches['team1'].unique())
    selected_team1 = st.selectbox("Select Team 1", teams, key="team1_selectbox")
    selected_team2 = st.selectbox("Select Team 2", [team for team in teams if team != selected_team1], key="team2_selectbox")

    # Filter matches for selected season and teams
    filtered_matches = matches[
        (matches['season'] == selected_season) &
        (((matches['team1'] == selected_team1) & (matches['team2'] == selected_team2)) |
         ((matches['team1'] == selected_team2) & (matches['team2'] == selected_team1)))
    ]

    if not filtered_matches.empty:
        # Select a specific match if multiple matches exist
        if len(filtered_matches) > 1:
            selected_match_date = st.selectbox("Select Match Date", filtered_matches['date'].dt.strftime('%Y-%m-%d'))
            filtered_match = filtered_matches[filtered_matches['date'] == pd.to_datetime(selected_match_date)].iloc[0]
        else:
            filtered_match = filtered_matches.iloc[0]

        match_id = filtered_match['id']
        st.write(f"### Match Details: {selected_team1} vs. {selected_team2} ({selected_season})")
        st.write(f"Venue: **{filtered_match['venue']}** | Date: **{filtered_match['date'].strftime('%Y-%m-%d')}**")

        # Filter deliveries for the selected match
        match_deliveries = deliveries[deliveries['match_id'] == match_id]

        # High-Level Match Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Runs", match_deliveries['total_runs'].sum())
        col2.metric("Wickets Taken", match_deliveries[match_deliveries['dismissal_kind'].notna()]['dismissal_kind'].count())
        col3.metric("Overs Bowled", match_deliveries['over'].nunique())
        col4.metric("Boundaries", match_deliveries[match_deliveries['batsman_runs'].isin([4, 6])].shape[0])

        # Runs Per Over Visualization
        st.write("### Runs Scored Per Over")
        runs_per_over = match_deliveries.groupby('over')['total_runs'].sum().reset_index()
        runs_chart = alt.Chart(runs_per_over).mark_line(point=True).encode(
            x=alt.X('over:O', title='Over'),
            y=alt.Y('total_runs:Q', title='Runs Scored'),
            tooltip=['over', 'total_runs']
        ).properties(width=700, height=400, title="Runs Scored Per Over")
        st.altair_chart(runs_chart, use_container_width=True)

        # Player-wise Performance
        st.write("### Player Performances")

        # Top Run Scorers
        st.write("#### Top Run Scorers")
        top_scorers = match_deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).reset_index()
        top_scorers_chart = alt.Chart(top_scorers.head(5)).mark_bar().encode(
            x=alt.X('batter:N', title='Batter'),
            y=alt.Y('batsman_runs:Q', title='Total Runs'),
            color=alt.Color('batsman_runs:Q', scale=alt.Scale(scheme='blues')),
            tooltip=['batter', 'batsman_runs']
        ).properties(width=700, height=400, title="Top 5 Run Scorers")
        st.altair_chart(top_scorers_chart, use_container_width=True)

        # Top Wicket Takers
        st.write("#### Top Wicket Takers")
        top_wickets = match_deliveries[match_deliveries['dismissal_kind'].notna()]
        top_wicket_takers = top_wickets.groupby('bowler')['dismissal_kind'].count().sort_values(ascending=False).reset_index()
        top_wickets_chart = alt.Chart(top_wicket_takers.head(5)).mark_bar().encode(
            x=alt.X('bowler:N', title='Bowler'),
            y=alt.Y('dismissal_kind:Q', title='Wickets Taken'),
            color=alt.Color('dismissal_kind:Q', scale=alt.Scale(scheme='reds')),
            tooltip=['bowler', 'dismissal_kind']
        ).properties(width=700, height=400, title="Top 5 Wicket Takers")
        st.altair_chart(top_wickets_chart, use_container_width=True)

        # Ball-by-Ball Breakdown
        st.write("### Ball-by-Ball Analysis")
        st.dataframe(match_deliveries[['over', 'ball', 'batter', 'bowler', 'batsman_runs', 'total_runs', 'dismissal_kind']])
    else:
        st.write("No match data available for the selected filters.")


# Venue Stats Page
elif page == "Venue Stats":
    st.title("Venue Performance")

    # Matches Played at Each Venue
    st.write("### Matches Played at Different Venues")
    matches_per_venue = filtered_matches['venue'].value_counts().reset_index()
    matches_per_venue.columns = ['Venue', 'Matches']
    venue_bar_chart = alt.Chart(matches_per_venue).mark_bar().encode(
        x=alt.X('Matches:Q', title='Number of Matches'),
        y=alt.Y('Venue:N', sort='-x', title='Venue'),
        tooltip=['Venue', 'Matches']
    ).properties(
        title="Matches Played per Venue",
        width=700,
        height=400
    )
    st.altair_chart(venue_bar_chart, use_container_width=True)

    # Average Runs Scored per Inning at Each Venue
    st.write("### Average Runs Scored per Inning at Each Venue")

    # Step 1: Calculate total runs per inning
    inning_scores = deliveries.groupby(['match_id', 'inning'])['total_runs'].sum().reset_index()

    # Step 2: Merge with matches to get venue information
    inning_scores = inning_scores.merge(matches[['id', 'venue']], left_on='match_id', right_on='id')

    # Step 3: Calculate average runs per inning per venue
    avg_runs_per_inning = inning_scores.groupby(['venue', 'inning'])['total_runs'].mean().reset_index()

    # Renaming columns for clarity
    avg_runs_per_inning.columns = ['Venue', 'Inning', 'Avg_Runs']

    # Plot the results using Altair
    avg_runs_chart = alt.Chart(avg_runs_per_inning).mark_bar().encode(
        x=alt.X('Avg_Runs:Q', title='Average Runs'),
        y=alt.Y('Venue:N', sort='-x', title='Venue'),
        color=alt.Color('Inning:N', scale=alt.Scale(scheme='category10'), title='Inning'),
        tooltip=['Venue', 'Inning', 'Avg_Runs']
    ).properties(
        title="Average Runs Scored per Inning at Each Venue",
        width=800,
        height=400
    )

    st.altair_chart(avg_runs_chart, use_container_width=True)



    # Win Percentages by Venue
    st.write("### Win Percentage by Venue")
    venue_wins = filtered_matches.groupby('venue')['winner'].value_counts(normalize=True).unstack(fill_value=0).reset_index()
    venue_win_chart = alt.Chart(venue_wins.melt('venue', var_name='Team', value_name='Win_Percentage')).mark_bar().encode(
        x=alt.X('Win_Percentage:Q', title='Win Percentage', axis=alt.Axis(format='%')),
        y=alt.Y('venue:N', sort='-x', title='Venue'),
        color=alt.Color('Team:N', legend=alt.Legend(title="Teams")),
        tooltip=['venue', 'Team', 'Win_Percentage']
    ).properties(
        title="Team Win Percentage per Venue",
        width=700,
        height=400
    )
    st.altair_chart(venue_win_chart, use_container_width=True)

        # Boundary Analysis
    st.write("### Boundary Analysis at Venues")
    boundaries = filtered_deliveries[filtered_deliveries['batsman_runs'].isin([4, 6])]

    # Merge deliveries with matches to include venue information
    boundaries = boundaries.merge(filtered_matches[['id', 'venue']], left_on='match_id', right_on='id', how='left')

    # Group by venue and boundary type (fours or sixes) to count the number of boundaries
    boundary_counts = boundaries.groupby(['venue', 'batsman_runs']).size().unstack(fill_value=0).reset_index()
    boundary_counts.columns = ['Venue', 'Fours', 'Sixes']

    # Melt the DataFrame for easier plotting
    boundary_chart_data = boundary_counts.melt('Venue', var_name='Boundary_Type', value_name='Count')

    # Create the chart
    boundary_chart = alt.Chart(boundary_chart_data).mark_bar().encode(
        x=alt.X('Count:Q', title='Count of Boundaries'),
        y=alt.Y('Venue:N', sort='-x', title='Venue'),
        color=alt.Color('Boundary_Type:N', legend=alt.Legend(title="Boundary Type")),
        tooltip=['Venue', 'Boundary_Type', 'Count']
    ).properties(
        title="Boundary Analysis per Venue",
        width=700,
        height=400
    )

    # Display the chart in Streamlit
    st.altair_chart(boundary_chart, use_container_width=True)
# Matches Played Over Seasons at Each Venue
    st.write("### Matches Played Over Seasons at Each Venue")
    venue_season_trend = filtered_matches.groupby(['venue', 'season']).size().reset_index(name='Matches')

    # Create the stacked bar chart
    season_trend_chart = alt.Chart(venue_season_trend).mark_bar().encode(
        x=alt.X('season:O', title='Season'),
        y=alt.Y('Matches:Q', title='Number of Matches'),
        color=alt.Color('venue:N', legend=alt.Legend(title="Venue")),
        tooltip=['venue', 'season', 'Matches']
    ).properties(
        title="Matches Played Over Seasons at Each Venue",
        width=700,
        height=400
    )

    # Display the chart in Streamlit
    st.altair_chart(season_trend_chart, use_container_width=True)


    st.write("Explore the venue stats further using the filters on the sidebar to refine the analysis.")

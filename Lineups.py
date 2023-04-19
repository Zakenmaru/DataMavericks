# Required imports
import pandas as pd
import streamlit as st
import json
from pathlib import Path
import requests

mavs_pbp_season = pd.read_parquet(str(Path.cwd()) + "/data/mavs_pbp_season.parquet")
all_players_data = pd.read_parquet(str(Path.cwd()) + "/data/player_data.parquet")

mavs_players_names = all_players_data[all_players_data['team'] == 'DAL']

teams_json = json.loads(requests.get('https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)
all_teams = {}
for team in teams_json:
    all_teams[team['teamName']] = team['teamId']
del all_teams['Dallas Mavericks']

lineups = pd.read_parquet(str(Path.cwd()) + "/data/lineups.parquet")

# Get the position of a given player
def get_position(player_name):
    positions = all_players_data[all_players_data['name'] == player_name].reset_index()
    unique_pos = list(positions['startPos'].unique())
    counts = {}
    for pos in unique_pos:
        counts[pos] = len(all_players_data[all_players_data['startPos'] == pos])
    
    if "" in counts:
        del counts[""]
    max_count = 0
    max_pos = ""
    for pos in counts:
        if max_count < counts[pos]:
            max_count = counts[pos]
            max_pos = pos
    
    return max_pos

def get_team_id(team_name):
    return all_teams[team_name]

def get_team_abbrev(team_id):
    all_player_data = all_players_data[all_players_data['nbaTeamId'] == str(team_id)].reset_index()
    return all_player_data.at[0, 'team']

# Define function for the first tab
def Lineups():
    st.header("Lineups")

    teams = list(all_teams.keys())
    selected_team = st.selectbox("Select an opponent to create possible roster against", teams, index=0)
    st.markdown("Optimal lineups against: **{0}**".format(selected_team))
    st.caption("_Select a column header to sort by increasing/decreasing order_")

    team_abbrev = get_team_abbrev(int(get_team_id(selected_team)))

    team_lineups = lineups[lineups['team'] == team_abbrev].reset_index()
    #team_lineups.drop_duplicates(inplace=True)
    #st.dataframe(team_lineups)
    filtered_lineups = pd.DataFrame(columns=['C', 'PF', 'SG', 'PG', 'SF', 'Play Type', 'Offense Strength', 'Defense Strength'])
    for i in range(len(team_lineups.index)):
        lineup = team_lineups.at[i,'lineup']
        lineup_pos = {'C': [], 'PF': [], 'SG': [], 'PG': [], 'SF': []}
        for player in lineup:
            lineup_pos[get_position(player)].append(player)
        check = True
        updated_lineup = {}
        for pos in lineup_pos:
            if len(lineup_pos[pos]) == 0:
                check = False
        
        if check:
            for pos in lineup_pos:
                if len(lineup_pos[pos]) == 1:
                    updated_lineup[pos] = lineup_pos[pos][0]
                elif "Luka Doncic" in lineup_pos[pos]:
                    updated_lineup[pos] = "Luka Doncic"
                elif "Kyrie Irving" in lineup_pos[pos]:
                    updated_lineup[pos] = "Kyrie Irving"
                else:
                    updated_lineup[pos] = lineup_pos[pos][0]
            new_lineup = [updated_lineup['C'], updated_lineup['PF'], updated_lineup['SG'], updated_lineup['PG'], updated_lineup['SF']]
            new_lineup.append(team_lineups.at[i,'play_type'])
            new_lineup.append(team_lineups.at[i,'offense_strength'])
            new_lineup.append(team_lineups.at[i,'defense_strength'])
            
            filtered_lineups.loc[len(filtered_lineups.index)] = new_lineup
    
    filtered_lineups.drop_duplicates(inplace=True)
    filtered_lineups.set_index('Play Type', inplace=True)
    st.dataframe(filtered_lineups)

    # Metric information
    play_col, offense_col, defense_col = st.columns(3)

    if len(filtered_lineups.index) > 0:
        play_col.metric(":green[**Average Play Type**]", list(filtered_lineups.index)[0])
    offense_col.metric(":green[**Average Offensive Strength**]", "{:.3f}".format(filtered_lineups['Offense Strength'].mean()))
    defense_col.metric(":green[**Average Defensive Strength**]", "{:.3f}".format(filtered_lineups['Defense Strength'].mean()))

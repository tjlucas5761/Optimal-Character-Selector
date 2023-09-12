import os.path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#dataframe rows = fighting as
#dataframe columns = fighting against

def main():
    data_folder_path = os.path.dirname(__file__) + "\\character_data"
    #Initialize DataFrames if eliminations.csv already exists
    if os.path.isfile(data_folder_path + "\\eliminations.csv"):
        print("Welcome back!")
        eliminations_df, deaths_df, ratios_df, matches_df, characters = initialize_dataframes(data_folder_path)
    #Create dataframes, folder, and files if eliminations.csv does not exist.
    else:
        print("Creating new folder and files!")
        characters = ["Black Prior","Centurion","Conqueror","Gladiator","Gryphon","Lawbringer","Peacekeeper","Warden","Warmonger"]
        template_df = pd.DataFrame(index = characters, columns = characters)
        template_df.fillna(0, inplace = True)
        os.makedirs(data_folder_path)
        save_dfs_to_csv(template_df, template_df, template_df, template_df, data_folder_path)
        eliminations_df, deaths_df, ratios_df, matches_df, characters = initialize_dataframes(data_folder_path)
     
    while True:        
        user_input = input("What would you like to do?: Ratios vs Opponent, Ratios to Matches vs Opponent, Update Stats, Void and Exit, or Save and Exit\n")
        if user_input == "Ratios vs Opponent":
            create_opponent_ratios_bar_chart(characters, ratios_df)
        elif user_input == "Ratios to Matches vs Opponent":
            create_opponent_ratios_to_matches_scatter_plot(characters,ratios_df, matches_df)
        elif user_input == "Update Stats":
            update_current_dataframes(characters, eliminations_df, deaths_df, ratios_df, matches_df)
        #Incase the user inputs a wrong number, the updated dataframes will not be saved
        elif user_input == "Void and Exit":
            print("Updated stats voided!")
            break
        elif user_input == "Save and Exit":
            save_dfs_to_csv(eliminations_df, deaths_df, ratios_df, matches_df, data_folder_path)
            print("Changes have been saved!")
            break
        else:
            print("Invalid Input!")


def save_dfs_to_csv(eliminations_df, deaths_df, ratios_df, matches_df, data_folder_path):
    eliminations_df.to_csv(data_folder_path + "\\eliminations.csv", index = False)
    deaths_df.to_csv(data_folder_path + "\\deaths.csv", index = False)
    ratios_df.to_csv(data_folder_path + "\\ratios.csv", index = False)
    matches_df.to_csv(data_folder_path + "\\matches.csv", index = False)


def initialize_dataframes(data_folder_path):
    eliminations_df = pd.read_csv(data_folder_path + "\\eliminations.csv")
    deaths_df = pd.read_csv(data_folder_path + "\\deaths.csv")
    ratios_df = pd.read_csv(data_folder_path + "\\ratios.csv")
    matches_df = pd.read_csv(data_folder_path + "\\matches.csv")
    characters = list(eliminations_df.columns)
    eliminations_df.index = characters
    deaths_df.index = characters
    ratios_df.index = characters
    matches_df.index = characters
    return eliminations_df, deaths_df, ratios_df, matches_df, characters

  
def check_if_character_is_valid(character_list, character_name):
    while True:
        if character_name not in character_list:
            character_name = input("Invalid Character name!" "\n" "Please choose from: " + ", ".join(character_list) + "\n")
        else:
            return character_name


def create_opponent_ratios_bar_chart(character_list, ratios_df):
    opponent = input("Who are you fighting against?: ")
    opponent = check_if_character_is_valid(character_list, opponent)
    opponent_ratios_df = ratios_df.sort_values(opponent, ascending=False)
    opponent_ratios_bar_chart = opponent_ratios_df[opponent].plot(
        kind="bar",
        title="Opponent: " + opponent)
    opponent_ratios_bar_chart.set_xlabel("character_options")
    opponent_ratios_bar_chart.set_ylabel("eliminations_to_deaths_ratio")
    plt.xticks(rotation=45)
    plt.show()


def create_opponent_ratios_to_matches_scatter_plot(character_list, ratios_df, matches_df):
    opponent = input("Who are you fighting against?: ")
    opponent = check_if_character_is_valid(character_list, opponent)
    opponent_ratios_matches_df = pd.concat([ratios_df[opponent], matches_df[opponent]], axis = 1)
    opponent_ratios_matches_df.columns = ["eliminations_to_death_ratio", "number_of_matches"]
    sns.scatterplot(
        data=opponent_ratios_matches_df,
        x=opponent_ratios_matches_df.loc[:, "number_of_matches"],
        y=opponent_ratios_matches_df.loc[:, "eliminations_to_death_ratio"],
        s=200,
        hue=character_list)
    plt.title("Against: " + opponent)
    plt.legend(
        title="Characters",
        loc="center left",
        bbox_to_anchor=(1, 0.5))
    plt.grid()
    plt.show()


def update_current_dataframes(character_list, eliminations_df, deaths_df, ratios_df, matches_df):
    current_character = input("Who are you playing as?: ")
    current_character = check_if_character_is_valid(character_list, current_character)
    opponent = input("Who are you fighting against?: ")
    opponent = check_if_character_is_valid(character_list, opponent)
    while True:
        try:
            incoming_eliminations = int(input("How Many Eliminations?: "))
            incoming_deaths = int(input("How Many Deaths?: "))
        except:
            print("Non integer input: Enter an integer!")
        else:
            #determine if the outcome of the match is possible
            if (incoming_eliminations <= 3) and (incoming_eliminations >= 0) and (incoming_deaths <= 3) and (incoming_deaths >= 0):
                if (incoming_eliminations == 3 and incoming_eliminations != incoming_deaths) or (incoming_deaths == 3 and incoming_eliminations != incoming_deaths):
                    break
                else:
                    print("Impossible outcome: Either eliminations or deaths must equal 3, but not both!")
            else:
                print("Impossible outcome: Eliminations or Deaths are out of range!")
                
    total_eliminations = eliminations_df.loc[current_character, opponent] = eliminations_df.loc[current_character, opponent] + incoming_eliminations
    total_deaths = deaths_df.loc[current_character, opponent] = deaths_df.loc[current_character, opponent] + incoming_deaths
    if total_deaths == 0:
        #Cannot divide by zero, essentially (3-0) == (3-1). However, no death is added to the deaths dataframe so that the ratio will be correct when the player eventually dies.
        ratios_df.loc[current_character, opponent] = total_eliminations
    else:
        ratios_df.loc[current_character, opponent] = round(total_eliminations / total_deaths, 2)
        
    matches_df.loc[current_character, opponent] = matches_df.loc[current_character, opponent] + 1
    print("Stats updated!")


if __name__ == "__main__":
    main()
import requests
import random, time
import datetime

server_url = 'http://127.0.0.1:5000/'

# -----------------------------INTRODUCTION------

print("Welcome to the D&D Character builder. You will be guided through a serious of prompts to come up with your character")
print(f"You will choose a race (such as human or halfling) and a class (such as fighter or wizard).\n")
print("You will also have the option to randomly generate each step of your character but are encouraged to go through each step and use the help feature to learn more information") #1
input(f"Hit enter when you're ready to begin\n\n")


#--------------------------------------------RACE--------------------------------------
# Function to fetch class information from microservice
def get_race_info(race_name):
    data = {'race': race_name}
    response = requests.post(server_url+'get_race_info', json=data)
    return response.json()

# Function to format race description
def format_race_description(data):
    description = f"Race: {data['name']}\n"
    description += f"Alignment: {data['alignment']}\n"
    description += f"Age: {data['age']}\n"
    description += f"Size: {data['size']} - {data['size_description']}\n"
    description += f"Languages: {data['language_desc']}\n"
    return description


# Gets all races
races = requests.post(server_url+'get_races', json={})
races = races.json()
races = [item["index"] for item in races["results"]]

race_choice = ""



# Interaction with user to determine a race
print("-------------------------------------------------------------------------")
print("We will start off by having you select a race for your character")
print(f"Your choice of race affects many different aspects of your character. It establishes fundamental qualities that exist throughout your character's adventuring career.\n")
print("Race options: ", ", ".join(races))
print("")

while True:
    user_input = input("Type your choice or hit enter for a random selection. You can also type HELP for more info\n") #7

    if user_input == "":
        while True:
            # Pick a random race
            race_choice = random.choice(races)
            print(f"Randomly selected race: {race_choice}")
            user_input = input("Keep this race? (yes/no): ") #4
            if user_input.lower() in ["yes", "y"]: #QUALITY ATTRIBUTE: USABILITY
                break
        break
    elif user_input.lower() == 'help': #3
        race_name = input("Enter the race name for more information: ")
        if race_name in races:
            try:
                race_info = get_race_info(race_name)
                print(format_race_description(race_info))
            except Exception as e:
                print(f"Error fetching race info: {e}")
        else:
            print("Race not found.")
        continue  # Add this line to return to the main loop
    elif user_input in races:
        race_choice = user_input
        print(f"You have chosen {race_choice}")
        break
    else:
        print("Wrong input. Choose from:\n", ", ".join(races))
 

# -----------------------------------CLASSES-------------------------------------
# Fetch class information from microservice
def get_class_info(class_name):
    #TODO change to hardcoded
    data = {'class': class_name}
    response = requests.post(server_url+'get_class_info', json=data)
    return response.json()

# Gets all classes
classes = requests.post(server_url+'get_classes', json={})
classes = classes.json()
classes = [item["index"] for item in classes["results"]]

class_choice = ""


# Interaction with user to determine class
print(f"\n\n-----------------------------------------------------------")
print("In the next step, choose a class for your character.")
print(f"Every adventurer is a member of a class. Class broadly describes a character's vocation, what special talents he or she possesses, and the tactics he or she is most likely to employ when exploring a dungeon, fighting monsters, or engaging in a tense negotiation\n")
print("Class options: ", ", ".join(classes))

while True:
    user_input = input(f"\nWhat Class do you want? Type one of the choices above, hit enter for random, or 'help' for more info\n")

    if user_input == "":
        # Pick a random class
        while True:
            class_choice = random.choice(classes)
            print(f"Randomly selected class: {class_choice}")
            user_input = input("Keep this class? (yes/no): ") #5
            if user_input.lower() in ["yes", "y"]:
                break
        break
    elif user_input in classes:
        class_choice = user_input
        print(f"You have chosen {class_choice}")
        break
    else:
        print("Wrong input. Choose from:\n", ", ".join(classes))

#-------------------------PROFICIENCES--------
proficiency_choice = []
    
# choose proficiencies
print(f"\n\n-----------------------------------------------------------")
print("In the next step, you will choose your characters proficiencies")
print("Proficiencies represent skills your character will excel at in the game. You get a bonus added to skill checks, saving throws, or attacks for skills that a character is proficient in") #TODO
print("")

class_data = get_class_info(class_choice)

for proficiency_choice in class_data['proficiency_choices']:
    options = [option['item']['name'] for option in proficiency_choice['from']['options']]
    selected_proficiencies = []

    print(f"Choose {proficiency_choice['choose']} from the following options:")
    print("Type the proficiency or the number corresponding to it to save time :)") #2
    while proficiency_choice['choose'] > 0:
        print("Proficiences:")
        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        if proficiency_choice['choose'] == 1:
            user_input = input("Enter your choice: ")
        else:
            user_input = input(f"Enter your choice ({proficiency_choice['choose']} left): ")

        if user_input.isdigit():
            index = int(user_input) - 1
            if 0 <= index < len(options):
                selected_proficiencies.append(options[index])
                options.pop(index)
                proficiency_choice['choose'] -= 1
            else:
                print("Invalid choice. Please select a valid option.")
        else:
            print("Invalid input. Please enter the number corresponding to your choice.")

    proficiency_choice = selected_proficiencies

    print(f"\nYou have selected the following proficiencies:")
    for selected_proficiency in selected_proficiencies:
        print(f"- {selected_proficiency}")



#-------------Roll for skills-----------
#roll skills
# Write a python method for calculating ability scores in D&D. Roll your stats by rolling 4 x 6-sided dice, dropping the lowest number, and adding the remaining total. Do this for all of the keys in the ability dictionary (ability = {"Strength" : 0, "Dexterity" : 0, "Constitution" : 0, "Intellect" : 0,  "Wisdom" : 0}) and update this dictionary accordingly. prompt the user for inputs and display all the stats at the end
print(f"\n\n-----------------------------------------------------------")
print("Lastly you will be rolling to determine your character's base stats which include Strength, Dexterity, Constitution, Intellect, and Wisdom")
print("You'll roll 4 x 6-sided dice, dropping the lowest number")
ability = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intellect": 0, "Wisdom": 0}

def roll_ability_scores():

    for key in ability:
        input(f"Press Enter to roll for {key}: ") #6
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.sort()
        total = sum(rolls[1:])  # Drop the lowest roll and sum the remaining
        ability[key] = total

        time.sleep(.5)
        print(f"Rolls for {key}: {rolls}")
        time.sleep(.5)
        print(f"Final {key} score: {total}\n")

    print("Ability Scores:")
    for key, value in ability.items():
        print(f"{key}: {value}")

# Call the function to roll ability scores
roll_ability_scores() # QUALITY ATTRIBUTE: TESTABILITY


#----------------------------Ending dialogue-----------------------
print("---------------------------------------------------------")
print("Congrats! You have created your character:")
print("RACE: ", race_choice)
print("CLASS: ", class_choice)
print("PROFICIENCES: ")
for selected_proficiency in selected_proficiencies:
        print(f"- {selected_proficiency}")
print("STATS: ")
for key, value in ability.items():
        print(f"{key}: {value}")



#-------- QUALITY ATTRIBUTE: PERFORMANCE EFFICIENCY
start_time = datetime.datetime.now()
# insert code snippet here
end_time = datetime.datetime.now()
print(end_time - start_time)
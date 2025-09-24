import requests
import random, time
import datetime

server_url = 'http://127.0.0.1:5000/'

# -----------------------------INTRODUCTION------
def print_header():
    print("=" * 80)
    print("""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║                            _____             _____                           ║
    ║                           |  __ \    ___    |  __ \                          ║
    ║                           | |  | |  ( _ )   | |  | |                         ║
    ║                           | |  | |  / _ \/\ | |  | |                         ║
    ║                           | |__| | | (_>  < | |__| |                         ║
    ║                           |_____/   \___/\/ |_____/                          ║
    ║                                                                              ║
    ║                              CHARACTER GENERATOR 🎲                          ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    print("=" * 80)

def print_section_header(title, emoji=""):
    print(f"\n{'=' * 80}")
    print(f"  {emoji} {title.upper()} {emoji}")
    print('=' * 80)

def print_step(step_num, title, description=""):
    print(f"\n STEP {step_num}: {title}")
    if description:
        print(f"   {description}")
    print("-" * 60)

print_header()
print("Welcome to the D&D Character builder! You will be guided through a series of")
print("prompts to create your character. You'll choose a race (such as human or")
print("halfling) and a class (such as fighter or wizard).")
print("\nYou can also randomly generate each step or use the help feature to learn")
print("more about your options!")
print("\n" + "=" * 80)
input("🎯 Press ENTER when you're ready to begin your adventure...\n")


#--------------------------------------------RACE--------------------------------------
# Function to fetch class information from microservice
def get_race_info(race_name):
    data = {'race': race_name}
    response = requests.post(server_url+'get_race_info', json=data)
    return response.json()

# Function to format race description
def format_race_description(data):
    print(f"\n{'─' * 60}")
    print(f"🏷️  RACE: {data['name'].upper()}")
    print(f"⚖️  ALIGNMENT: {data['alignment']}")
    print(f" AGE: {data['age']}")
    print(f"📏 SIZE: {data['size']} - {data['size_description']}")
    print(f"️  LANGUAGES: {data['language_desc']}")
    print(f"{'─' * 60}")

# Gets all races
races = requests.post(server_url+'get_races', json={})
races = races.json()
races = [item["index"] for item in races["results"]]

race_choice = ""

# Interaction with user to determine a race
print_section_header("RACE SELECTION", "🎲")
print_step(1, "Choose Your Character's Race", 
          "Your race affects many aspects of your character - abilities, traits, and roleplay opportunities!")

print(f"\n�� Available Races:")
print("─" * 40)
for i, race in enumerate(races, 1):
    print(f"  {i:2d}. {race.title()}")
print("─" * 40)

while True:
    print(f"\n💭 What would you like to do?")
    print("   • Type a race name to select it")
    print("   • Type a number (1-{}) for quick selection".format(len(races)))
    print("   • Press ENTER for random selection")
    print("   • Type 'help' for detailed race information")
    
    user_input = input(f"\n🎲 Your choice: ").strip()

    if user_input == "":
        while True:
            # Pick a random race
            race_choice = random.choice(races)
            print(f"\n🎲 Randomly selected race: {race_choice.title()}")
            user_input = input("✅ Keep this race? (yes/no): ")
            if user_input.lower() in ["yes", "y"]:
                break
        break
    elif user_input.lower() == 'help':
        race_name = input("🎲 Enter the race name for more information: ").strip()
        if race_name in races:
            try:
                race_info = get_race_info(race_name)
                format_race_description(race_info)
            except Exception as e:
                print(f"❌ Error fetching race info: {e}")
        else:
            print("❌ Race not found. Please check the spelling.")
        continue
    elif user_input.isdigit() and 1 <= int(user_input) <= len(races):
        race_choice = races[int(user_input) - 1]
        print(f"✅ You have chosen: {race_choice.title()}")
        break
    elif user_input in races:
        race_choice = user_input
        print(f"✅ You have chosen: {race_choice.title()}")
        break
    else:
        print("❌ Invalid input. Please choose from the available options above.")

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
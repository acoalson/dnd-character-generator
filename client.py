"""
Interactive CLI for building a D&D 5e character.
Flow: header → race selection → class selection → proficiencies → ability rolls → summary.
External dependency: talks to a local Flask microservice in server.py for races/classes data.
"""
import requests
import random, time
import datetime

server_url = 'http://127.0.0.1:5000/'
RACES_SERVICE_URL = 'http://127.0.0.1:5001/'
CLASSES_SERVICE_URL = 'http://127.0.0.1:5002/'

# -----------------------------INTRODUCTION------
def print_header():
    """Print the branded ASCII banner and intro separators."""
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
    """Print a visual section divider with a title and optional emoji."""
    print(f"\n{'=' * 80}")
    print(f"  {emoji} {title.upper()} {emoji}")
    print('=' * 80)

def print_step(step_num, title, description=""):
    """Print a step header with optional one-line description."""
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
    """POST to races service to fetch details for a given race.
    Request: { 'race': <race_index> }
    Returns: upstream JSON dict on success; may raise/return invalid JSON if service fails.
    """
    data = {'race': race_name}
    response = requests.post(RACES_SERVICE_URL+'get_race_info', json=data)
    return response.json()

# Function to format race description
def format_race_description(data):
    """Pretty-print race details. Expects keys: name, alignment, age, size, size_description, language_desc."""
    print(f"\n{'─' * 60}")
    print(f"🏷️  RACE: {data['name'].upper()}")
    print(f"⚖️  ALIGNMENT: {data['alignment']}")
    print(f" AGE: {data['age']}")
    print(f"📏 SIZE: {data['size']} - {data['size_description']}")
    print(f"️  LANGUAGES: {data['language_desc']}")
    print(f"{'─' * 60}")

# Gets all races
races = requests.post(RACES_SERVICE_URL+'get_races', json={})
races = races.json()
races = [item["index"] for item in races["results"]]

race_choice = ""

# Interaction with user to determine a race
print_section_header("RACE SELECTION", "🎲")
print_step(1, "Choose Your Character's Race", 
          "Your race affects many aspects of your character - abilities, traits, and roleplay opportunities!")

print(f"\nAvailable Races:")
print("─" * 40)
for i, race in enumerate(races, 1):
    print(f"  {i:2d}. {race.title()}")
print("─" * 40)

# Accepted inputs: name, number (1-N), ENTER for random, 'help' to view details for a race
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
    """POST to classes service to fetch details for a given class.
    Request: { 'class': <class_index> }
    Returns: upstream JSON dict on success; may raise/return invalid JSON if service fails.
    """
    #TODO change to hardcoded
    data = {'class': class_name}
    response = requests.post(CLASSES_SERVICE_URL+'get_class_info', json=data)
    return response.json()

# Enhanced formatter for class information
def format_class_description(data):
    """Pretty-print class details. Expects keys: name, hit_die, saving_throws, proficiencies, subclasses."""
    try:
        print(f"\n{'─' * 60}")
        print(f"🛡️  CLASS: {data.get('name', 'Unknown').upper()}")
        if 'hit_die' in data:
            print(f"🎲 HIT DIE: d{data['hit_die']}")
        # Saving throws
        if 'saving_throws' in data and data['saving_throws']:
            saving = ", ".join(st.get('name', 'Unknown') for st in data['saving_throws'])
            print(f"💪 SAVING THROWS: {saving}")
        # Core proficiencies
        if 'proficiencies' in data and data['proficiencies']:
            profs = ", ".join(p.get('name', 'Unknown') for p in data['proficiencies'][:8])
            print(f"📜 PROFICIENCIES: {profs}{' …' if len(data['proficiencies']) > 8 else ''}")
        # Subclasses (if any)
        if 'subclasses' in data and data['subclasses']:
            subclasses = ", ".join(sc.get('name', 'Unknown') for sc in data['subclasses'])
            print(f"🏷️  SUBCLASSES: {subclasses}")
        print(f"{'─' * 60}")
    except Exception as _:
        print("❌ Unable to format class details.")

# Gets all classes
classes = requests.post(CLASSES_SERVICE_URL+'get_classes', json={})
classes = classes.json()
classes = [item["index"] for item in classes["results"]]

class_choice = ""


# Interaction with user to determine class
print_section_header("CLASS SELECTION", "🧭")
print_step(2, "Choose Your Character's Class",
          "Your class defines your vocation, combat style, and special talents.")

print(f"\nAvailable Classes:")
print("─" * 40)
for i, class_name in enumerate(classes, 1):
    print(f"  {i:2d}. {class_name.title()}")
print("─" * 40)

# Accepted inputs: name, number (1-N), ENTER for random, 'help' to view details for a class
while True:
    print(f"\n💭 What would you like to do?")
    print("   • Type a class name to select it")
    print("   • Type a number (1-{}) for quick selection".format(len(classes)))
    print("   • Press ENTER for random selection")
    print("   • Type 'help' for detailed class information")

    user_input = input(f"\n⚔️  Your choice: ").strip()

    if user_input == "":
        while True:
            class_choice = random.choice(classes)
            print(f"\n🎲 Randomly selected class: {class_choice.title()}")
            user_input = input("✅ Keep this class? (yes/no): ")
            if user_input.lower() in ["yes", "y"]:
                break
        break
    elif user_input.lower() == 'help':
        class_name = input("⚔️  Enter the class name for more information: ").strip()
        if class_name in classes:
            try:
                class_info = get_class_info(class_name)
                format_class_description(class_info)
            except Exception as e:
                print(f"❌ Error fetching class info: {e}")
        else:
            print("❌ Class not found. Please check the spelling.")
        continue
    elif user_input.isdigit() and 1 <= int(user_input) <= len(classes):
        class_choice = classes[int(user_input) - 1]
        print(f"✅ You have chosen: {class_choice.title()}")
        break
    elif user_input in classes:
        class_choice = user_input
        print(f"✅ You have chosen: {class_choice.title()}")
        break
    else:
        print("❌ Invalid input. Please choose from the available options above.")

#-------------------------PROFICIENCES--------
proficiency_choice = []
    
# choose proficiencies
print_section_header("PROFICIENCIES", "📜")
print_step(3, "Choose Your Proficiencies",
          "Proficiencies represent skills your character excels at. They grant bonuses to checks, saves, or attacks where applicable.")

class_data = get_class_info(class_choice)

for proficiency_choice in class_data['proficiency_choices']:
    options = [option['item']['name'] for option in proficiency_choice['from']['options']]
    selected_proficiencies = []

    total_to_choose = proficiency_choice['choose']
    print(f"\nYou may choose {total_to_choose} from the following options:")
    print("─" * 60)
    for i, option in enumerate(options):
        print(f"  {i + 1:2d}. {option}")
    print("─" * 60)

    while len(selected_proficiencies) < total_to_choose:
        remaining = total_to_choose - len(selected_proficiencies)
        prompt = "Select by number or name (comma-separated), 'rand' to auto-fill, 'ls' to show list"
        user_input = input(f"➡️  {prompt} — {remaining} left: ").strip()

        if user_input.lower() == 'ls':
            print("─" * 60)
            for i, option in enumerate(options):
                print(f"  {i + 1:2d}. {option}")
            print("─" * 60)
            continue

        if user_input.lower() == 'rand':
            import random as _random
            fill_count = min(remaining, len(options))
            random_picks = [_random.choice(options) for _ in range(fill_count)]
            # Deduplicate random picks if options < remaining
            unique_random_picks = []
            for rp in random_picks:
                if rp in options and rp not in unique_random_picks:
                    unique_random_picks.append(rp)
            for rp in unique_random_picks:
                options.remove(rp)
                selected_proficiencies.append(rp)
                print(f"✅ Added: {rp}")
            continue

        # Parse comma-separated selections from numbers and/or names; dedupe per round
        tokens = [t.strip() for t in user_input.split(',') if t.strip()]
        if not tokens:
            print("❌ No input detected. Please enter numbers, names, 'rand', or 'ls'.")
            continue

        additions_this_round = []
        for token in tokens:
            if len(selected_proficiencies) + len(additions_this_round) >= total_to_choose:
                break
            if token.isdigit():
                idx = int(token) - 1
                if 0 <= idx < len(options):
                    choice_name = options[idx]
                    if choice_name not in additions_this_round:
                        additions_this_round.append(choice_name)
                else:
                    print(f"❌ {token} is out of range.")
            else:
                # name match (case-insensitive)
                matches = [opt for opt in options if opt.lower() == token.lower()]
                if matches:
                    choice_name = matches[0]
                    if choice_name not in additions_this_round:
                        additions_this_round.append(choice_name)
                else:
                    print(f"❌ '{token}' not found in available options. Type 'ls' to list.")

        if not additions_this_round:
            continue

        # Apply additions and confirm to user
        for chosen in additions_this_round:
            if chosen in options and len(selected_proficiencies) < total_to_choose:
                options.remove(chosen)
                selected_proficiencies.append(chosen)
                print(f"✅ Added: {chosen}")

    proficiency_choice = selected_proficiencies

    print(f"\n🎯 You selected:")
    for selected_proficiency in selected_proficiencies:
        print(f"  • {selected_proficiency}")
    print("─" * 60)


#-------------Roll for skills-----------
#roll skills
# Write a python method for calculating ability scores in D&D. Roll your stats by rolling 4 x 6-sided dice, dropping the lowest number, and adding the remaining total. Do this for all of the keys in the ability dictionary (ability = {"Strength" : 0, "Dexterity" : 0, "Constitution" : 0, "Intellect" : 0,  "Wisdom" : 0}) and update this dictionary accordingly. prompt the user for inputs and display all the stats at the end
print_section_header("ABILITY SCORES", "🎯")
print_step(4, "Roll Your Ability Scores",
          "You'll roll 4d6, drop the lowest, and sum the rest for each ability.")
ability = {"Strength": 0, "Dexterity": 0, "Constitution": 0, "Intellect": 0, "Wisdom": 0}


def roll_ability_scores():
    """Roll 4d6 per ability, drop the lowest die, sum remaining, and mutate the global ability dict."""

    for key in ability:
        input(f"Press Enter to roll for {key}: ")
        rolls = [random.randint(1, 6) for _ in range(4)]
        rolls.sort()
        total = sum(rolls[1:])
        ability[key] = total

        time.sleep(.5)
        print("─" * 40)
        print(f"🎲 Rolls for {key}: {rolls}  → drop {rolls[0]}")
        time.sleep(.3)
        print(f"✅ {key} score: {total}\n")

    print("─" * 40)
    print("Ability Scores:")
    for key, value in ability.items():
        print(f"  {key:<12} {value}")
    print("─" * 40)

# Call the function to roll ability scores
roll_ability_scores() # QUALITY ATTRIBUTE: TESTABILITY


#----------------------------Ending dialogue-----------------------
print_section_header("CHARACTER SUMMARY", "🏰")
print("Here is your adventurer:")
print("─" * 40)
print(f"RACE:  {race_choice.title()}")
print(f"CLASS: {class_choice.title()}")
print("PROFICIENCIES:")
for selected_proficiency in selected_proficiencies:
        print(f"  • {selected_proficiency}")
print("STATS:")
for key, value in ability.items():
        print(f"  {key:<12} {value}")
print("─" * 40)


#-------- QUALITY ATTRIBUTE: PERFORMANCE EFFICIENCY
start_time = datetime.datetime.now()
# insert code snippet here
end_time = datetime.datetime.now()
print(end_time - start_time)
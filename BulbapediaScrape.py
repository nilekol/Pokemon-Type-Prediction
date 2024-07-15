from bs4 import BeautifulSoup
import csv
import requests
import re
import pandas as pd
import string
import numpy as np
import urllib.parse
import string

pokemon_list = []

columns = [
    'name', 'abilities', 'type1', 'type2', 'is_legendary', 'japanese_name', 
    'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 
    'base_total', 'classification', 'generation', 'base_egg_steps', 
    'height_m', 'weight_kg', 'base_happiness', 'capture_rate', 
    'experience_growth', 'percentage_male', 'pokedex_number', 'against_bug', 
    'against_dark', 'against_dragon', 'against_electric', 'against_fairy', 
    'against_fight', 'against_fire', 'against_flying', 'against_ghost', 
    'against_grass', 'against_ground', 'against_ice', 'against_normal', 
    'against_poison', 'against_psychic', 'against_rock', 'against_steel', 
    'against_water'
]

# Initialize an empty DataFrame with explicit columns
df = pd.DataFrame(columns=columns)


with open('pokemon_scraper/pokemon_names.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        pokemon_list.append(''.join(row))



# Declaring variables to scrape
def roman_to_int(roman):
    roman_numerals = {
        'I': 1,
        'II': 2,
        'III': 3,
        'IV': 4,
        'V': 5,
        'VI': 6,
        'VII': 7,
        'VIII': 8,
        'IX': 9
    }
    return roman_numerals.get(roman, None)

def map_experience_growth(exp):
    experience_growth = {
        'Slow': 1250000,
        'Medium Slow': 1059860,
        'Medium Fast': 1000000,
        'Fast': 800000,
        'Fluctuating': 1640000,
        'Erratic': 600000,
        'Slightly Slow': 949930,
        'Slightly Fast': 849970
    }
    return experience_growth.get(exp, None)
for pokemon in pokemon_list[1:]:
    
    

    abilities = []
    against_bug = against_dark = against_dragon = against_electric = against_fairy = against_fight = against_fire = against_flying = against_ghost = against_grass = against_ground = against_ice = against_normal = against_poison = against_psychic = against_rock = against_steel = against_water = 1.0
    attack = base_egg_cycle = base_happiness = base_total = capture_rate = defense = experience_growth = hp = pokedex_number = sp_attack = sp_defense = speed = generation = 0
    classfication = japanese_name = name = type1 = type2 = ''
    height_m = weight_kg = percentage_male = 0.0
    is_legendary = 0

    
    url = f'https://bulbapedia.bulbagarden.net/wiki/{pokemon}_(Pok%C3%A9mon)'
    


    html = requests.get(url)
    

    s = BeautifulSoup(html.text, 'html.parser')

    result = s.find('table', class_='roundy')
    
    if result is not None:
        
        #print(s.encode('utf-8'))
        #print(result.encode('utf-8'))
        
        
        # We find a Pokemon's ability/type through an <a> tag with an href attribute that matches the pattern.
        # ex : <a href="/wiki/Levitate_(Ability)" title="Levitate (Ability)">Levitate</a>
        # We want to extract Levitate from the <a> tag
        
        #Find all <a> tags with href attribute matching the pattern
        ability_links = result.find_all('a', href=re.compile(r"\/wiki\/(.+?)_\(Ability\)"))
        type_links = result.find_all('a', href=re.compile(r"\/wiki\/(.+?)_\(type\)"))
        
        hp_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/HP"))
        
        
        attack_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/Stat#Attack"))
        defense_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/Stat#Defense"))
        sp_attack_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/Stat#Special_Attack"))
        sp_defense_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/Stat#Special_Defense"))
        speed_links = s.find("span", {"id":"Game_data"}).find_next('a', href=re.compile(r"\/wiki\/Stat#Speed"))

        classification_links = s.find('a', href=re.compile(r"\/wiki/Pok%C3%A9mon_category"))
        

        height_links = s.find('a', href=re.compile(r"\/wiki/List_of_Pok%C3%A9mon_by_height"))
        weight_links = s.find('a', href=re.compile(r"\/wiki/Weight"))

        base_happiness_link = s.find('a', href=re.compile(r"\/wiki/List_of_Pok%C3%A9mon_by_base_friendship"))

        capture_rate_link = s.find('a', href=re.compile(r"\/wiki/Catch_rate"))

        experience_growth_link = s.find('a', href=re.compile(r"\/wiki/Experience")).find_next('a', href=re.compile(r"\/wiki/Experience"))
        
        percentage_male_link = s.find('a', href=re.compile(r"\/wiki/List_of_Pok%C3%A9mon_by_gender_ratio"))

        pokedex_number_link =  s.find('a', href=re.compile(r"\/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")).find_next('a', href=re.compile(r"\/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"))



        # Extract the text before _(Ability) in the href link
        for link in ability_links:
            href = link.get('href')
            match = re.search(r"\/wiki\/(.+?)_\(Ability\)", href)
            if match:
                #Replace underscores with spaces
                ability_name = match.group(1).replace('_', ' ')  
                
                #check to see if ability is not already in the list
                if(abilities.count(ability_name) == 0 and ability_name != 'Cacophony'):
                    abilities.append(ability_name)

        
        #Extracting the Pokemon's type
        if  s.find(string = ") is a dual-type ") is not None:
        
            pokemon_type = s.find(string = ") is a dual-type ").find_next('a')
            type1 = pokemon_type.get_text().lower()
            pokemon_type = pokemon_type.find_next('a')
            type2 = pokemon_type.get_text().lower()
        else:
            type1 = s.find(string = re.compile(r"\) is (a|an) ")).find_next('a').get_text().split("-")[0].lower()
            type2 = ""

        #Check if the pokemon is legendary or mythical
        if "Mythical Pokémon introduced" in s.text or "Legendary Pokémon introduced" in s.text:
            is_legendary = 1

        
        #extract the pokemon's Japanese name. It is the text after the <i> tag
        japanese_name_tag = s.find('i')
        if japanese_name_tag:
            japanese_name = japanese_name_tag.get_text()
        else:
            japanese_name = "Not Found"

        #Extract the Pokemon's weaknesses against other types
        weakness = s.find("th", string = "Weak to:\n")        
        weakness_list = []
        if weakness:
            tr_parent = weakness.parent

            #Get the next <td> tag
            nested_td = tr_parent.find_all("td")

            for ntd in nested_td:
                
                inline_blocks = ntd.find_all("span", style=re.compile(r"display:\s*inline-block"))
                for block in inline_blocks:
                    # Process each inline-block element as needed
                    inline_content = block.get_text(strip=True)
                    weakness_list.append(inline_content[:-1])
        

        #extracting the Pokemon's resistances against other types
        #resistances are stored in the form of "[TYPE]0.5" or "[TYPE]0.25"
        resistance = s.find("th", string = "Resistant to:\n")        
        resistance_list = []
        if resistance:
            tr_parent = resistance.parent

            #Get the next <td> tag
            nested_td = tr_parent.find_all("td")

            for ntd in nested_td:
                
                inline_blocks = ntd.find_all("span", style=re.compile(r"display:\s*inline-block"))
                for block in inline_blocks:
                    # Process each inline-block element as needed
                    inline_content = block.get_text(strip=True)
                    inline_content = inline_content.replace("½", "0.50").replace("¼", "0.25")

                    
                    resistance_list.append(inline_content[:-1])
            
            #extracting a pokemon's immunities against other types
            #immunities are stored in the form of "[TYPE]0" or "Non" if there are no immunities
            immunity = s.find("th", string = "Immune to:\n")
            immunity_list = []
            if immunity:
                tr_parent = immunity.parent

                #Get the next <td> tag
                nested_td = tr_parent.find_all("td")

                for ntd in nested_td:
                    
                    inline_blocks = ntd.find_all("span", style=re.compile(r"display:\s*inline-block"))
                    for block in inline_blocks:
                        # Process each inline-block element as needed
                        inline_content = block.get_text(strip=True)
                        immunity_list.append(inline_content[:-2])
        
            #Extract the Pokemon's base stats

            
            hp = hp_links.find_next('div').get_text()
            attack = attack_links.find_next('div').get_text()
            defense = defense_links.find_next('div').get_text()
            sp_attack = sp_attack_links.find_next('div').get_text()
            sp_defense = sp_defense_links.find_next('div').get_text()
            speed = speed_links.find_next('div').get_text()

            base_total = int(hp) + int(attack) + int(defense) + int(sp_attack) + int(sp_defense) + int(speed)
                
            #Extract the Pokemon's classification.
            classfication = classification_links.get_text()

            #Extract the base egg steps. Website records cycles. As of most recent games, each cycle is 128 steps
            base_egg_cycle = s.find("small", string = "cycles").find_previous().get_text()
            base_egg_cycle = int(re.search(r'\d+', base_egg_cycle).group())

            #Extract the weight and height in kilograms and meters respectively
            height = height_links.find_next('tr').find_next('td').find_next('td').get_text()
            height = height.split('m')[0].strip()

            weight = weight_links.find_next('tr').find_next('td').find_next('td').get_text()
            weight = weight.split('kg')[0].strip()

            #Extract the base happiness of the Pokemon
            base_happiness = base_happiness_link.find_next('tr').find_next('td').get_text().strip()

            #Extract the capture rate of the Pokemon
            capture_rate = capture_rate_link.find_next('tr').find_next('td').get_text().split()[0].strip()

            #Extract the experience growth of the Pokemon
            experience_growth = experience_growth_link.find_next('tr').find_next('td').get_text().strip()            
            experience_growth = map_experience_growth(experience_growth)

            #Extract the percentage of the pokemon that are male
            
            percentage_male = percentage_male_link.find_next('span').find_next("span").find_next("span").get_text().split()[0][:-1].strip()

            if "Gender unknown" in s.text:
                percentage_male = -1
            
            #Extract the pokedex number of the Pokemon
            pokedex_number = pokedex_number_link.find_next('span').get_text().split(":")[0][1:].strip()
            pokedex_number = int(pokedex_number)

            #Calculate the Pokemon's generation based on the Pokedex Number
            if pokedex_number <= 151:
                generation = 1
            elif pokedex_number <= 251:
                generation = 2
            elif pokedex_number <= 386:
                generation = 3
            elif pokedex_number <= 493:
                generation = 4
            elif pokedex_number <= 649:
                generation = 5
            elif pokedex_number <= 721:
                generation = 6
            elif pokedex_number <= 809:
                generation = 7
            elif pokedex_number <= 905:
                generation = 8
            else:
                generation = 9

            
            
            
            #Calculate the Pokemon's type effectiveness
            
            

            for resistance in resistance_list:
                percent = resistance[-4:]
                resistance = resistance[:-4]
                
                if resistance == "Fighting":
                    against_fight = float(percent)
                if resistance == "Dragon":
                    against_dragon = float(percent)
                if resistance == "Dark":
                    against_dark = float(percent)
                if resistance == "Electric":
                    against_electric = float(percent)
                if resistance == "Normal":
                    against_normal = float(percent)
                if resistance == "Psychic":
                    against_psychic = float(percent)
                if resistance == "Poison":
                    against_poison = float(percent)
                if resistance == "Ghost":
                    against_ghost = float(percent)
                if resistance == "Grass":
                    against_grass = float(percent)
                if resistance == "Water":
                    against_water = float(percent)
                if resistance == "Fire":
                    against_fire = float(percent)
                if resistance == "Ice":
                    against_ice = float(percent)
                if resistance == "Bug":
                    against_bug = float(percent)
                if resistance == "Steel":
                    against_steel = float(percent)
                if resistance == "Rock":
                    against_rock = float(percent)
                if resistance == "Flying":
                    against_flying = float(percent) 
                if resistance == "Ground":
                    against_ground = float(percent)
                if resistance == "Fairy":
                    against_fairy = float(percent)
            
            for weakness in weakness_list:
                multiplier = weakness[-1:]
                weakness = weakness[:-1]
                
                if weakness == "Fighting":
                    against_fight = int(multiplier)
                if weakness == "Dragon":
                    against_dragon = int(multiplier)
                if weakness == "Dark":
                    against_dark = int(multiplier)
                if weakness == "Electric":
                    against_electric = int(multiplier)
                if weakness == "Normal":
                    against_normal = int(multiplier)
                if weakness == "Psychic":
                    against_psychic = int(multiplier)
                if weakness == "Poison":
                    against_poison = int(multiplier)
                if weakness == "Ghost":
                    against_ghost = int(multiplier)
                if weakness == "Grass":
                    against_grass = int(multiplier)
                if weakness == "Water":
                    against_water = int(multiplier)
                if weakness == "Fire":
                    against_fire = int(multiplier)
                if weakness == "Ice":
                    against_ice = int(multiplier)
                if weakness == "Bug":
                    against_bug = int(multiplier)
                if weakness == "Steel":
                    against_steel = int(multiplier)
                if weakness == "Rock":
                    against_rock = int(multiplier)
                if weakness == "Flying":
                    against_flying = int(multiplier) 
                if weakness == "Ground":
                    against_ground = int(multiplier)
                if weakness == "Fairy":
                    against_fairy = int(multiplier)
            
            for immunity in immunity_list:
                if immunity == "Fighting":
                    against_fight = 0
                if immunity == "Dragon":
                    against_dragon = 0
                if immunity == "Dark":
                    against_dark = 0
                if immunity == "Electric":
                    against_electric = 0
                if immunity == "Normal":
                    against_normal = 0
                if immunity == "Psychic":
                    against_psychic = 0
                if immunity == "Poison":
                    against_poison = 0
                if immunity == "Ghost":
                    against_ghost = 0
                if immunity == "Ground":
                    against_ground = 0


    else:
        print(f"No table found for {pokemon}")

    

    data = {
        'name': pokemon,
        'abilities': abilities,
        'type1': type1,
        'type2': type2,
        'is_legendary': is_legendary,
        'japanese_name': japanese_name,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'sp_attack': sp_attack,
        'sp_defense': sp_defense,
        'speed': speed,
        'base_total': base_total,
        'classification': classfication,
        'generation': generation,
        'base_egg_steps': base_egg_cycle,
        'height_m': height,
        'weight_kg': weight,
        'base_happiness': base_happiness,
        'capture_rate': capture_rate,
        'experience_growth': experience_growth,
        'percentage_male': percentage_male,
        'pokedex_number': pokedex_number,
        'against_bug': against_bug,
        'against_dark': against_dark,
        'against_dragon': against_dragon,
        'against_electric': against_electric,
        'against_fairy': against_fairy,
        'against_fight': against_fight,
        'against_fire': against_fire,
        'against_flying': against_flying,
        'against_ghost': against_ghost,
        'against_grass': against_grass,
        'against_ground': against_ground,
        'against_ice': against_ice,
        'against_normal': against_normal,
        'against_poison': against_poison,
        'against_psychic': against_psychic,
        'against_rock': against_rock,
        'against_steel': against_steel,
        'against_water': against_water

    }
    
    print(pokedex_number)

    new_row = pd.DataFrame([data])

    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)



print(df.tail(5))


    
    
df.to_csv('pokemon2.csv', index=False)    

#Issues: Flabebe, Nidoran Male and Nidoran Female cannot be loaded
#        Does not have seperate entries for alternate forms of a Pokemon (including Mega Evolution)

#Solution: Replace the special characters with their respective unicode characters

from bs4 import BeautifulSoup
import csv
import requests
import re

pokemon_list = []

with open('pokemon_scraper/pokemon_names.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        pokemon_list.append(''.join(row))

# Declaring variables to scrape


for pokemon in pokemon_list[1:]:
    
    abilities = []
    against_bug = against_dark = against_dragon = against_electric = against_fairy = against_fight = against_fire = against_flying = against_ghost = against_grass = against_ground = against_ice = against_normal = against_poison = against_psychic = against_rock = against_steel = against_water = 1.0
    attack = base_egg_steps = base_happiness = base_total = capture_rate = defense = experience_growth = hp = pokedex_number = sp_attack = sp_defense = speed = generation = 0
    classfication = japanese_name = name = type1 = type2 = ''
    height_m = weight_kg = percentage_male = 0.0
    is_legendary = False

    url = f'https://bulbapedia.bulbagarden.net/wiki/{pokemon}_(Pok%C3%A9mon)'
    html = requests.get(url)
    
    s = BeautifulSoup(html.text, 'html.parser')

    result = s.find('table', class_='roundy')
    if result is not None:
        
        #print(result.encode('utf-8'))
        
        
        # We find a Pokemon's ability/type through an <a> tag with an href attribute that matches the pattern.
        # ex : <a href="/wiki/Levitate_(Ability)" title="Levitate (Ability)">Levitate</a>
        # We want to extract Levitate from the <a> tag
        
        #Find all <a> tags with href attribute matching the pattern
        ability_links = result.find_all('a', href=re.compile(r"\/wiki\/(.+?)_\(Ability\)"))
        type_links = result.find_all('a', href=re.compile(r"\/wiki\/(.+?)_\(type\)"))
        

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

        
        # Extract the text before _(type) in the href link
        for link in type_links:
            href = link.get('href')
            match = re.search(r"\/wiki\/(.+?)_\(type\)", href)
            if match:
                #Replace underscores with spaces
                type_name = match.group(1).replace('_', ' ')  
                
                #check to see if type is not already in the list
                if(type_name != "Unknown"):
                    if(type1 == ''):
                        type1 = type_name
                    else:
                        type2 = type_name

        #Check if the pokemon is legendary or mythical
        if "Mythical Pokémon introduced" in s.text or "Legendary Pokémon introduced" in s.text:
            is_legendary = True

        
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
                    inline_content = inline_content.replace("½", "0.5").replace("¼", "0.25")

                    
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
                        immunity_list.append(inline_content[:-1])
        
            #Extract the Pokemon's base stats
            


    else:
        print(f"No table found for {pokemon}")

    print(f"Abilities for {pokemon}: {abilities}")
    print(f"Types for {pokemon}: {type1}, {type2}")
    print(f"Legendary: {is_legendary}")
    print(f"Japanese Name: {japanese_name}")
    print(f"Weaknesses: {weakness_list}")
    print(f"Resistances: {resistance_list}")
    print(f"Immunities: {immunity_list}")

    break  

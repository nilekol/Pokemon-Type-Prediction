import scrapy

class PokemonSpider(scrapy.Spider):
    name = 'pokemon'
    start_urls = ['https://www.serebii.net/pokemon/nationalpokedex.shtml'] 

    def parse(self, response):
        # Finding the 'dextable' table. On the serebii website, the dextable table holds the table of all the pokemon information
        dextable = response.css('table.dextable')
        
        # Iterate over <a> tags within the 'dextable' table
        for link in dextable.css('a[href*=pokemon]'):
            pokemon_name = link.css('::text').get()  # Extract the text within <a> tag
            
            # Ensure pokemon_name is not empty before yielding
            if pokemon_name:
                yield {
                    'pokemon_name': pokemon_name.strip()  # Strip any leading/trailing whitespace
                }

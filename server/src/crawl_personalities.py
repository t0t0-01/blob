import requests
from bs4 import BeautifulSoup
import json


# make a request to the webpage
url = "https://www.16personalities.com/personality-types"
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")
#print(soup)

# Find all div elements with class="image animated"
type_containers = soup.select('[class*=type-group]')


data = {}

for type_container in type_containers:
    
    # The class indexing returns a list; we take the second element to get the word we want
    typ = type_container['class'][1]

    data[typ] = {}
    
    personalities = type_container.find_all("a", class_="type")
    
    for personality_container in personalities:
        name = personality_container.h5.text[:personality_container.h5.text.find("-")]
        data[typ][name] = {"image": personality_container.img['src'],
                           "phrase": personality_container.div.text,
                           "link": personality_container['href'],
                           "type": personality_container.h4.text
                           }
        
    
    
    
print(data)


f = open(r"C:\Users\Anton\Desktop/personalities.json","w")
json.dump(data, f, indent=4)
f.close()    


import requests
from bs4 import BeautifulSoup
import json
import ast
import cairosvg
import os

def convert_svg_to_png(url, out_file):
    # convert the svg file to png
    cairosvg.svg2png(url=url, write_to=out_file)
    

def get_introduction_paragraphs(url):
    # make a request to the webpage
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    
    article = soup.find("article")
    
    
    
    definition_div = article.find("div", class_="definition")
    intro_par = definition_div.find_all("p")[-1]
    
    
    
    
    
    elements = [intro_par.text]
    
    first_h2 = article.find('h2')
    
    for sibling in definition_div.find_next_siblings():
        if sibling == first_h2:
            break
        if sibling.name == 'p':
            elements.append(sibling.text)
    
    return elements
    


def get_text_sections(url):
    # make a request to the webpage
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")
    
    
    
    article = soup.find("article")
    
    
    
    # get all h2 elements
    h2_elements = article.find_all('h2')
    
    
    elements = {}
    
    for i in range(len(h2_elements)):
        first_h2 = h2_elements[i]
        second_h2 = first_h2.find_next_sibling('h2')
        
        p_elements = []
        for sibling in first_h2.find_next_siblings():
            if sibling == second_h2:
                break
            if sibling.name == 'p':
                p_elements.append(sibling.text)
                
        elements[first_h2.text] = p_elements
    
    
    return elements


def get_strengths_weaknesses(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, "html.parser")
    article = soup.find("article")
    
    data = {"strengths": {}, "weaknesses": {}}
    
    strengths_weaknesses_list = article.find_all("ul")
        
    
    for pos, strength_or_weakness in enumerate(strengths_weaknesses_list):
        strengths_weaknesses = {}

        t = "strengths" if pos == 0 else "weaknesses"
        points = strength_or_weakness.find_all("li")
        for point in points:
            strengths_weaknesses[point.strong.text] = point.text[point.text.find("–") + 2 :]
            
        
        data[t] = strengths_weaknesses
        
    return data



def get_people(url, as_png=False):
        
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    answers = soup.find('div', class_="celebrities")
    
    str_representation = answers.find('app-carousel')[':celebrities']
    
    str_rep = str_representation.replace("\\", "")
    str_rep = str_rep.replace("null", '""')
    str_rep = str_rep.replace("\\u2019", "'")
    
    dic_rep = ast.literal_eval(str_rep)
    if as_png:
        for person in dic_rep:
            file_name = person['name'].replace(" ", "_") + ".png"
            convert_svg_to_png(person['avatar'], os.path.join(r"C:\Users\Anton\Desktop\celebrities", file_name))
            person['avatar'] = f"./assets/celebrities/{file_name}"
    
        return dic_rep
    else: 
        return ast.literal_eval(str_rep)




def get_branch_links_from_intro(url):
    response = requests.get(url)
    
    links = {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    a_list = soup.find_all('a')
    
    first, second, third = False, False, False
    
    for a in a_list:
        if a.text.strip() == "Strengths and Weaknesses":
            links["Strengths"] = a['href']
            first = True
            
        elif a.text.strip() == "Friendships":
            links["Friendships"] = a['href']
            second = True
            
        elif a.text.strip() == "Introduction":
            links["Introduction"] = a['href']
            third = True
            
        if first and second and third:
            break
            
    return links
    
    
    

def main():
    f = open(r"C:\Users\Anton\Desktop\personalities.json", "r")
    main_hub = json.load(f)
    f.close()
    
    # Remove the first level from the main dictionary
    # The first level corresponds to the type (e.g., Analysts...)
    # Output dictionary should be keys of personalities only
    personalities = {k: v2 for level1 in main_hub.values() for k, v2 in level1.items()}

    data = {}
    for pos, (pers, items) in enumerate(personalities.items()):
        data[pers] = {}
        links = get_branch_links_from_intro(items['link'])
        
        intro_pars = get_introduction_paragraphs(links['Introduction'])
        intro_sections = get_text_sections(links['Introduction'])
        celebrities = get_people(links['Introduction'], as_png=True)
        strengths = get_strengths_weaknesses(links['Strengths'])
        friendships_sections = get_text_sections(links['Friendships'])
        
        
        data[pers]['intro_pars'] = intro_pars
        data[pers]['intro_sections'] = intro_sections
        
        
        data[pers]['celebrities'] = celebrities
        
        
        
        data[pers]['strengths'] = strengths
        data[pers]['friendships_sections'] = friendships_sections
        
        print(f"{ (pos+1) / len(personalities) * 100:.2f}% done")
        
        
    return data
        
        
    
    
data = main()



f = open(r"C:\Users\Anton\Desktop/personalities_details.json","w")
json.dump(data, f, indent=4)
f.close()  




def merge_subset_details():       
    f1 = open(r"C:\Users\Anton\Desktop\personalities.json", "r")
    f2 = open(r"C:\Users\Anton\Desktop\personalities_details.json", "r")
    
    original = json.load(f1)
    details = json.load(f2)
    
    f2.close()
    
    for pers_type in original.values():
        for personality, data in pers_type.items():
            details[personality]["data"] = data
            
    f2 = open(r"C:\Users\Anton\Desktop\personalities_details.json", "w")
    
    json.dump(details, f2, indent=4)
    
    f1.close()
    f2.close()
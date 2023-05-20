# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 21:29:30 2023

@author: Anton
"""
import numpy as np
import random

A = {"Arts & Entertainment": 
         {"Music": 
              {"Rock": {} 
               },
              
              "Movies" : {"Action": {}}
        },
             
             "Sports & Fitness": {"Team Sports": {"Football": {}}}}
             

   

    
B = {"Arts & Entertainment": {"TV Shows": {"Drama": {}}}, "Books": {"Fiction": {}}}



taxonomy = {
  "Arts & Entertainment": {
    "Music": {
      "Rock": {},
      "Pop": {},
      "Hip-hop": {},
      "Electronic": {},
      "Classical": {}
    },
    "Movies": {
      "Action": {},
      "Drama": {},
      "Comedy": {},
      "Romance": {},
      "Horror": {}
    },
    "TV Shows": {
      "Drama": {},
      "Comedy": {},
      "Reality TV": {},
      "Crime & Thriller": {},
      "Sci-Fi & Fantasy": {}
    }
  },
  "Books": {
    "Fiction": {},
    "Non-fiction": {},
    "Romance": {},
    "Thriller & Suspense": {},
    "Science Fiction & Fantasy": {}
  },
  "Sports & Fitness": {
    "Team Sports": {
      "Football": {},
      "Basketball": {},
      "Baseball": {},
      "Hockey": {},
      "Soccer": {}
    },
    "Individual Sports": {
      "Running": {},
      "Cycling": {},
      "Swimming": {},
      "Tennis": {},
      "Golf": {}
    },
    "Fitness & Wellness": {
      "Yoga": {},
      "Pilates": {},
      "Weight Training": {},
      "Cardio": {},
      "Meditation": {}
    }
  },
  "Food & Drink": {
    "Cuisine": {
      "Italian": {},
      "Mexican": {},
      "Chinese": {},
      "Japanese": {},
      "Indian": {}
    },
    "Drinks": {
      "Wine": {},
      "Beer": {},
      "Cocktails": {},
      "Coffee": {},
      "Tea": {}
    },
    "Cooking & Baking": {
      "Recipes": {},
      "Techniques": {},
      "Appliances": {},
      "Ingredients": {},
      "Desserts": {}
    }
  },
  "Travel & Adventure": {
    "Destinations": {
      "Beaches": {},
      "Mountains": {},
      "Cities": {},
      "National Parks": {},
      "Historical Sites": {}
    },
    "Activities": {
      "Hiking": {},
      "Skiing": {},
      "Surfing": {},
      "Scuba Diving": {},
      "Bungee Jumping": {}
    },
    "Cultural Experiences": {
      "Museums": {},
      "Festivals": {},
      "Food Tours": {},
      "Architecture Tours": {},
      "Homestays": {}
    }
  },
  "Hobbies & Crafts": {
    "DIY & Home Improvement": {
      "Painting": {},
      "Carpentry": {},
      "Gardening": {},
      "Interior Design": {},
      "Home Automation": {}
    },
    "Crafts": {
      "Knitting": {},
      "Sewing": {},
      "Crochet": {},
      "Jewelry Making": {},
      "Pottery": {}
    },
    "Games & Puzzles": {
      "Board Games": {},
      "Video Games": {},
      "Crosswords & Sudoku": {},
      "Chess": {},
      "Card Games": {}
    }
  }
}


def get_depths(d, depth=1):
    """
    Returns a dictionary of key-depth pairs for all keys in the input dictionary `d`.
    
    Args:
    - d: dict, input dictionary whose key-depth pairs are to be computed
    - depth: int, depth of the current dictionary
    
    Returns:
    - dict, a dictionary where the keys are the original keys from the input dictionary
    and the values are the corresponding depths of those keys in the input dictionary
    """
    result = {}
    for key, value in d.items():
        result[key] = depth
        if isinstance(value, dict):
            sub_results = get_depths(value, depth=depth+1)
            for sub_key, sub_value in sub_results.items():
                result[key + '.' + sub_key] = sub_value
    return result


def get_index(d, depth=0):
    """
    Returns a dictionary of key-depth pairs for all keys in the input dictionary `d`.
    
    Args:
    - d: dict, input dictionary whose key-depth pairs are to be computed
    - depth: int, depth of the current dictionary
    
    Returns:
    - dict, a dictionary where the keys are the original keys from the input dictionary
    and the values are the corresponding depths of those keys in the input dictionary
    """
    result = {}
    for key, value in d.items():

        result[key] = depth
        depth += 1

        if isinstance(value, dict):
            sub_results = get_index(value, depth)
            for sub_key, sub_value in sub_results.items():

                result[key + '.' + sub_key] = sub_value
                depth += 1

    return result




def get_weights(A):
    depths_of_A = get_depths(A)
    max_depth = max(depths_of_A.values())
    concept_weights = {key: value/max_depth for key, value in depths_of_A.items()}
    
    mx, mn = max(concept_weights.values()), min(concept_weights.values())
    normalized_concept_weights = {key: (value - mn) / (mx - mn) for key, value in concept_weights.items()}


    return normalized_concept_weights, concept_weights


def cos_similarity(v1, v2):
    cosine = np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))
    return cosine




def get_similarity(A, B):
    taxonomy_index = get_index(taxonomy)

    norm_w_A, w_A = get_weights(A)
    
    vector_A = np.zeros(len(taxonomy_index))
    for k, v in w_A.items():
        vector_A[taxonomy_index[k]] = v
    
    
    norm_w_B, w_B = get_weights(B)
    vector_B = np.zeros(len(taxonomy_index))
    for k,v in w_B.items():
        vector_B[taxonomy_index[k]] = v
        
    return cos_similarity(vector_A, vector_B)
    


def generate_random_subset(taxonomy):
    # Select a random number of top-level categories to include
    num_categories = random.randint(1, len(taxonomy))

    # Select a random subset of top-level categories
    categories = random.sample(taxonomy.keys(), num_categories)

    # Create a dictionary containing the selected categories and their subcategories
    result = {}
    for category in categories:
        result[category] = {}
        if taxonomy[category]:
            subcategories = generate_random_subset(taxonomy[category])
            result[category] = subcategories

    return result


test = generate_random_subset(taxonomy)

#print(get_weights(test))

print(get_similarity(A, A))







"""
Test cases: brainstorm some more, and analyze
    Entertainment -> books and Entertainment -> music    >   no entertainment
    Entertainment -> books x2 > entertainment -> books and entertainment -> music
    One is contained in the other
    No relation whatsoever
    Identical
    Different depths. What happens?
    
    Only one item in common, but the common thing is at different depths. 
        Wouldn't matter, cause depth would be encoded in the 
        
    Sub-most thing is different
        
    Question: do the weights actually affect anything? I think not. Let's see.
        It does, but how?

"""












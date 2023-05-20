# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:50:30 2023

@author: Anton
"""

from flask import Flask, request, jsonify
import openai



def ai_api(compliment):
    openai.api_key = "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"
    
    prompt = """
    
    You are a communication and social expert. You will be given a piece of text that represents a compliment a certain user gave to another. The compliment will tackle one of the following topics: sense of humor, intelligence, generosity, positive attitude, emotional intelligence, conversation skills, appearance
    
    Your job is to identify which of these the compliment tackles. You need to return a vector whose elements would be 1 if the compliment tackles this specific topic, and 0 otherwise. The order of the dimensions of the vector follow the order in which I gave them to you.
    
    Return only the vector. Don't include any text. Don't include any explanation. Only print out the vector as is. Don't add any text.
    Here is a sample input: You look great today, your outfit is really stylish.
    Here is the sample output: [0, 0, 0, 0, 0, 0, 1]
    Make sure to follow the format of the sample output exactly
    
    """
    
    topics = ["sense of humor", "intelligence", "generosity", "positive attitude", "emotional intelligence", "conversation skills", "appearance"]
    
    
    labels = []
    
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": compliment},
            ]
        )

    content = response['choices'][0]['message']['content']
    listed = content.strip('][').split(', ')
    labels.append([int(x) for x in listed])
    
    return labels





app = Flask(__name__)



@app.route('/compliment_class', methods=['POST'])
##############
# POST request payload: {'compliments': str}
#
#
def compliment_class():
    
    data = request.get_json(force=True)
    if 'compliment' not in data:
        return jsonify({'error': 'No compliment provided'})
    
    compliment = data['compliment']
    
    prediction = ai_api(compliment)
    
    return {'prediction': prediction}



app.run("0.0.0.0", port=5000)



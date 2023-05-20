# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:50:30 2023

@author: Anton
"""

from flask import Flask, request, jsonify
import openai
import requests
import time



def read_file(filename, chunk_size=5242880):
    """Reads a binary file in chunks and yields the data.

    Parameters
    ----------
    filename : str
        The name of the file to read.
    chunk_size : int, optional
        The size of the chunks to read from the file. The default value is 5242880 bytes (5 MB).

    Yields
    ------
    bytes
        The data read from the file in chunks.

    Raises
    ------
    FileNotFoundError
        If the file cannot be found.
    """

    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def upload_file(path):
    """
    Uploads a file to the AssemblyAI API for transcription.

    Parameters:
    -----------
    path : str
        The path of the file to be uploaded.

    Returns:
    --------
    str
        The URL of the uploaded file.

    Raises:
    -------
    requests.exceptions.RequestException
        If there was an error during the HTTP request.
    """
    
    
    headers = {'authorization': "79fe1aefb66b45fca7e54ed5b2da42d3"}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(path))
     
    url = response.json()['upload_url']
    return url



def assembly_transcription(url, speakers=False):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    
    json = {
      "audio_url": url,
      "speaker_labels": speakers
    
    }
    
    headers = {
      "Authorization": "79fe1aefb66b45fca7e54ed5b2da42d3",
      "Content-Type": "application/json"
    }
    
    response = requests.post(endpoint, json=json, headers=headers)
    
    process_id = response.json()['id']
    
    fetch_endpoint = f"https://api.assemblyai.com/v2/transcript/{process_id}"
    
    fetch_headers = {
        "authorization": "79fe1aefb66b45fca7e54ed5b2da42d3",
    }
    
    response = requests.get(fetch_endpoint, headers=fetch_headers)
    
    while response.json()['status'] == 'processing':
        response = requests.get(fetch_endpoint, headers=fetch_headers)
        
    return response.json()['text']

    #add code to return utterances
    

    
    
def transcribe_local_file(filename):
    return assembly_transcription(upload_file(filename))

        


def ai_api_analysis(conversation, speaker=False):
    openai.api_key = "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"
    
    if not speaker:
        prompt = """You are a communication and social expert. Your job is to identify issues in people's conversations. You will be given a text extract and you need to identify if one of these issues were present in the conversation:
        
        - Lack of empathy and understanding towards others
        - Use of inappropriate or offensive language
        - Bringing up sensitive or controversial topics without regard for the other person's feelings
        - Engaging in negative or hostile behavior, such as insults or verbal attacks
        - Dismissing or belittling the other person's perspective or experiences
        
        Note that each one could have more than one issue. Return ONLY a vector with 1 if the issue is present, and 0 otherwise. Don't name the issue, just use a vector where the dimensions follow the order of the issues as i gave them to you. Don't return anything other than this vector. Don't explain anything. Don't include any text other than the vector."""
        
    else:
        prompt ="""You are a communication and social expert. You will be given a text extract that contains a conversation between two speakers. Your job is to identify each speaker's communication weaknesses. The weaknesses can be one of the following:
                
                - Lack of empathy and understanding towards others
                - Use of inappropriate or offensive language
                - Bringing up sensitive or controversial topics without regard for the other person's feelings
                - Engaging in negative or hostile behavior, such as insults or verbal attacks
                - Dismissing or belittling the other person's perspective or experiences
                
                The text you will be given will be labeled according to speaker. You need to return exactly one vector for each speaker that takes into account all the things said by only this speaker.
                
                The vector will have a 1 if the issue is present, and 0 otherwise. Don't name the issue, just use a vector where the dimensions follow the order of the issues as i gave them to you. Note that each one could have more than one issue. 
                
                Make sure not to confuse the speakers. Pay very close attention to who is exhibiting the issue and put the flag in that speaker's vector. Don't put it in the others'. If B exhibited an issue towards A (for instance, if B was insensitive to A), then the 1 would appear in B's vector. It would not appear in A's. 
                
                Make sure your output follows the following format: '{Speaker A: [x, x, x, x, x], Speaker B: [x, x, x, x, x]}'

                    """

    
    
    response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": conversation},
            ]
        )

    

    content = response['choices'][0]['message']['content']
    listed = content.strip('][').split(', ')
    return [int(x) for x in listed]
    



test_scenario = """Hey man, how are you doing? All's good?

Yeah man, all is good. And you?

All's good too. 

So I hear you graduated as a computer engineer from LAU. What are you doing now?

I'm actually working at Blob

Oh that's great! I hear it's a great place!"""
test_scenario_bad = """
Hey man, how are you doing? All's good?

Yeah man, all is good. And you?

All's good too. 

So I hear you graduated as a computer engineer from LAU. What are you doing now?

I'm actually working at CompanyX

Oh, what's that? Never heard of it... 

It's a small development firm.

Were you not able to secure a job at Google? that's funny. I actually work at Google.

It is what it is man. Great for you."""



app = Flask(__name__)



@app.route('/analysis', methods=['POST'])
##############
# POST request payload: {'filepath': str}
#
#
def analyze_meeting():
    data = request.get_json(force=True)
    if 'filepath' not in data:
        return jsonify({'error': 'No path provided'})
    
    filepath = data['filepath']
    
    transcription = transcribe_local_file(filepath)
    print(transcription)
    analysis = ai_api_analysis(transcription)
    
    return {'prediction': analysis}



app.run("0.0.0.0", port=5000)



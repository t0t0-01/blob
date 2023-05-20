from flask import Flask, request, jsonify

import tensorflow as tf
import tensorflow_text as text


bert_model = tf.keras.models.load_model(r'C:\Users\Anton\OneDrive\Uni\2022-2023\Spring 2023\FYP 2\ML Models\compliment_analysis\models\compliment3_bert')

def predict(sentence):
    result = tf.sigmoid(bert_model(tf.constant([sentence])))

    return result.numpy()[0][0]

app = Flask(__name__)



@app.route('/sentiment', methods=['POST'])
##############
# POST request payload: {'sentence': str}
#
#

def sentiment():
    data = request.get_json(force=True)
    if 'sentence' not in data:
        return jsonify({'error': 'No sentence provided'})
    
    sentence = data['sentence']
    prediction = predict(sentence)
    
    return {'prediction': round(prediction)}



app.run("0.0.0.0", port=6000)



"""
$ sudo apt-get update
$ sudo apt-get install python3-venv
Activate the new virtual environment in a new directory
// Create directory
$ mkdir helloworld
$ cd helloworld
// Create the virtual environment
$ python3 -m venv venv
// Activate the virtual environment
$ source venv/bin/activate
// Install Flask
$ pip install Flask
Create a Simple Flask API
$ sudo nano app.py
// Add this to app.py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

if __name__ == "__main__":
	app.run()
"""
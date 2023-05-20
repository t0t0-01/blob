from flask import Flask, request, jsonify
import json
import base64
import os
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf
import tensorflow_text as text

os.chdir(r"C:\Users\Anton\Desktop\FYP\blob_app\server")


#############################
# Helper Functions
#############################
bert_model = tf.keras.models.load_model(r'C:\Users\Anton\OneDrive\Uni\2022-2023\Spring 2023\FYP 2\ML Models\compliment_analysis\models\compliment3_bert')

def predict(sentence):
    result = tf.sigmoid(bert_model(tf.constant([sentence])))

    return result.numpy()[0][0]

##############################

    

app = Flask(__name__)



@app.route('/upload_id', methods=['POST'])
##############
# POST request payload: {'image': base64_str}
#
#

def upload_id():
    data = request.get_json(force=True)
    if 'image' not in data:
        return jsonify({'error': 'No sentence provided'})
    
    base64_str = data['image']
    img_bytes = base64.b64decode(base64_str)
    
    # Create an image object from the bytes
    img = Image.open(BytesIO(img_bytes))
    
    # Display the image
    plt.imshow(img)
    plt.axis('off')
    plt.show()    
    
    return {'success': True}



@app.route('/get_personalities_data', methods=['GET'])
##############

def personalities_data():
    ####
    # We assume that the data returned by this function contains both the summarized data (in a key data) as well as the details
    ####
    personality = request.args.get('personality')


    f = open(r"./data/personalities_details.json", "r",  encoding="utf8")
    j = json.load(f)
    f.close()
    
    celebrities = j[personality]["celebrities"]
    for celeb in celebrities:
        link = celeb['avatar']
        with open(link, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            
        celeb['avatar'] = encoded_string
        
    j[personality]["celebrities"] = celebrities
    
    
    strengths = j[personality]["strengths"]['strengths']
    for strength in strengths:
        link = strengths[strength]['image']
        with open(link, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        strengths[strength]['image'] = encoded_string
    j[personality]['strengths']['strengths'] = strengths
    
    weaknesses = j[personality]["strengths"]['weaknesses']
    for weakness in weaknesses:
        link = weaknesses[weakness]['image']
        with open(link, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        weaknesses[weakness]['image'] = encoded_string
    j[personality]['strengths']['weaknesses'] = weaknesses

    
    
    return {"data": j[personality]}



@app.route('/user/get_by_id', methods=['GET'])
##############

def get_user_by_id():
    user_id = request.args.get('id')
    
    if user_id == "Antonio":
        with open(r"C:\Users\Anton\OneDrive\Documents\CV\Image.jpeg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            first_name = "Antonio"
            last_name = "Chedid"
            phone = "+96176304061"
    
    else:

        with open("./assets/omar_pic.jfif", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            first_name = "Omar"
            last_name = "Chaiban"
            phone = "+96170511065"
    
    
    
    with open(r"C:\Users\Anton\Desktop\FYP\blob_app\blob_app\assets\interests_icons\italian_food.png", "rb") as image_file:
        encoded_interest = base64.b64encode(image_file.read()).decode('utf-8')
    
    
    with open(r"./assets/hiking.png", "rb") as image_file:
        encoded_interest_2 = base64.b64encode(image_file.read()).decode('utf-8')
        
        
        
    return {"personality": {"name": "INTJ", "type": "Architect", "group": "Analysts", "image": "https://www.16personalities.com/static/images/personality-types/avatars/intj-architect.svg?v=2",}, "first_name": first_name, "last_name": last_name, "email": "antoniochedid@outlook.com", "phone_nb": phone, "date_of_birth": "10/12/2001", "picture": encoded_string, "interests": [{
                "title": "Italian Cuisine",
                "image": encoded_interest,
                "description": 
                  "Savor the tastes of the Mediterranean as you indulge in the rich flavors of Italy, from savory pastas and pizzas to sweet gelato and tiramisu.",
              }, {"title": "Hiking", "image": encoded_interest_2, "description": "Unleash your inner explorer, feel the thrill of conquering new heights, and witness awe-inspiring landscapes that leave you in awe."}
            ]}


@app.route('/user/get_friends', methods=['GET'])
##############

def get_user_friends():
    user_id = request.args.get('id')
    
    with open(r"C:\Users\Anton\OneDrive\Documents\CV\Image.jpeg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    sample_response =[
  {"user_id": 1, "image": "", "first_name": "Omar", "last_name": "Chaiban"},
  {"user_id": 2, "image": "", "first_name": "Ethan", "last_name": "Johnson"},
  {"user_id": 3, "image": "", "first_name": "Olivia", "last_name": "Smith"},
  {"user_id": 4, "image": "", "first_name": "Ben", "last_name": "Anderson"},
  {"user_id": 5, "image": "", "first_name": "Ava", "last_name": "Johnson"},
  {"user_id": 6, "image": "", "first_name": "Sam", "last_name": "Thomp"},
  {"user_id": 7, "image": "", "first_name": "Mia", "last_name": "Davis"},
  {"user_id": 8, "image": "", "first_name": "Alex", "last_name": "Martinez"},
  {"user_id": 9, "image": "", "first_name": "Charly", "last_name": "Wilson"},
  {"user_id": 10, "image": "", "first_name": "Daniel", "last_name": "Rodriguez"},
  {"user_id": 11, "image": "", "first_name": "Emily", "last_name": "Taylor"},
  {"user_id": 12, "image": "", "first_name": "George", "last_name": "Bush"}

]







    
    return {"data": sample_response}


@app.route('/user/get_friend_by_name', methods=['GET'])

def get_friend_by_name():
    friend_name = request.args.get('id')
    

        
    sample_response = [{"user_id": 1, "image": "", "first_name": "Antonio", "last_name": "Chedid"}] * 7

    
    return {"data": sample_response}


@app.route('/venues/get_all', methods=['GET'])
##############

def get_all_venues():
    f = open("./data/zones_get_all.json", "r")
    dic = json.load(f)
    f.close()

    
    return {"data": dic}





@app.route('/venues/get_by_id', methods=['GET'])
def get_venue_by_id():
    venue_id = request.args.get('venue_id')
    print(venue_id)
    f = open("./data/zones_get_by_id.json", "r")
    dic = json.load(f)[0]
    
    with open("./assets/swiss_butter_logo.jpg", "rb") as image_file:
        dic['images'][0] = base64.b64encode(image_file.read()).decode('utf-8')
    

    f.close()
    
    
    
    return dic


@app.route('/venues/get_date_time', methods=['GET'])
def get_date_time():
    venue_id = request.args.get('venue_id')
    
    
    return {
  "current_date": "2023-05-15",
  "current_week": {
    "15": 0,
    "16": 0,
    "17": 0,
    "18": 0,
    "19": 1,
    "20": 1,
    "21": 1
  },
  "time": {
    "current_time": "21:53:42",
    "available_times": {
      "19": [
        {
          "time": "09:00 AM",
          "available": 0
        },
        {
          "time": "10:00 AM",
          "available": 0
        },
        {
          "time": "11:00 AM",
          "available": 1
        },
        {
          "time": "12:00 PM",
          "available": 1
        },
        {
          "time": "01:00 PM",
          "available": 1
        },
        {
          "time": "02:00 PM",
          "available": 1
        },
        {
          "time": "03:00 PM",
          "available": 1
        },
        {
          "time": "04:00 PM",
          "available": 1
        },
        {
          "time": "05:00 PM",
          "available": 1
        },
        {
          "time": "06:00 PM",
          "available": 1
        },
        {
          "time": "07:00 PM",
          "available": 1
        },
        {
          "time": "08:00 PM",
          "available": 1
        },
        {
          "time": "09:00 PM",
          "available": 0
        },
        {
          "time": "10:00 PM",
          "available": 0
        },
        {
          "time": "11:00 PM",
          "available": 1
        }
      ],
      "20": [
        {
          "time": "09:00 AM",
          "available": 1
        },
        {
          "time": "10:00 AM",
          "available": 1
        },
        {
          "time": "11:00 AM",
          "available": 1
        },
        {
          "time": "12:00 PM",
          "available": 1
        },
        {
          "time": "01:00 PM",
          "available": 1
        },
        {
          "time": "02:00 PM",
          "available": 1
        },
        {
          "time": "03:00 PM",
          "available": 1
        },
        {
          "time": "04:00 PM",
          "available": 1
        },
        {
          "time": "05:00 PM",
          "available": 1
        },
        {
          "time": "06:00 PM",
          "available": 1
        },
        {
          "time": "07:00 PM",
          "available": 1
        },
        {
          "time": "08:00 PM",
          "available": 1
        },
        {
          "time": "09:00 PM",
          "available": 1
        },
        {
          "time": "10:00 PM",
          "available": 1
        },
        {
          "time": "11:00 PM",
          "available": 1
        }
      ]
    }
  }
}



@app.route('/user/reserve', methods=['POST'])
##############
# POST request payload: {customer_id: '', time: '', venue_id: ''}
#
#

def submit_booking():
    data = request.get_json(force=True)
    print(data)

    customer_id = data["customer_id"]
    time = data["time"]
    venue_id = data["venue_id"]
    return {'customer_id': customer_id, "time": time, "venue_id": venue_id}






@app.route('/venues/get_review', methods=['GET'])
##############

def get_reviews_of_venues():
    venue_id = request.args.get('venue_id')


        
    sample_response = [{"customer": {"first_name": "Anton", "last_name": "Ched"}, "comment": "Great Food!", "rating": 4.5}]

    
    return {"data": sample_response}


@app.route('/user/all_booking', methods=['GET'])
##############

def get_bookings_of_user():
    user_id = request.args.get('user_id')
    
    with open("./assets/swiss_butter_logo.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    
    sample_response = {"passed_bookings": [{"venue": {"images": encoded_string, "name": "Swiss Butter", "category": ["Restaurant", "Casual Dining"], "review_rate": 4.5}, "booking_date": "05/15/2023 - 20:00"}], "upcoming_bookings": [{"venue": {"images": encoded_string, "name": "Swiss Butter", "category": ["Restaurant", "Casual Dining"], "review_rate": 4.5}, "booking_date": "05/19/2023 - 20:00"}]}


    return sample_response
        

    
@app.route('/user/review_venue', methods=['POST'])
##############
# POST request payload: {'venue_id': , customer_id: ,rating: , comment: ,}
##############

def submit_review():
    data = request.get_json(force=True)
    
    venue_id = data["venue_id"]
    customer_id = data["customer_id"]
    rating = data["rating"]
    comment = data["comment"]

    print("Done")
    return {"data": "ok"}    
    
    
    
    

    base64 = data['image']
    print(base64)
    
    return {'image': "received"}



@app.route('/user/get_personality_dashboard', methods=['GET'])
##############

def get_dashboard():
    user_id = request.args.get('user_id')
    
    
    f = open("./data/blob_tips.json", "r")
    data = json.load(f)
    f.close()
    
    for issue in data:
        with open(f"./assets/analyzed_issues/{issue['image']}","rb") as image_file:
            issue['image'] = base64.b64encode(image_file.read()).decode('utf-8')
            
    with open("./assets/omar_pic.jfif", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    with open("./assets/person.jpg", "rb") as image_file:
        encoded_2 = base64.b64encode(image_file.read()).decode('utf-8')



    sample_response={"blob_tips":data, "user_compliments": [{
                      "user": {"name": "Omar Chaiban", "image": encoded_string},
                      "classes": {
                        "conversation": 0,
                        "humor": 1,
                        "intelligence": 0,
                        "generosity": 0,
                        "positivity": 0,
                        "emotional": 0,
                        "conversation": 0,
                        "appearance": 0,
                      },
                      "compliment": "Thanks for bringing laughter and joy into our interactions. Keep the humor flowing!",
                    }, {
                      "user": {"name": "John Doe", "image": encoded_2},
                      "classes": {
                        "conversation": 0,
                        "humor": 1,
                        "intelligence": 0,
                        "generosity": 0,
                        "positivity": 0,
                        "emotional": 1,
                        "conversation": 0,
                        "appearance": 0,
                      },
                      "compliment": "Your genuine concern and support make a significant impact on those around you, as they know they can rely on you for understanding and empathy. Also, thanks for all the laughs!",
                    }]}

    return sample_response

@app.route('/user/get_past_common_trips', methods=['GET'])
##############
def get_past_trips_between_users():
    user_id = request.args.get('user_id')
    friend_id = request.args.get('friend_id')
    
    with open("./assets/swiss_butter_logo.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    
    sample_response = {"data": [{"venue": {"images": encoded_string, "name": "Swiss Butter", "category": ["Restaurant", "Casual Dining"], "review_rate": 4.5}, "booking_date": "05/07/23"}]}


    return sample_response
        

@app.route('/get_list_of_interests', methods=['GET'])

def get_list_of_interests():
    f = open("./data/interests_description.json", "r")
    overall_arr = json.load(f)
    f.close()
    
    for category in overall_arr:
        for topic in category["topics"]:
            for interest in topic["interests"]:
                with open(interest['thumbnail'], "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    interest["thumbnail"] = encoded_string
    
    
    sample_response = { "data": overall_arr }


    return sample_response



UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/user/upload_recording', methods=['POST'])
def upload_recording():
    if 'file' not in request.files:
        return {"status": "No file selected"}
    file = request.files['file']
    if file.filename == '':
        return {"status": "No file selected"}
    
    else:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return {"status": "ok"}


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
    
    return {'prediction': int(prediction >= 0.7)}
    

    

app.run("0.0.0.0", port=5000)

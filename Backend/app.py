from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore
import firebase_admin
import os 
from dotenv import load_dotenv




load_dotenv()


app = Flask(__name__)



# Initialize Firebase by refrencing the credentials within the json file
credentials_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred)
#initialize the database
db = firestore.client()


#Register function all we have to do in the front end is make it point to this route and send the data 
@app.route('/register', methods=['POST'])
def register():
    try:
        # Get data from request
        data = request.json
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
            
        # Create document with username as ID
        doc_ref = db.collection('users').document(username)
        
        # Store user data
        doc_ref.set({
            'username': username,
            'name': name,
            'email': email,
            'password': password,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({'message': 'Data stored successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
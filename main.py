from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
from flask import Flask, request, render_template
from flask import request, redirect, url_for,session
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from flask import request
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    username=db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,fullname,email,username,password):
        self.fullname=fullname
        self.username= username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


# Load the trained model (ensure the model is saved after training and path is correct)
model = tf.keras.models.load_model('my_model.h5')


# # Dummy user data for demonstration purposes
# users = {
#     'root': '123',
#     'user2': 'password2'
# }

# @app.route('/', methods=['GET'])
# def root():
#     user = User.query.filter_by(username=session['username']).first()
#     return render_template('homepage.html',user=user)
@app.route('/', methods=['GET'])
def root():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template('homepage.html', user=user)
    else:
        # Redirect the user to the login page if not logged in
        return redirect(url_for('login'))

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username= request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['username'] = user.username
            session['user_id'] = user.id
            return redirect('/')
        else:
             error = 'Invalid username or password. Please try again.'
             return render_template('login.html',error=error)

    return render_template('login.html')
  




@app.route('/logout', methods=['GET'])
def logout():
    if 'user_id' in session:
        # Remove the 'user_id' from the session
        session.pop('user_id')

    if 'username' in session:
        # Get the username from the session
        username = session['username']

        # Remove the user from the database
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()

        # Clear the 'username' from the session
        session.pop('username')

    return render_template('logout.html')



# @app.route('/logout', methods=['GET'])
# def logout():
#     return render_template('logout.html')

@app.route('/signup', methods=['GET','POST'])  # Define the route for the signup page
def signup():
     if request.method == 'POST':
        # handle request
        fullname = request.form['fullname']
        email = request.form['email']
        username=request.form['username']
        password = request.form['password']

        new_user = User(fullname=fullname,email=email,username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
     error="Something Wrong Happened, please try again!"
     return render_template('signup.html', error=error)



class_labels = {0: 'afan', 1: 'alshees', 2: 'depelodia', 3: 'fyozariomi', 4: 'khayas', 5: 'lafha', 6: 'leaf', 7: 'mayalan', 8: 'tabaqqu3', 9: 'takashor', 10: 'tashteeb', 11: 'thobool', 12:"healthy"}

@app.route('/predict', methods=['POST'])
def predict():
    img_file = request.files['image']
    
    # Convert the FileStorage to a BytesIO object
    img_bytes = BytesIO(img_file.read())

    # Load the image directly from BytesIO
    img = image.load_img(img_bytes, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    # Perform prediction
    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_label = class_labels.get(predicted_class_index, 'Unknown')  # Handle case where index is not in class_labels

    return render_template('result.html', prediction=predicted_label)

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    # Run the Flask app, dynamically binding to the specified port or defaulting to 8080
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

import cv2
import face_recognition
import mysql.connector
import numpy as np

# Connect to MySQL database
def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="aju.magic13",
        database="votingsystempictures"
    )
    return connection

# Capture an image from the webcam
def capture_image():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()
    cv2.destroyAllWindows()
    return frame

# Register a new voter
def register_voter(voter_id):
    # Capture voter's face
    frame = capture_image()
    face_locations = face_recognition.face_locations(frame)
    
    if len(face_locations) == 1:
        face_encoding = face_recognition.face_encodings(frame)[0]
        
        # Save face encoding to database along with voter ID
        connection = connect_db()
        cursor = connection.cursor()
        sql = "INSERT INTO voters (voter_id, face_encoding) VALUES (%s, %s)"
        cursor.execute(sql, (voter_id, face_encoding.tobytes()))
        connection.commit()
        connection.close()
        
        print(f"Voter with ID {voter_id} registered successfully.")
    else:
        print("Error: Make sure exactly one face is visible.")

# Login function
def login_voter():
    voter_id = input("Enter your Voter ID: ")

    # Capture login face
    login_frame = capture_image()
    login_face_encoding = face_recognition.face_encodings(login_frame)[0]
    
    # Fetch face encoding for the given voter ID from database
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT face_encoding FROM voters WHERE voter_id = %s", (voter_id,))
    result = cursor.fetchone()
    connection.close()

    if result:
        db_face_encoding = np.frombuffer(result[0], dtype=np.float64)
        
        # Compare the captured face with the stored face encoding
        matches = face_recognition.compare_faces([db_face_encoding], login_face_encoding)
        
        if matches[0]:
            print(f"Login successful! Voter ID {voter_id} recognized.")
        else:
            print("Login failed. Face does not match the Voter ID.")
    else:
        print("No Voter found with the given Voter ID.")

# Example usage
while True:
    action = input("Enter 'register' to register or 'login' to login: ")
    if action == "register":
        voter_id = input("Enter your Voter ID: ")
        register_voter(voter_id)
    elif action == "login":
        login_voter()
    else:
        break

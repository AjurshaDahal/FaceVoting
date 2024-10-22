return connection

# # Capture an image from the webcam
# def capture_image():
#     video_capture = cv2.VideoCapture(0)
#     ret, frame = video_capture.read()
#     video_capture.release()
#     cv2.destroyAllWindows()
#     return frame

# # Register a new voter
# def register_voter(voter_id):
#     # Capture voter's face
#     frame = capture_image()
#     face_locations = face_recognition.face_locations(frame)

#     if len(face_locations) == 1:
#         face_encoding = face_recognition.face_encodings(frame)[0]
        
#         # Convert the face encoding to a byte format for storage
#         face_encoding_bytes = face_encoding.tobytes()

#         # Save the voter ID and face encoding to the database
#         connection = connect_db()
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO voters (voter_id, face_encoding) VALUES (%s, %s)", (voter_id, face_encoding_bytes))
#         connection.commit()
#         connection.close()
#         print(f"Voter ID {voter_id} registered successfully.")
#     else:
#         print("Error: Unable to detect exactly one face. Registration failed.")

# # Login function
# def login_voter():
#     voter_id = input("Enter your Voter ID: ")

#     # Capture login face
#     login_frame = capture_image()
#     login_face_encoding = face_recognition.face_encodings(login_frame)[0]
#     if len(login_face_encoding) == 0:
#         print("Error: No face detected. Login failed.")
#         return
    
#     login_face_encoding = login_face_encoding[0]

#     # Fetch face encoding for the given voter ID from database
#     connection = connect_db()
#     cursor = connection.cursor()
#     cursor.execute("SELECT face_encoding FROM voters WHERE voter_id = %s", (voter_id,))
#     result = cursor.fetchone()
#     connection.close()

#     if result:
#         db_face_encoding = np.frombuffer(result[0], dtype=np.float64)
        
#         # Compare the captured face with the stored face encoding
#         matches = face_recognition.compare_faces([db_face_encoding], login_face_encoding)
        
#         if matches[0]:
#             print(f"Login successful! Voter ID {voter_id} recognized.")
#         else:
#             print("Login failed. Face does not match the Voter ID.")
#     else:
#         print("No Voter found with the given Voter ID.")

# # Example usage
# while True:
#     action = input("Enter 'register' to register or 'login' to login: ")
#     if action == "register":
#         voter_id = input("Enter your Voter ID: ")
#         register_voter(voter_id)
#     elif action == "login":
#         login_voter()
#     else:
#         break

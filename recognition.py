import cv2
import face_recognition
import mysql.connector
import numpy as np

# Connect to the database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Aju.magic13",
        database="voting_system"
    )

# Capture image from webcam
def capture_image():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()
    if ret:
        return frame
    else:
        print("Error: Could not capture image from webcam.")
        return None

# Register a new voter
def register_voter(voter_id):
    frame = capture_image()
    if frame is None:
        print("Error: No image captured.")
        return

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)

    if len(face_locations) == 1:  # Check if exactly one face is detected
        face_encoding = face_recognition.face_encodings(rgb_frame)[0]
        face_encoding_bytes = face_encoding.tobytes()

        # Insert face encoding into the voters table
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO voters (voter_id, face_encoding) VALUES (%s, %s)", (voter_id, face_encoding_bytes))
        connection.commit()
        cursor.close()
        connection.close()
        print(f"Voter ID {voter_id} registered successfully.")
    else:
        print("Error: Unable to detect exactly one face. Registration failed.")

# Capture video and check face match
def start_video_capture(voter_id):
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not capture image from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        match_result = "False"  # Default result
        if len(face_locations) > 0:  # If faces are detected
            login_face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if login_face_encodings:
                login_face_encoding = login_face_encodings[0]

                # Retrieve stored face encoding from the database
                connection = connect_db()
                cursor = connection.cursor()
                cursor.execute("SELECT face_encoding FROM voters WHERE voter_id = %s", (voter_id,))
                result = cursor.fetchone()

                if result:
                    db_face_encoding = np.frombuffer(result[0], dtype=np.float64)
                    # Compare the face encodings
                    matches = face_recognition.compare_faces([db_face_encoding], login_face_encoding)
                    if matches[0]:
                        match_result = "True"
                        cv2.putText(frame, "Login Successful!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "Login Failed!", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Draw a rectangle around the detected face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the match result
        cv2.putText(frame, match_result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show the video feed
        cv2.imshow("Video", frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Example usage
while True:
    action = input("Enter 'register <Voter ID>' to register or 'login <Voter ID>' to login (or 'exit' to quit): ")
    if action.startswith("register"):
        voter_id = action.split()[1]
        register_voter(voter_id)
    elif action.startswith("login"):
        voter_id = action.split()[1]
        start_video_capture(voter_id)
    elif action == "exit":
        break
    else:
        print("Invalid command. Please try again.")

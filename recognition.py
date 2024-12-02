import cv2
import face_recognition
import mysql.connector
import numpy as np

# Connect to the database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Aju.magic13",
            database="voting_system"
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection failed: {e}")
        return None

# Registration process
def register_voter(voter_id):
    print(f"Attempting to register Voter ID: {voter_id}")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not access the webcam.")
        return

    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM voters WHERE voter_id = %s", (voter_id,))
            result = cursor.fetchone()
            if result:
                print(f"Voter ID {voter_id} is already registered.")
                cursor.close()
                connection.close()
                video_capture.release()
                return
            cursor.close()
            connection.close()

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        video_capture.release()
        return

    print("Please position your face within the frame for registration.")
    face_registered = False

    while not face_registered:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not capture image from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Green rectangle

        # Display the video feed
        cv2.imshow("Register Face", frame)

        # Check if exactly one face is detected
        if len(face_locations) == 1:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            print("Face detected. Registering...")

            try:
                connection = connect_db()
                if connection:
                    cursor = connection.cursor()
                    face_encoding_bytes = face_encoding.tobytes()
                    cursor.execute("INSERT INTO voters (voter_id, face_encoding) VALUES (%s, %s)", 
                                   (voter_id, face_encoding_bytes))
                    connection.commit()
                    print(f"Voter ID {voter_id} registered successfully.")
                    face_registered = True
                    cursor.close()
                    connection.close()
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
                break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to cancel registration
            print("Exiting registration process.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Login process with face frame and success/failure message
def start_video_capture(voter_id):
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not access the webcam.")
        return

    print("Please position your face within the frame to log in.")
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not capture image from webcam.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)  # Blue rectangle

        # Display the video feed with the rectangle around the face
        cv2.imshow("Login Face", frame)

        # If faces are detected, try logging in
        if len(face_locations) > 0:
            login_face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            try:
                connection = connect_db()
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT face_encoding FROM voters WHERE voter_id = %s", (voter_id,))
                    result = cursor.fetchone()

                    if result:
                        db_face_encoding = np.frombuffer(result[0], dtype=np.float64)
                        matches = face_recognition.compare_faces([db_face_encoding], login_face_encodings[0])

                        if matches[0]:
                            print("Login Successful!")
                            cv2.putText(frame, "Login Successful!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            cv2.imshow("Login Face", frame)
                            cv2.waitKey(2000)  # Wait for 2 seconds to display success message
                            video_capture.release()
                            cv2.destroyAllWindows()
                            return
                        else:
                            print("Face did not match. Login failed.")
                            cv2.putText(frame, "Login Failed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            cv2.imshow("Login Face", frame)
                            cv2.waitKey(2000)  # Wait for 2 seconds to display failure message
                    else:
                        print("Voter ID not found in the database.")
                        cv2.putText(frame, "Voter ID not found", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        cv2.imshow("Login Face", frame)
                        cv2.waitKey(2000)

                    cursor.close()
                    connection.close()
            except mysql.connector.Error as e:
                print(f"Database error: {e}")

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit login
            print("Exiting login process.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Main program loop
while True:
    action = input("Enter 'register <Voter ID>' to register, 'login <Voter ID>' to log in, or 'exit' to quit: ").strip()
    if action.lower().startswith("register"):
        voter_id = action.split()[1]
        register_voter(voter_id)
    elif action.lower().startswith("login"):
        voter_id = action.split()[1]
        start_video_capture(voter_id)
    elif action.lower() == "exit":
        break
    else:
        print("Invalid command. Please try again.")

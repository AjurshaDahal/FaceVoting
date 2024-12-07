import mysql.connector

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

# Function to handle voting
def vote_for_party(voter_id):
    print("Login Successful! Please choose a party to vote for:")
    print("1. Party A")
    print("2. Party B")
    print("3. Party C")

    choice = input("Enter the party number: ")

    # Map choice to party name
    party_name = ""
    if choice == '1':
        party_name = "Party A"
    elif choice == '2':
        party_name = "Party B"
    elif choice == '3':
        party_name = "Party C"
    else:
        print("Invalid choice.")
        return

    # Store the vote in the database
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO votes (voter_id, party_name) VALUES (%s, %s)", (voter_id, party_name))
            connection.commit()
            print(f"Vote for {party_name} by Voter ID {voter_id} recorded successfully.")
            cursor.close()
            connection.close()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")

# Example usage
while True:
    voter_id = input("Enter Voter ID to vote (or 'exit' to quit): ").strip()
    if voter_id.lower() == "exit":
        break
    vote_for_party(voter_id)

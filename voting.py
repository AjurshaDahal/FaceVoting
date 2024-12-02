# Simple Voting System with Admin Authentication and Persistence

# Initial vote counts (could be loaded from a file in a real-world scenario)
votes_lotus = 0
votes_sunflower = 0

# Admin authentication (hardcoded for simplicity)
admin_password = "admin123"

# Function to authenticate admin
def authenticate_admin():
    password = input("Enter admin password to start voting: ")
    if password == admin_password:
        print("Admin authenticated. Voting can now begin.")
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

# Function to cast votes
def cast_vote():
    global votes_lotus, votes_sunflower
    print("Welcome to the Voting System")
    print("Please vote for one of the following candidates:")
    print("1. Lotus")
    print("2. Sunflower")

    while True:
        choice = input("\nEnter 1 for Lotus, 2 for Sunflower, or 'end' to stop voting: ")
        if choice == '1':
            votes_lotus += 1
            print("Vote recorded for Lotus.")
        elif choice == '2':
            votes_sunflower += 1
            print("Vote recorded for Sunflower.")
        elif choice.lower() == 'end':
            print("Voting has ended.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 'end' to stop.")

# Function to show results
def show_results():
    print("\nFinal Results:")
    print(f"Lotus: {votes_lotus} votes")
    print(f"Sunflower: {votes_sunflower} votes")

    if votes_lotus > votes_sunflower:
        print("Lotus is the winner!")
    elif votes_sunflower > votes_lotus:
        print("Sunflower is the winner!")
    else:
        print("It's a tie!")

# Function to save the results to a file
def save_results():
    with open('vote_results.txt', 'w') as file:
        file.write(f"Lotus: {votes_lotus}\n")
        file.write(f"Sunflower: {votes_sunflower}\n")
    print("Results have been saved to 'vote_results.txt'.")

# Function to load results from a file
def load_results():
    global votes_lotus, votes_sunflower
    try:
        with open('vote_results.txt', 'r') as file:
            lines = file.readlines()
            votes_lotus = int(lines[0].split(':')[1].strip())
            votes_sunflower = int(lines[1].split(':')[1].strip())
            print("Previous vote results loaded.")
    except FileNotFoundError:
        print("No previous results found. Starting fresh.")

# Main menu for user interaction
def main_menu():
    while True:
        print("\n--- Voting System ---")
        print("1. Start Voting")
        print("2. Show Results")
        print("3. Exit")

        choice = input("Choose an option (1/2/3): ")
        if choice == '1':
            if authenticate_admin():
                load_results()  # Load previous results
                cast_vote()
                save_results()  # Save updated results after voting
        elif choice == '2':
            show_results()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

# Run the voting system
if __name__ == "__main__":
    main_menu()


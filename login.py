import json
import recommender
import library
import pandas as pd 
from recommender import recommendation #dont remove this it will not call the reccomendation funtion later, both imports are needed

file_name = pd.read_csv('ratings.csv')
movie_ratings = recommender.get_ratings()
movies = recommender.get_movies()

def register(user_id, password):
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}
        while True:
            if not str(user_id).isdigit():
                print("Error: User ID must be a numerical value.")
                continue
            user_id_str = str(user_id)
            if user_id_str in users:
                print("Error: User ID already exists. Please choose another user ID.")
                user_id = int(input("Enter a new user ID: "))
                continue

            users[user_id_str] = password
            with open('users.json', 'w') as file:
                json.dump(users, file)
            print("Registration successful. Please log in.")
            login()
    

def login():
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        print("Error: Can't open the users.json file")
        return False

    while True:
        try:
            user_id = input("Enter your user ID: ")
            if user_id == 'quit':
                input_ui()
            if not user_id.isdigit():
                raise ValueError("User IDs can only have numerical values")
            user_id_str = str(user_id)

            password = input("Enter your password: ")
            if user_id_str in users and users[user_id_str] == password:
                print(f"\nWelcome, {user_id_str}!")
                menu(user_id_str)
            elif user_id_str == 'admin' and password == 'admin':
                try:
                    with open('users.json', 'r') as file:
                        users = json.load(file)
                except FileNotFoundError:
                    print("Error: Can't open the users.json file")
                    break
                print("List of all user IDs and passwords:")
                for user_id, passwd in users.items():
                    print(f"User ID: {user_id}, Password: {passwd}")
                break
            else:
                print("Invalid user ID or password. Please try again or enter 'quit' to return to the main menu\n")
        except ValueError as e:
            print(f"Error: {e}")

def menu(user_id):
    while True:
        print("\nPlease choose from the commands displayed: ")
        print("-Type 'display' to display movies.")
        print("-Type 'update' to update a movie.")
        print("-Type 'delete' to delete a previous rating.")
        print("-Type 'recommend' to recommend movies.")
        print("-Type 'quit' to quit the system.")
        cmd = input("Input command: ")
        if cmd == 'update':
            while True:
                movie_to_update = input("What movie would you like to update? (type 'back' to go back) ")
                if movie_to_update == 'back':
                    break
                if movie_to_update in movies['title'].values:
                    while True:
                        new_rating = float(input("What is the new rating for the movie (0-5)? "))
                        if 1 <= new_rating <= 5:
                            library.update_rating(user_id, movie_to_update, new_rating)
                            print("Rating updated")
                            break
                        else:
                            print("Please Enter a decimal value from 1-5")
                else:
                    print("Error Invalid movie name")

        elif cmd == 'display':
            key_word = input("Enter a key word: ")
            library.display_movies(key_word)
            while True:
                back = input("\nWould you like to go back? (yes): ").lower()
                if back == 'yes':
                    break
                else: 
                    print("Error invalid entry")
        elif cmd == 'delete':
            while True:
                movie_to_delete = input("What movie would you like to delete from the list of ratings? (type 'back' to go back) ")
                if movie_to_delete == 'back':
                    break
                while True:
                    if movie_to_delete in movies['title'].values:
                        library.delete_rating(user_id, movie_to_delete)
                        print("Rating Deleted")
                        break
                    else:
                        print("Movie Title not in list")
                        break

        elif cmd == 'recommend':
            print('Recommendations for user ', user_id)
            recommended_movies = recommendation(user_id)
            print(recommended_movies)
        elif cmd == 'quit':
            if cmd == 'quit' or cmd == 'q':
                print("Good bye!")
                exit(1)
        else:
            print('Sorry you have entered an incorrect command! Try again.\n')

def input_ui():
    print("\nWelcome to the Movie Recommendation System")
    while True:
        option = input("Do you have an account? (yes/no/quit) : ").lower()
        if option == 'yes' or option == 'y':
            attempt = False
            while not attempt:
                attempt = login()
            break
        if option == 'no' or option == 'n':
            while True:
                try:
                    user_id = int(input("Enter a user ID: "))
                except ValueError:
                    print("Error: User ID must be a numerical value")
                    continue
                password = input("Enter a password: ")
                register(user_id, password)
                break
        if option == 'quit' or option == 'q':
            print("Good bye!")
            exit(1)
        else:
            print("Invalid option. Please enter 'yes' or 'no'")

if __name__ == "__main__":
    input_ui()
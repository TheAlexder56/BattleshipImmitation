import random

'''
This function basically defines and then specifics the size and position of the different ships
in both the player's and computer's board using for and while loops to determine the position
using the random library. Then placing them in a matrix.
'''
def generate_ships(board):
    # Define ship types and their sizes, then randomly place them on the board
    ships = {"Gunboat": 2, "Submarine": 3, "Gunship": 4}
    positions = {}
    for ship, size in ships.items():
        while True:
            direction = random.choice(["horizontal", "vertical"])
            if direction == "horizontal":
                row = random.randint(0, 9)
                col = random.randint(0, 9 - size)
                if all(board[row][col + i] == "-" for i in range(size)):
                    for i in range(size):
                        board[row][col + i] = "O"
                    positions[ship] = [(row, col + i) for i in range(size)]
                    break
            else:
                row = random.randint(0, 9 - size)
                col = random.randint(0, 9)
                if all(board[row + i][col] == "-" for i in range(size)):
                    for i in range(size):
                        board[row + i][col] = "O"
                    positions[ship] = [(row + i, col) for i in range(size)]
                    break
    return positions

'''
This function prints the board where the players ships are visible and the computers arent.
'''
def print_board(board, show_ships=False, player_board=True):
    print("   1  2  3  4  5  6  7  8  9 10")
    for i in range(10):
        print(f"{i+1:2d}", end=" ")
        for j in range(10):
            if player_board:
                if show_ships:
                    print(board[i][j], end="  ")
                else:
                    if board[i][j] == "O":
                        print("-", end="  ")
                    else:
                        print(board[i][j], end="  ")
            else:
                if show_ships:
                    if board[i][j] == "O":
                        print("O", end="  ")
                    else:
                        print("-", end="  ")
                else:
                    print(board[i][j], end="  ")
        print()

'''
Play game is the main code in which the computer gives the player an opportunity
to choose where to hit the ships. Using loops whiles and fors to give the unlimited attempts.
It will then print the final scores of each player, and ask it they want to save.
'''
def play_game():
    #Generate ship positions, and start the game loop
    player_board = [["-" for _ in range(10)] for _ in range(10)]
    computer_board = [["-" for _ in range(10)] for _ in range(10)]
    
    #Display player's board and generate ship positions
    print("Player's board:")
    player_positions = generate_ships(player_board)
    print_board(player_board)
    print("------------")
    
    #Display computer's board and generate ship positions
    print("Computer's board:")
    computer_positions = generate_ships(computer_board)
    print_board(computer_board)
    
    player_score = 0
    computer_score = 0

    while True:
        # Player's turn: Take input, check for hit/miss, update scores, and display boards
        while True:
            player_guess = input("Enter your guess (row, col): ").split(",")
            if len(player_guess) == 2:
                break
            else:
                print("Invalid input. Please enter both row and column coordinates separated by a comma.")
        player_row, player_col = int(player_guess[0]) - 1, int(player_guess[1]) - 1
        
        # Check if player hits a ship
        if computer_board[player_row][player_col] == "O":
            print("Hit!")
            computer_board[player_row][player_col] = "X"
            player_score += 10
            for ship, positions in computer_positions.items():
                if (player_row, player_col) in positions:
                    positions.remove((player_row, player_col))
                    if len(positions) == 0:
                        print(f"You sunk the {ship}!")
                        player_score += 15
                        break
        else:
            print("Miss!")
            computer_board[player_row][player_col] = "O"
            player_score += 2
    
        computer_row = random.randint(0, 9)
        computer_col = random.randint(0, 9)
        
        # Check if computer hits a ship
        if player_board[computer_row][computer_col] == "O":
            print("Computer hit your ship!")
            player_board[computer_row][computer_col] = "X"
            computer_score += 10
            for ship, positions in player_positions.items():
                if (computer_row, computer_col) in positions:
                    positions.remove((computer_row, computer_col))
                    if len(positions) == 0:
                        print(f"The computer sunk your {ship}!")
                        computer_score -= 5
                        break
        else:
            print("Computer missed!")
            player_board[computer_row][computer_col] = "O"
            computer_score += 2
        
        # Display updated boards
        print("Your board:")
        print_board(player_board)
        print("------------")
        print("Computer's board:")
        print_board(computer_board)
        
        # Check for game end conditions
        if all(len(positions) == 0 for positions in computer_positions.values()):
            print("Congratulations! You sunk all of the computer's ships!")
            save_score(player_score)
            break
        elif all(len(positions) == 0 for positions in player_positions.values()):
            print("Oh no! The computer sunk all of your ships!")
            save_score(player_score)
            break
    
    # Print the final scores
    print("Your score:", player_score)
    print("Computer's score:", computer_score)
    
'''
Save score will save the scores the program printed before. It will ask the user if it wants to save the socres.
These will then be saved in a .txt file that can then be called back to show what other scores are there.
'''
def save_score(score):
    save = input("Would you like to save your score? (yes/no): ").lower()
    if save == "yes":
        with open("scores.txt", "a") as file:
            file.write(str(score) + "\n")
            print("Score saved successfully!")
    else:
        print("Score not saved.")

# This function only reads the previous scores the file has
def previous_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            if scores:
                print("Previous Scores:")
                for score in scores:
                    print(score.strip())
            else:
                print("No previous scores.")
    file.close()

'''
This function will read the game instructions that are found in another text file.
'''
def game_instructions():
    with open("rulesofgame.txt", "r") as file:
        print(file.read())

def menu():
    print("MENU")
    print("1. Play Game")
    print("2. Game Instructions")
    print("3. Previous Scores")
    print("4. Exit")

def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            play_game()
        elif choice == "2":
            game_instructions()
        elif choice == "3":
            previous_scores()
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

main()

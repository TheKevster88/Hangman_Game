from dearpygui import dearpygui as dpg
import time
from random import randrange
import random, requests

game_word = ''
letter_attempts = []
correct_letters = []

def main_menu():
    with dpg.window(label="Main Menu",tag="Main Menu", width=700,height=600):
        dpg.add_text("hangman game main menu")
        dpg.add_text("\n\n")
        dpg.add_text("How do you want the word to be selected?")
        dpg.add_listbox(['Type in manually','Pick Random from imported list','Python Word Generator'],tag="word_input_type",width=250)
        dpg.add_input_text(label="Word input (Type in word for game or file name based on above selection)",tag="word_input",width=100)
        dpg.add_button(label="process input name and types",callback=input_text_processing)
        dpg.add_text("\n\n")
        dpg.add_button(label="Start new game",callback=start_game)

def input_text_processing():
    global game_word
    input_text = dpg.get_value("word_input")
    input_type = dpg.get_value("word_input_type")
    
    if input_type == 'Type in manually':
        game_word = input_text
        game_word = str(game_word).lower()
    elif input_type == 'Pick Random from imported list':
        print("Attempting to import file now...")
        ImportFilename = input_text
        ImportFilename = ImportFilename + ".txt"
        try:
            with open(ImportFilename, "r") as file:
                print("file opened successfully.")
                word_list = []
                for line in file:
                    word_list.append(line.rstrip())
            game_word = word_list[randrange(len(word_list))]
            game_word = str(game_word).lower()
        except IOError:
            print("Error: File does not appear to exist.")
            game_word = ''
    elif input_type == 'Python Word Generator':
        print("grabbing random word")
        try:
            response = requests.get("https://www.mit.edu/~ecprice/wordlist.10000")
            word_list = response.content.splitlines()
            game_word = (random.choice(word_list)).decode('utf-8')
            game_word = str(game_word).lower()
        except:
            print("error getting request, most likely due to no internet connection.")
            game_word = ''

    return game_word

def start_game():
    global game_word
    input_text_processing()
    if game_word == 'blank' or game_word == '':
        print("default word is still in place, skipping start game function")
    else:
        #logic for resetting game statistics...
        global total_attempts, wrong_attempts, attempts_left, display_word, game_word_breakdown
        total_attempts = 0
        wrong_attempts = 0
        attempts_left = 6
        display_word = ""
        game_word_breakdown = list(game_word)
        for item in game_word_breakdown:
            display_word = display_word + "_ "

        if dpg.does_item_exist("Hangman Game"):
            reset_stats()
            dpg.show_item("Hangman Game")
        else:
            with dpg.window(label="Hangman Game instance",tag="Hangman Game",width=650,height=650):
                dpg.add_text("letters attempted: " + str(letter_attempts),tag="letters_attempted")
                dpg.add_text("Attempts Left: " + str(attempts_left),tag="attempts_left")
                dpg.add_text("\n")
                dpg.add_text("_____\n|   |\n|\n|\n|\n--------",tag="hangman_figure")
                dpg.add_text("\n\n")
                #dpg.add_text("Word (will be updated later, this is placeholder for testing): " + game_word,tag="demowordshow")
                dpg.add_text(display_word,tag="display_word")
                dpg.add_text("\n\n")
                dpg.add_input_text(label="Input letter",tag="Game_letter_input")
                dpg.add_button(label="Submit Guess",callback=letter_guess)
                

def reset_stats():
    global total_attempts, wrong_attempts, attempts_left, display_word, letter_attempts, correct_letters
    print("resetting stats in game...")
    letter_attempts = []
    correct_letters = []
    dpg.set_value("letters_attempted","letters attempted: " + str(letter_attempts))
    dpg.set_value("attempts_left","Attempts Left: " + str(attempts_left))
    dpg.set_value("hangman_figure","_____\n|   |\n|\n|\n|\n--------")
    dpg.set_value("display_word",display_word)
    #dpg.set_value("demowordshow","Word (will be updated later, this is placeholder for testing): " + game_word)

def update_stats():
    global total_attempts, wrong_attempts, attempts_left, display_word, correct_letters, game_word_breakdown
    display_word = ''
    for item in game_word_breakdown:
        if item in correct_letters:
            display_word = display_word + item + " "
        else:
            display_word = display_word + "_ "
    print("updating stats in game...")
    dpg.set_value("letters_attempted","letters attempted: " + str(letter_attempts))
    dpg.set_value("attempts_left","Attempts Left: " + str(attempts_left))
    dpg.set_value("display_word",display_word)
    if wrong_attempts == 0:
        dpg.set_value("hangman_figure","_____\n|   |\n|\n|\n|\n--------")
    if wrong_attempts == 1:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|\n|\n--------")
    if wrong_attempts == 2:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|   | \n|\n--------")
    if wrong_attempts == 3:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|  -| \n|\n--------")
    if wrong_attempts == 4:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|  -|-\n|\n--------")
    if wrong_attempts == 5:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|  -|-\n|  /\n--------")
    
    if wrong_attempts == 6 or attempts_left == 0:
        dpg.set_value("hangman_figure","_____\n|   |\n|   O\n|  -|-\n|  / \ \n--------")
        time.sleep(1)
        game_over()
    correct_word = ''
    for item in game_word_breakdown:
        correct_word = correct_word + item + " "
    
    if display_word == correct_word:
        game_win()

def letter_guess():
    global game_word, letter_attempts,correct_letters
    global total_attempts, wrong_attempts, attempts_left, display_word
    print("something here...")
    game_letter_input = dpg.get_value("Game_letter_input")
    game_letter_input = str(game_letter_input).lower()
    #if len(list(game_letter_input)) > 1:
    #    print("Please input just one character, skipping guess function...")
    #    return
    game_letter_input = list(str(game_letter_input))
    for item in game_letter_input:
        print(item)
        if item in letter_attempts:
            print("this letter has already been attempted, skipping guess function...")
            continue
        total_attempts +=1
        game_word_list = list(game_word)
        #print(game_word_list) - used to print the list of all letters in the current game word...
        if item in game_word_list:
            print(item + " is a correct input!")
            correct_letters.append(item)
        else:
            print(item + " is not a correct letter in the word")
            wrong_attempts+=1
            attempts_left-=1
        letter_attempts.append(item)
        update_stats()

def game_over():
    global game_word
    dpg.hide_item("Hangman Game")
    if dpg.does_item_exist("Game_Over"):
        dpg.set_value("finish_gameword_lose","The word was: "+ str(game_word).lower())
        dpg.show_item("Game_Over")
    else:
        with dpg.window(label="Game Over!",tag="Game_Over",width=200,height=200):
            dpg.add_text("Game Over!")
            dpg.add_text("The word was: "+ str(game_word).lower(), tag="finish_gameword_lose")
            dpg.add_button(label="Accept",callback=reset_to_main_menu)

def game_win():
    global game_word
    dpg.hide_item("Hangman Game")
    if dpg.does_item_exist("Game_Win"):
        dpg.set_value("finish_gameword_win","The word was: "+ str(game_word).lower())
        dpg.show_item("Game_Win")
        
    else:
        with dpg.window(label="You Win!",tag="Game_Win",width=200,height=200):
            dpg.add_text("You Win!")
            dpg.add_text("The word was: "+ str(game_word).lower(),tag="finish_gameword_win")
            dpg.add_button(label="Accept",callback=reset_to_main_menu)

def reset_to_main_menu():
    try:
        dpg.hide_item("Game_Over")
    except:
        pass
    try:
        dpg.hide_item("Game_Win")
    except:
        pass
    dpg.show_item("Main Menu")

if __name__ == '__main__':
    print("do thing here...")
    dpg.create_context()
    dpg.create_viewport()
    dpg.setup_dearpygui()

    
    main_menu()

    #this goes at the very end of the script
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

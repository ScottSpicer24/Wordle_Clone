from flask import Flask, redirect, render_template, request, session
import re, linecache, random

app = Flask(__name__)

# global variables used in all letter amounts
amnt_guesses = 0
real_word = ""
guess = [""] * 6
guess_code = [[0]*9 for i in range(9)]
letter_amnt = 0
guesses_left = 6 - amnt_guesses
rounds_survived = 0

# dictionary of letters and their code used for printing the correct color
letters = {
    'a' : 3,
    'b' : 3,
    'c' : 3,
    'd' : 3,
    'e' : 3,
    'f' : 3,
    'g' : 3,
    'h' : 3,
    'i' : 3,
    'j' : 3,
    'k' : 3,
    'l' : 3,
    'm' : 3,
    'n' : 3,
    'o' : 3,
    'p' : 3,
    'q' : 3,
    'r' : 3,
    's' : 3,
    't' : 3,
    'u' : 3,
    'v' : 3,
    'w' : 3,
    'x' : 3,
    'y' : 3,
    'z' : 3,
}

@app.route('/')
def index():
    return render_template("selection.html") #send them to select their letter amount

@app.route("/selection", methods=["GET", "POST"])
def selection():
    if(request.method == "POST"):
        global letter_amnt #letter amount they choose stored globally 
        global guesses_left 
        guesses_left = 6 - amnt_guesses #initlize the amount of guesses they have
        #get their selection and set the letter amount to that amount
        from_form = request.form.get("letter_amnt").strip()
        if(from_form == "3"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "4"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "5"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "6"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "7"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "8"):
            letter_amnt = int(from_form)
            return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        elif(from_form == "Guantlet"):
            letter_amnt = 3
            global rounds_survived
            rounds_survived = 0
            return render_template("gauntlet_info.html")
        else:
            return render_template("selection.html")
    else:
        #if method is GET
        return render_template("selection.html")

#page used to tell the rules of guantlet mode 
@app.route("/gaun_info", methods=["GET", "POST"])
def gaun_info():
    if(request.method == "POST"):
        global letter_amnt
        if(request.form.get("start") == "start"): # when they start run the gauntlet function and page
            letter_amnt = 3
            return render_template("gauntlet.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left, rounds_survived=rounds_survived)
    else:
        return render_template("guantlet_info.html")

@app.route("/gauntlet", methods=["GET", "POST"])
def gauntlet():
    if(request.method == "POST"):
        # globals used
        global amnt_guesses 
        global guess
        global guesses_left
        global rounds_survived
        global letter_amnt
        # if there are no guesses choose a word
        if(amnt_guesses == 0):
            choose_word(letter_amnt)
        # score used to check if they getthe word correctly
        round_score = 0
        # get their guess
        from_form = request.form.get("guess").lower().strip()
        # make sure they have the correct chars and amount of letters
        match = re.fullmatch(rf'^[a-z]{{{letter_amnt}}}$', from_form)
        if match: # if they do put it in the guess array
            guess[amnt_guesses] = from_form
        else: # if not reload the page
            return render_template("gauntlet.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left, rounds_survived=rounds_survived)
        # check the guess to see if it is correct
        round_score = checker(letter_amnt)
        # if they have a 2 for every letter they are correct
        if(round_score == (letter_amnt * 2)):
            # if they are not at 8 letters itterate to next letter and reset everything else and add 1 to rounds survived
            if(letter_amnt < 8):
                temp = letter_amnt
                reset(letter_amnt)
                letter_amnt = temp + 1
                rounds_survived += 1
                return render_template("gauntlet.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left, rounds_survived=rounds_survived)
            else:
                #if they are at 8 letters they win so render the success page
                rounds_survived += 1
                reset(letter_amnt)
                return render_template("success.html", real_word=real_word)
        else:
            # if the guess is wrong add one to the amount of guesses and remove 1 from guessees left
            amnt_guesses += 1
            guesses_left = 6 - amnt_guesses
            # if amnt of guessis is over the limit they lose
            if(amnt_guesses >= 6):
                reset(letter_amnt)
                return render_template("game_over_g.html", real_word=real_word, rounds_survived=rounds_survived)            
            else: 
                # else give them another guess
                return render_template("gauntlet.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left, rounds_survived=rounds_survived)
    else:
        # if method is post render the gauntlet page
        guesses_left = 6 - amnt_guesses
        return render_template("gauntlet.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left, rounds_survived=rounds_survived)

# if they are doing a letter amount a single time.
# It is the same as the gauntlet code but renders diffrent pages if they succeeds or fail 
@app.route("/wordle", methods=["GET", "POST"])
def wordle():
    if(request.method == "POST" ):
        global amnt_guesses 
        global guess
        global guesses_left
        if(amnt_guesses == 0):
            choose_word(letter_amnt)
        round_score = 0
        from_form = request.form.get("guess").lower().strip()
        match = re.fullmatch(rf'^[a-z]{{{letter_amnt}}}$', from_form)
        if match:
            guess[amnt_guesses] = from_form
        else:
            return render_template("wordle.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
        round_score = checker(letter_amnt)
        if(round_score == (letter_amnt * 2)):
            reset(letter_amnt)
            return render_template("success.html", real_word=real_word)
        else:
            amnt_guesses += 1
            guesses_left = 6 - amnt_guesses
            if(amnt_guesses >= 6):
                reset(letter_amnt)
                return render_template("game_over.html", real_word=real_word)            
            else: 
                return render_template("wordle.html", guess=guess, guess_code=guess_code, letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)
    else:
        guesses_left = 6 - amnt_guesses
        return render_template("wordle.html", letters=letters, letter_amnt=letter_amnt, guesses_left=guesses_left)

# checks if the word is correct   
def checker(len):
    global guess_code
    global amnt_guesses
    global letters
    score = 0 
    for j in range(len):
        if(real_word[j] == guess[amnt_guesses][j]): # letter in correct spot assign that spot and letter the correct color  
            guess_code[amnt_guesses][j] = 2
            score += 2
            letters[guess[amnt_guesses][j]] = 2
        elif(guess[amnt_guesses][j] in real_word): # letter in wrong spot but is in word assign that spot and letter the correct color 
            guess_code[amnt_guesses][j] = 1
            letters[guess[amnt_guesses][j]] = 1
        else:                                      # letter not in word
            guess_code[amnt_guesses][j] = 0
            letters[guess[amnt_guesses][j]] = 0  
    return score

# change all globals to default value
def reset(len): 
    global guess
    global guess_code
    global amnt_guesses
    global letters
    global letter_amnt
    letter_amnt = 0
    amnt_guesses = 0
    for i in range(len):
        for j in range(len):
            guess_code[i][j] = 0
    guess = [""] * 6
    for key, value in letters.items():
        letters[key] = 3

# choose the correct txt file, get a rand int, nod it by txt file length, choose word and store it in global variable
def choose_word(len):
    global real_word
    if(len == 5):                                   
        path = "./static/five_letter_words.txt"
        txt_len = 5757
    elif(len == 3):
        path = "./static/three_letter_words.txt"
        txt_len = 39
    elif(len == 4):
        path = "./static/four_letter_words.txt"
        txt_len = 521
    elif(len == 6):
        path = "./static/six_letter_words.txt"
        txt_len = 10539
    elif(len == 8):
        path = "./static/eight_letter_words.txt"
        txt_len = 1000
    else:
        path = "./static/seven_letter_words.txt"
        txt_len = 1371
    choosen_line = random.randint(0, 25000)
    choosen_line %= txt_len
    real_word = linecache.getline(path, choosen_line).strip().lower()

if __name__ == '__main__':
    app.run(debug=True)

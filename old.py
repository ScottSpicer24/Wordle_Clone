from flask import Flask, redirect, render_template, request, session
import re, linecache, random

app = Flask(__name__)

#global variables used in all letter amounts
amnt_guesses = 0
real_word = ""
guess = [""] * 7
guess_code = [[0]*7 for i in range(7)]

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
    return render_template("selection.html")

@app.route("/fiveLetter", methods=["GET", "POST"])
def fiveLetter():
    if(request.method == "POST"):
        global amnt_guesses 
        global guess
        if(amnt_guesses == 0):
            choose_word(5)
        round_score = 0
        from_form = request.form.get("guess").lower().strip()
        match = re.fullmatch(r'^[a-z]{5}$', from_form)
        if match:
            guess[amnt_guesses] = from_form
        else:
            return render_template("fiveLetter.html", guess=guess, guess_code=guess_code, letters=letters)
        round_score = checker(5)
        if(round_score == 10):
            reset(5)
            return render_template("success.html", real_word=real_word)
        else:
            amnt_guesses += 1
            if(amnt_guesses >= 5):
                reset(5)
                return render_template("game_over.html", real_word=real_word)            
            else: 
                return render_template("fiveLetter.html", guess=guess, guess_code=guess_code, letters=letters)
    else:
        return render_template("fiveLetter.html", letters=letters)

@app.route("/sixLetter", methods=["GET", "POST"])
def sixLetter():
    if(request.method == "POST"):
        global amnt_guesses 
        global guess
        if(amnt_guesses == 0):
            choose_word(6)
        round_score = 0
        from_form = request.form.get("guess").lower().strip()
        match = re.fullmatch(r'^[a-z]{6}$', from_form)
        if match:
            guess[amnt_guesses] = from_form
        else:
            return render_template("sixLetter.html", guess=guess, guess_code=guess_code, letters=letters)
        round_score = checker(6)
        if(round_score == 12):
            reset(6)
            return render_template("success.html", real_word=real_word)
        else:
            amnt_guesses += 1
            if(amnt_guesses >= 5):
                reset(6)
                return render_template("game_over.html", real_word=real_word)            
            else: 
                return render_template("sixLetter.html", guess=guess, guess_code=guess_code, letters=letters)
    else:
        return render_template("sixLetter.html", letters=letters)

@app.route("/sevenLetter", methods=["GET", "POST"])
def sevenLetter():
    if(request.method == "POST"):
        global amnt_guesses 
        global guess
        if(amnt_guesses == 0):
            choose_word(7)
        round_score = 0
        from_form = request.form.get("guess").lower().strip()
        match = re.fullmatch(r'^[a-z]{7}$', from_form)
        if match:
            guess[amnt_guesses] = from_form
        else:
            return render_template("sevenLetter.html", guess=guess, guess_code=guess_code, letters=letters)
        round_score = checker(7)
        if(round_score == 14):
            reset(7)
            return render_template("success.html", real_word=real_word)
        else:
            amnt_guesses += 1
            if(amnt_guesses >= 5):
                reset(7)
                return render_template("game_over.html", real_word=real_word)            
            else: 
                return render_template("sevenLetter.html", guess=guess, guess_code=guess_code, letters=letters)
    else:
        return render_template("sevenLetter.html", letters=letters)      

def checker(len):
    #tried to use set notation to optimize time complexity but that has issues with words with the same letters more than once
    global guess_code
    global letters
    score = 0 
    for j in range(len):
        if(real_word[j] == guess[amnt_guesses][j]):   
            guess_code[amnt_guesses][j] = 2
            score += 2
            letters[guess[amnt_guesses][j]] = 2
        elif(guess[amnt_guesses][j] in real_word):
            guess_code[amnt_guesses][j] = 1
            letters[guess[amnt_guesses][j]] = 1
        else:
            guess_code[amnt_guesses][j] = 0
            letters[guess[amnt_guesses][j]] = 0  
    return score

def reset(len):
    global guess
    global guess_code
    global amnt_guesses
    global letters
    amnt_guesses = 0
    for i in range(len):
        guess[i] = ""
        for j in range(len):
            guess_code[i][j] = 0
    for key, value in letters.items():
        letters[key] = 3

def choose_word(len):
    global real_word
    if(len == 5):                                   
        path = "./static/five_letter_words.txt"
        txt_len = 5757
    elif(len == 6):
        path = "./static/six_letter_words.txt"
        txt_len = 10539
    else:
        path = "./static/seven_letter_words.txt"
        txt_len = 1371
    choosen_line = random.randint(0, 25000)
    choosen_line %= txt_len
    real_word = linecache.getline(path, choosen_line).strip().lower()

    

if __name__ == '__main__':
    app.run(debug=True)
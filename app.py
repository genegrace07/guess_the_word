from flask import Flask, render_template,request,session,redirect,url_for
from words import animals
from hangman import hangman_art
import random
from collections import Counter

app = Flask(__name__)
app.secret_key = "my_secretkey"

def hint():
    global chosen
    global chosen_hint
    global first_hint

    chosen = random.choice(animals)

    letter_counts = Counter(chosen)
    eligible_letter = [n for n,letter in enumerate(chosen) if letter_counts[letter] == 1]

    if len(chosen) <= 3:
        hints = random.sample(eligible_letter, 1)
        chosen_hint = "_" * len(chosen)
        chosen_hint = list(chosen_hint)

        for h in hints:
            chosen_hint[h] = chosen[h]
        first_hint = " ".join(chosen_hint)

        return first_hint

    else:
        hints = random.sample(eligible_letter, 2)
        chosen_hint = "_" * len(chosen)
        chosen_hint = list(chosen_hint)

        for h in hints:
            chosen_hint[h] = chosen[h]
        first_hint = " ".join(chosen_hint)

        return first_hint
def wrong_guesses():
    return hangman_art

hint()

@app.route('/', methods=['GET','POST'])
def main():
    user_guesses = wrong_guesses() #dict
    letters_count = len(chosen)

    correct_messages = ["Very good!","Well done!","Excellent!","Great job!","Correct! Keep it up!","Amazing!","You got it!","Fantastic!","Brilliant guess!","You're doing great!","Nice one!","Keep up the good work!"]
    incorrect_messages = ["Oops! Wrong guess!","Not quite!","Try another letter!","Better luck next time!","Oh no! That's incorrect!","Wrong letter! Keep trying!","Don't give up!","Almost there!","Unfortunately, that's not correct!","Keep guessing!","Careful! One mistake closer to Hangman!","You can do better!"]
    random_correct_msg = random.choice(correct_messages)
    random_incorrect_msg = random.choice(incorrect_messages)

    if 'hint_update' not in session:
        session['hint_update'] = chosen_hint.copy()

    session_hints = session['hint_update']

    if 'wrong_counts' not in session:
        session['wrong_counts'] = 0

    display_hangman = user_guesses.get(session['wrong_counts'],"")

    if request.method == 'POST':
        user_guess = request.form.get("answer")

        if user_guess not in chosen:

            session['wrong_counts'] += 1
            display_hangman = user_guesses[session['wrong_counts']]
            wrong_answer = random_incorrect_msg
            update_hint = " ".join(chosen_hint)

            if session['wrong_counts'] == 7:
                game_over = "GAME OVER!!! Better luck next time"
                correct_answer = f"{chosen} is the correct answer"
                return render_template('main.html',correct_answer=correct_answer,user_guess=user_guess,display_hint = update_hint,game_over=game_over,display_hangman = display_hangman,letters_count=letters_count)

            return render_template('main.html',user_guess=user_guess,display_hangman = display_hangman,display_hint = update_hint, wrong_answer=wrong_answer,letters_count=letters_count)

        if user_guess in first_hint:
            already_guessed = f'"{user_guess}" already on hint'
            display_hint = " ".join(chosen_hint)
            return render_template('main.html',user_guess=user_guess,already_guessed=already_guessed,display_hint=display_hint,display_hangman=display_hangman, letters_count=letters_count)

        if user_guess in session_hints:
            already_guessed = f'"{user_guess}" already answered'
            display_hint = " ".join(chosen_hint)
            return render_template('main.html',user_guess=user_guess,already_guessed=already_guessed,display_hint=display_hint,display_hangman=display_hangman, letters_count=letters_count)
        if user_guess in chosen:

            for idx, letter in enumerate(chosen):
                if letter == user_guess:
                    chosen_hint[idx] = user_guess
                    display_hint = " ".join(chosen_hint)
                    completed_guess = "".join(chosen_hint)

                    if completed_guess == chosen:

                        session['hint_update']=[]

                        complete = 'Congratulations!!! Very good, Well done'
                        return render_template('main.html',user_guess=user_guess,display_hint=display_hint, complete=complete,display_hangman = display_hangman,letters_count=letters_count)

            session['hint_update'] = chosen_hint

            right_ans = random_correct_msg
            return render_template('main.html',user_guess=user_guess,display_hint = display_hint,right_ans=right_ans,display_hangman = display_hangman,letters_count=letters_count)

    return render_template('main.html',display_hint = first_hint,display_hangman=display_hangman,letters_count=letters_count)

@app.route('/reset')
def reset():
    hint()
    session['wrong_counts'] = 0
    session['hint_update'] = []
    return redirect(url_for('main'))

@app.route('/tryagain')
def tryagain():
    hint()
    session['wrong_counts'] = 0
    session['hint_update'] = []
    return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)


'''
NOTE: #not reading user guess session after already input and not appending to session
      #condition for if user guess already in hint, and updated hint
      #after guessing correct answer and already in hint, hint display is not updated
      #remove change button after 1 guess to avoid cheating/skipping 
      #remove input box and submit button if the game is finished or game over
      #create a list of welcome message if correct and wrong answer, random it
      #display correct answer if game over
'''
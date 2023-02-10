import time, tkinter as tk, sys, speech_recognition as sr

from qg import quizGen

from ai import *


def exit():
    global RUNNING
    if RUNNING:
        RUNNING = False
    sys.exit()

def check_events(event):
    global RUNNING
    global PAUSED

    if event.keysym == "Escape":
        RUNNING = False
        
    if event.keysym == "space":
        if not PAUSED:
            PAUSED = True
        else:
            PAUSED = False

def start():
    # Hides the start button
    start_btn.pack_forget()

    # Disables interacting with the options menu
    menubar.entryconfig("Options", state = "disabled")

    global RUNNING
    global PAUSED

    RUNNING = True
    while RUNNING:
        # Obtains a random quiz set from database
        quiz = quizGen()

        if x.get() == 1:
            _run_online_mode(quiz)
        elif x.get() == 2:
            _run_offline_mode(quiz)

    # Recover the start button
    start_btn.pack()
    
    menubar.entryconfig("Options", state = "normal")

def _run_offline_mode(quiz):
    _ask_question(quiz)
    time.sleep(5)

    QA.set(quiz.answer)
    window.update()
    agent.say(f"The correct answer is {quiz.voice_answer()}")
    time.sleep(2)

    QA.set("")
    window.update()

def _run_online_mode(quiz):
    _ask_question(quiz)

    # Initializing the recognizer
    voiceEng = sr.Recognizer()

    rightAnswer = quiz.voice_answer()

    try:
        # Allows voice input through the microphone
        with sr.Microphone() as source:
            voiceEng.adjust_for_ambient_noise(source, duration=0.2)
            print("speak: ")

            # Listens to user input audio
            audio = voiceEng.listen(source)

            # Translates audio to text using google
            output_text = voiceEng.recognize_google(audio)

            QA.set(quiz.answer)
            window.update()

            if _is_accurate_answer(output_text, rightAnswer):
                agent.say(f"That is correct. The answer is {rightAnswer}")
            else:
                agent.say(f"That is incorrect. The right answer is {rightAnswer}")
            time.sleep(2)

            QA.set("")
            window.update()

    except sr.RequestError or ConnectionResetError or sr.RequestError as e:
            agent.say("There seem to be a very bad internet connection")
            agent.say("Reverting to offline mode")
            print("Reverted to offline mode")
            x.set(2)
    except sr.UnknownValueError:
        QA.set(quiz.answer)
        window.update()
        agent.say(f"The correct answer is {rightAnswer}")
        agent.say("Please speak clearly into your microphone")
        QA.set("")
        window.update()

def _is_accurate_answer(output_text, answer):
    correct_words = 0
    words = answer.split()
    for word in words:
        if word in output_text:
            correct_words += 1
    if correct_words/len(words) >= 0.8:
        return True

def _ask_question(quiz):
    # Display and voice quiz question on screen
    QA.set(f"{quiz.id}. {quiz.question}")
    window.update() 
    agent.say(quiz.id)
    agent.say(quiz.voice_question())

def darkTheme():
    window.config(bg = "black")
    face_lbl.config(bg = "black")
    quiz_lbl.config(bg = "black", fg = "white")

def lightTheme():
    window.config(bg = "white")
    face_lbl.config(bg = "white")
    quiz_lbl.config(bg = "white", fg = "black")

def Butler():
    agent.name  = "Butler"
    agent.voice = MALE
    agent.intro()

def Alberta():
    agent.name  = "Alberta"
    agent.voice = FEMALE
    agent.intro()

def mode():
    if x.get() == 1:
        print("Online mode")
    if x.get() == 2:
        print("Offline  mode")


RUNNING = False
PAUSED = False

window = tk.Tk()
x = tk.IntVar()
x.set(1)

# images
logo_img = tk.PhotoImage(file = "images/pbicon.png")
face_img = tk.PhotoImage(file = "images/face.png")

# window dimension
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

# Menus
menubar = tk.Menu()
options_menu = tk.Menu(menubar, tearoff = 0)
theme_menu = tk.Menu(menubar, tearoff = 0)
voice_menu = tk.Menu(options_menu, tearoff = 0)
mode_menu = tk.Menu(options_menu, tearoff = 0)

menubar.add_cascade(label = "Options", menu = options_menu)

# Contents of options menu
options_menu.add_cascade(label = "Theme", menu = theme_menu)
options_menu.add_cascade(label = "Agent", menu = voice_menu)
options_menu.add_separator()
options_menu.add_cascade(label = "Mode", menu = mode_menu)

# Contents of mode menu
mode_menu.add_radiobutton(label = "online", value = 1, variable = x, command = mode)
mode_menu.add_radiobutton(label = "offline", value = 2, variable = x , command = mode)

# Contents of theme menu
theme_menu.add_command(label = "Light", command = lightTheme)
theme_menu.add_command(label = "Dark", command = darkTheme)

# Contents of voice menu
voice_menu.add_command(label = "Butler", command = Butler)
voice_menu.add_command(label = "Alberta", command = Alberta)

# Window features
window.geometry(f"{screen_width}x{screen_height}")
window.state("zoomed")
window.title("Petrobowl Trivia")
window.iconphoto(True, logo_img)
window.config(bg = "white", cursor = "arrow", menu = menubar)

# Events
window.bind("<Key>", check_events)
window.protocol("WM_DELETE_WINDOW", exit) # Calls exit function when window is closed (ie clicking "X")

QA = tk.StringVar()

# Agent
agent = DEFAULT
face_lbl = tk.Label(window, bg = "white", image = face_img)
face_lbl.pack()

# Quiz label
quiz_lbl = tk.Label(window, textvariable = QA, 
font = ("Arial", 25),bg = "white",fg = "black",
justify = "center", wraplength = 1000
)
quiz_lbl.pack(pady = 10)
"""Wraplength creats a space beyond which new words would jump to next line"""
"""justify = align; (left, right, or center)"""

# Start button
start_btn = tk.Button(window, text = "START", font = ("Arial"),
command = start, border = 1,bg = "#00b1ff", fg = "black",
borderwidth = 3, relief = "raised", height = 2, width = 10,
activebackground = "gold"
)
start_btn.pack(pady = 5)

window.update()
agent.intro()
"""window.update() is called before agent.intro() to allow the agent to
introduce itself after the window is displayed"""

window.mainloop()
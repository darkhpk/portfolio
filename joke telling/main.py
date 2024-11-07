#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import time, sys


def nJokes():
    jquestion = [
        "What do dentists call their x-rays?",
        "What�s the difference between a hippo and a zippo?",
        "How do you measure a snake?",
        "Where does a waitress with only one leg work?"
    ]
    janswer = [
        "Tooth pics!",
        "One is really heavy and the other�s a little lighter.",
        "IHOP."
    ]
    jokes = zip(jquestion, janswer)
    while True:
        for j in jokes:
            print(j[0])
            time.sleep(1)
            print(j[1])
            time.sleep(1.5)

        print("Do you wanna hear them again?[y/n]")
        answ = input()

        if answ.lower() == "y":
            continue
        elif answ.lower() == "n":
            sys.exit()

def hJokes():
    print("I really wanted to put any, but someone told me it's inappropriate!")

def mJokes():
    print("I really wanted to put any, but someone told me it's inappropriate!")

def rJokes():
    print("I really wanted to put any, but someone told me it's inappropriate!")


def switch(value, cond1, cond2, cond3, cond4, cond5):
    if value == cond1:
        nJokes()
    elif value == cond2:
        hJokes()
    elif value == cond3:
        mJokes()
    elif value == cond4:
        rJokes()
    elif value == cond5:
        sys.exit()

print("""

|=======================================|
|      Choose your type of jokes!       |
|                                       |
|      1. Normal Jokes (boring!!)       |
|      2. Homophobic Jokes              |
|      3. Mysoginistic Jokes            |
|      4. Racist Jokes                  |
|      Q. Quit (Like a loser!)          |
|                                       |
|=======================================|
""")

while True:
    print("Your Choice?")
    choice = input()

    if choice == "1":
        nJokes()
    elif choice == "2":
        hJokes()
    elif choice == "3":
        mJokes()
    elif choice == "4":
        rJokes()
    elif choice.lower() == "q":
        sys.exit()
    else:
        print("The option is not valid, try again!")
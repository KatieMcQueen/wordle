import random as rand

words = []
answers = []
guesses = []
goalWord = ''
state = 'generator'
tries = 0
cheats = False

helpText = '''Exit: end the program
New: generate a new word
Peek: print the hidden word
Poke: set the hidden word
cheatson: turns cheat mode on
cheatsoff: turns cheat mode off
cheats: toggles cheats mode
Help: print this text'''

with open('answers.txt') as file:
    for line in file:
        answers.append(line.strip())

with open('guesses.txt') as file:
    for line in file:
        guesses.append(line.strip())

words = answers + guesses

def assessGuess(guess):
    results = [None] * 5
    dupes = []
    for i in range(len(guess)):
        letterGuess = guess[i]
        letterGoal = goalWord[i]
        count = guess.count(letterGuess)
        if letterGuess == letterGoal:
            results[i] = 'correct'
            if count > 0:
                letterIndex = None
                for index in range(len(dupes)):
                    if dupes[index][0] == letterGuess:
                        letterIndex = index
                if letterIndex == None:
                    letterIndex = len(dupes)
                    dupes.append([letterGuess, count - 1])
                dupes[letterIndex][1] -= 1

        elif letterGuess in goalWord:
            if count == 1:
                results[i] = 'place'
            else:
                letterIndex = None
                for index in range(len(dupes)):
                    if dupes[index][0] == letterGuess:
                        letterIndex = index
                if letterIndex == None:
                    letterIndex = len(dupes)
                    dupes.append([letterGuess, count - 1])
                if dupes[letterIndex][1] == 0:
                    results[i] = 'wrong'
                if dupes[letterIndex][1] > 0:
                    results[i] = 'place'
                    dupes[letterIndex][1] -= 1



        else:
            results[i] = 'wrong'

    return(results)



def printResult(result, command):
    resultString = ''
    for i in range(5):
        match result[i]:
            case 'correct':
                resultString += '\x1b[2;30;42m' + command[i] + '\033[0;0m'
            case 'place':
                resultString += '\x1b[2;30;43m' + command[i] + '\033[0;0m'
            case 'wrong':
                resultString += '\x1b[2;30;47m' + command[i] + '\033[0;0m'

    resultString += ' ' + str(tries) + '/6'
    resultString += '\n'
    print(resultString)



while(state != 'end'):
    goalWord = rand.choice(answers)
    correct = False
    tries = 0
    state = 'guess'
    while(state == 'guess'):
        command = input("Enter a word or comand: ")
        match len(command):
            case 5:
                if command == goalWord:
                    print('Correct!')
                    state = 'generator'
                    correct = True
                if command in words or cheats:
                    tries += 1
                    result = assessGuess(command)
                    printResult(result, command)
                else:
                    print("word not in dictionary")
                if tries == 6 and not correct:
                    print("You lost. Try again.")
                    print("The word was: \x1b[2;30;41m" + goalWord + '\033[0;0m')
                    state = 'generator'
            case _:
                match command: #when the input isn't 5 letters interpret it as a command
                    case 'exit' | 'end':
                        state = 'end'
                    case 'new':
                        state = 'generator'
                    case 'peek':
                        print(goalWord)
                    case 'poke':
                        newWord = input("Enter a new word: ")
                        if len(newWord) == 5:
                            goalWord = newWord
                        else:
                            print("Wrong length")
                    case 'cheatson':
                        cheats = True
                        print("Cheats on")
                    case 'cheatsoff':
                        cheats = False
                        print("Cheats off")
                    case 'cheats':
                        if cheats:
                            cheats = False
                            print("Cheats off")
                        elif not cheats:
                            cheats = True
                            print("Cheats on")
                    case 'help':
                        print(helpText)

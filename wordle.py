import random as rand

words = []
answers = []
guesses = []
goalWord = ''
state = 'generator'
tries = 0

helpText = '''Exit: end the program
New: generate a new word
Peek: print the hidden word
Poke: set the hidden word
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
    for i in range(len(guess)):
        letterGuess = guess[i]
        letterGoal = goalWord[i]
        count = guess.count(letterGuess)
        if letterGuess == letterGoal:
            results[i] = 'correct'
        elif letterGuess in goalWord:
            results[i] = 'place'
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
                tries += 1
                result = assessGuess(command)
                printResult(result, command)
                if tries == 6 and not correct:
                    print("You lost. Try again.")
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
                    case 'help':
                        print(helpText)

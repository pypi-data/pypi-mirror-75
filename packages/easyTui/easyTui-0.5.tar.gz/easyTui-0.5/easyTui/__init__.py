import time
import os

#os.system("mode con cols=width lines=height")
#os.system('color 0A')  0 - BACKGROUND, A - TEXT
#
#   COLORS
#
# 0 = BLACK     8 = GRAY
# 1 = BLUE      9 = BRIGHT-BLUE
# 2 = GREEN     A = BRIGHT-GREEN
# 3 = CYAN      B = BRIGHT-CYAN
# 4 = RED       C = BRIGHT-RED
# 5 = PURPLE    D = BRIGHT-PURPLE
# 6 = YELLOW    E = BRIGHT-YELLOW
# 7 = WHITE     F = BRIGHT-WHITE
#

def title(title):
    length = len(title) + 6
    titlestr = '=' * length + '\n-- ' + title + ' --\n' + '=' * length
    return titlestr

def label(label):
    length = len(label) + 6
    labelstr = '\n ' + label + '\n' + '-' * length + '\n'
    return labelstr

def score(name, score):
    length = len(name) + len(str(score)) + 10
    scorestr = name + ': ' + str(score) + '  \n' + '-' * length
    return scorestr

def updScore (name, score, freq):
    updscorestr = name + ': ' + str(score) + '\r'
    time.sleep(freq)
    return updscorestr
    
def ul(options):
    ulstr = ''
    for i in options:
        ulstr += '  -' + i + '\n'
    ulstr += '-' * 24
    return ulstr

def ol(options):
    olstr = ''
    num = 0
    for i in options:
        olstr += '  [' + str(num) + ']' + i + '\n'
        num += 1
    olstr += '-' * 24
    return olstr

import string
import time
import os
import csv

files = os.listdir('logs')

letters = {}
words = {}
am = {12: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}
pm = {12: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0}

current_time = 0
meridiem = 0

for txt in files:
    inputfile = open('logs/' + txt)
    for line in inputfile:
        lower_line = line.lower()
        splitline = lower_line.split()
        if "[3/" in line:
            current_time = time.strptime(splitline[1], "%H:%M:%S")
            if "am" in splitline[2]:
                meridiem = 0
            else:
                meridiem = 1
        elif "[4/" in line:
            current_time = time.strptime(splitline[1], "%H:%M:%S")
            if "am" in splitline[2]:
                meridiem = 0
            else:
                meridiem = 1
        else:
            for char in lower_line:
                if meridiem is 0:
                    am[current_time.tm_hour] += 1
                else:
                    pm[current_time.tm_hour] += 1
            for word in splitline:
                #if len(word) >= 4:
                    if word not in words:
                        words[word] = 1
                    else:
                        words[word] += 1
            for char in lower_line:
                if char not in letters:
                    letters[char] = 1
                else:
                    letters[char] += 1

#print am
#print pm

writer = csv.writer(open('gathered_data/am.csv', 'wb'))
for key, value in am.items():
    writer.writerow([key, value])
writer2 = csv.writer(open('gathered_data/pm.csv', 'wb'))
for key, value in pm.items():
    writer2.writerow([key, value])
    
ordered_words = sorted(words.items(), key=lambda x:x[1])
writer3 = csv.writer(open('gathered_data/words.csv', 'wb'))
it = reversed(ordered_words)
for x in range(0, 100):
    the_word = it.next()
    writer3.writerow([the_word[0], the_word[1]])

ordered_tuples = sorted(letters.items(), key=lambda x:x[1])
writer4 = csv.writer(open('gathered_data/letters.csv', 'wb'))
it = reversed(ordered_tuples)
for x in range(0, 15):
    the_letter = it.next()
    writer4.writerow([the_letter[0], the_letter[1]])

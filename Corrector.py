import re
reg = re.compile('[^a-zA-Z ]') # преберемо всі не регулярні символи, що залишились з файлу

fileread = open("import.txt", "r")
dictiorary = fileread.readlines()
dictiorary = [i.rstrip() for i in dictiorary]


filereadorigin = open("origin.txt", "r")
OriginText = filereadorigin.read()
OriginText = OriginText.split()
OriginText = [reg.sub('', i) for i in OriginText]

# алгоритм Вагнера про лінгвістичну дистанцію мені він здався простішим)  
def get_levenshtein_distance(word1, word2):
   
    #      ε К О Р А Б Е Л Ь
        #ε 0 1 2 3 4 5 6 7 8   /* тобто відстань між пустим словом і словом КОРАБЕЛЬ = 8 (довжина слова КОРАБЕЛЬ) */
        #Б 1 1 2 3 4 4 5 6 7   /* між Б і КОРАБЕЛЬ відстань = 7 (літера Б в обох словах і може бути використана) */
        #А 2 2 2 3 3 4 5 6 7   /* між БА і КОРАБЕЛЬ відстань = 7 (лише одну з літер Б або А можна використати) */
        #Л 3 3 3 3 4 4 5 5 6   /* між БАЛ і КОРАБЕЛЬ відстань = 6 (можна використати дві літери (Б або А) + Л) */

    word2 = word2.lower()
    word1 = word1.lower()
    matrix = [[0 for x in range(len(word2) + 1)] for x in range(len(word1) + 1)]

    for x in range(len(word1) + 1):
        matrix[x][0] = x
    for y in range(len(word2) + 1):
        matrix[0][y] = y

    for x in range(1, len(word1) + 1):
        for y in range(1, len(word2) + 1):
            if word1[x - 1] == word2[y - 1]: # якщо однакові
                matrix[x][y] = min( # повертае найменьший з аргументів 
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1],
                    matrix[x][y - 1] + 1
                )
            else: 
                matrix[x][y] = min( # повертае найменьший з аргументів 
                    matrix[x - 1][y] + 1,
                    matrix[x - 1][y - 1] + 1, 
                    matrix[x][y - 1] + 1
                )
                
    return matrix[len(word1)][len(word2)] #значення відстані Левенштайна в останній клітинці матриці 

listOfRight =[] #список довгих ісправлених слів 
listOfRightSmall =[] ##список коротких ісправлених слів
listOfUsedWords =[] # список слів що вже були використані
RegularWordsList =[i for i in dictiorary if len(i)<5] # короткі слова а також прислівники які складно індифікувати
RegularWordsList = [reg.sub('', i) for i in RegularWordsList] # приводимо в один вид з OriginText 

for i in OriginText:
   for y in dictiorary:
        if (get_levenshtein_distance( y,i ) > 0 and get_levenshtein_distance(y,i ) <= 2 and len(y)>5 and listOfUsedWords.count(i) < 2 ): #мотод для довгих слів 
            listOfRight.append(y) 
            listOfUsedWords.append(i) 
            print ("\tFound unknown word %s. Suggestions: %s -> %s\n" %(i,i,listOfRight))

        elif(get_levenshtein_distance( y,i ) > 0 and get_levenshtein_distance(y,i ) <= 1 and (len(i) <=5 and len(i) >=3) and listOfUsedWords.count(i) < 2):
            if (i[0]==y[0] and RegularWordsList.count(i) == 0):
                listOfRightSmall.append(y)
                listOfUsedWords.append(i)
                print ("\tFound unknown word %s. Suggestions: %s -> %s\n" %(i,i,listOfRightSmall))

   listOfRight.clear()
   listOfRightSmall.clear()

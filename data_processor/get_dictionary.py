def remove_english(word):
    letters = list(word)
    word = "".join(letters[:-1]) if letters[-1] == "\n" else "".join(letters)
    res = "" if len(set(word.lower()).intersection(set(list("abcdefghijklmnopqrstuvwxyz")))) != 0 else word
    return res


# Calculate the frequency of words and store them in a list
filename = "/temp/sentences.txt"
dictionary = set()
counter = 0

# read file
with open(filename, "r") as file:
    flag = True
    while flag:
        line = file.readline()
        flag = False if line == "" else True
        for word in line.split(" "):
            print(counter)
            counter += 1
            filtered_word = remove_english(word)
            dictionary.add(word)

# writing file
with open("temp/dictionary.txt", "w") as file:
    for word in dictionary:
        file.write(word)
        file.write("\n")

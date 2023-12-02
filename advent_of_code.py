import re


with open(r"C:\Users\AaronWork\Desktop\day1.txt", "r") as f:
    words = [line.strip() for line in f.readlines()]

# words = ["two1nine",
# "eightwothree",
# "abcone2threexyz",
# "xtwone3four",
# "4nineeightseven2",
# "zoneight234",
# "7pqrstsixteen"]

words_map_to_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def mapper(word: str):
    while True:
        indicies = {}
        for number_word in words_map_to_numbers.keys():
            found_index = word.find(number_word)
            if found_index != -1:
                indicies[found_index] = number_word
        if len(indicies) == 0:
            break
        key_to_remove = min(indicies.keys())
        next_number_word = indicies[key_to_remove]
        word = word.replace(next_number_word[:-1], words_map_to_numbers[next_number_word], 1)
        del indicies[key_to_remove]
    return word


all_nums = []


for word in words:
    print(word, end=" -> ")
    word = mapper(word)
    print(word, end=" -> ")

    num = []
    for letter in word:
        if letter.isdecimal():
            num.append(letter)
    print(num)
    all_nums.append(num)

sum = 0

for num in all_nums:
    if len(num) == 1:
        value = int(num[0] + num[0])
        print(value)
        sum += value
    else:
        value = int(num[0] + num[-1])
        print(value)
        sum += value

print(sum)
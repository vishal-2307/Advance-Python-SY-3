import re

sentence = input("Enter a sentence: ")

words = re.findall(r'\b\w+\b', sentence.lower())

repeated = []

for word in words:
    if words.count(word) > 1 and word not in repeated:
        repeated.append(word)

if repeated:
    print("Repeated words are:", repeated)
else:
    print("No repeated words found.")
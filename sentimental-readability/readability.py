letters = 0.0
words = 1.0
sentences = 0

text = str(input("Text: "))

textsize = len(text)

for c in text:
    if c.isalpha():
        letters += 1
    elif c.isspace():
        words += 1
    elif c == '.' or c == '?' or c == '!':
        sentences += 1

L = (letters / words) * 100
S = (sentences / words) * 100

index = (0.0588 * L) - (0.296 * S) - 15.8

if index < 1:
    print("Before Grade 1")
elif 16 >= index >= 1:
    print(f"Grade {index: .0f}")
else:
    print("Grade 16+")

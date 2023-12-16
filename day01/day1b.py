
class IndexValue:
    index = 0
    value = "1"

    
    def __init__(self, index, value):
        self.index = index
        self.value = value
        
    def __str__(self):
        return f"(i:{self.index}, v:{self.value})"
        

class WordNumber:
    word = "one"
    number = "1"
    
    def __init__(self, word, number):
        self.word = word
        self.number = number
        
mappings = [
    WordNumber("one", "1"),
    WordNumber("two", "2"),
    WordNumber("three", "3"),
    WordNumber("four", "4"),
    WordNumber("five", "5"),
    WordNumber("six", "6"),
    WordNumber("seven", "7"),
    WordNumber("eight", "8"),
    WordNumber("nine", "9"),
]

    
with open("test.txt", 'r', encoding="utf8") as file:
    total = 0
    for line in file:
        index_to_chars = {}
        for index, char in enumerate(line):
            if char.isnumeric():
                index_to_chars[index] = char
            
            for mapping in mappings:
                substring = line[index:index+len(mapping.word)]
                if substring == mapping.word:
                    index_to_chars[index] = mapping.number
                    
        print(index_to_chars, line)
        first_index = min(index_to_chars.keys())
        last_index = max(index_to_chars.keys())
        
        number = int(index_to_chars[first_index] + index_to_chars[last_index])
        total += number
        
        
    print(total)
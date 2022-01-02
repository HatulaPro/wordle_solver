import random
from sys import argv

GREEN = '\033[32m'
YELLOW = '\033[33m'
RESET = '\033[0m'

words = set([word.strip() for word in open('./words.txt', 'r').readlines()])

def update_results(word, greens, yellows, blacks, target=None):
	result = ''
	if bool(target):
		for index, char in enumerate(word):
			if char == target[index]:
				result += 'g'
			elif char in target:
				result += 'y'
			else:
				result += 'b'
		print(f'Result: {result}')
	else:
		result = input('Result: ').lower()

	assert len(result) == 5, "Bad length"
	assert 5 == result.count('g') + result.count('y') + result.count('b'), "Only the letters `g`, `y` and `g` are allwed"
	if result == 'ggggg':
		return True
	for index, char in enumerate(word):
		if result[index] == 'g':
			greens.append({'char': char, 'location': index})
		elif result[index] == 'y':
			yellows.append({'char': char, 'location': index})
		elif result[index] == 'b':
			blacks.append(char)
	return False
		

def choose_next(greens, yellows, blacks):
	potential_answers = set()
	for word in list(words):
		if any(char in word for char in blacks):
			continue
		if not any(char in word for char in blacks) and all(yellow['char'] in word and word[yellow['location']] != yellow['char'] for yellow in yellows) and all(word[green['location']] == green['char'] for green in greens):
			potential_answers.add(word)
	return potential_answers

def color_word(word, greens, yellows):
	res = ''
	for index, char in enumerate(word):
		if any(green['location'] == index and char == green['char'] for green in greens):
			res += GREEN
		elif any(yellow['char'] == char and index != yellow['location'] for yellow in yellows):
			res += YELLOW
		else:
			res += RESET
		res += char
		 
	return res + RESET


def main():
	global words
	target = None
	if len(argv) == 3 and argv[1] == '-s':
		target = argv[2].lower()
		assert len(target) == 5, "Bad length"
		assert target.isalpha(), "Only English letters are allowed"
		print(f'Started simulation with word {target}...\n')
	elif len(argv) != 1:
		print('This program is used to solve wordle challenges (finding a 5 characters word based on clues)\n\nUsage:\n  Standard mode: python main.py\n    - At this point the program will ask for clues\n    - Use `g` for green guesses, `y` for yellow guesses and `b` for black guesses.\n    - Example: when guessing `grows` and the target is `boost`, you\'ll have to input `bbgby`\n  Simulation mode: python main.py -s <target>\n    - The program will show its solution for that given target')
		exit(1)
	tries = 1
	word = random.choice(list(words))
	while len(set(list(word))) < len(word):
		word = random.choice(list(words))
	greens = []
	yellows = []
	blacks = []
	while True:
		print(f'{tries}. Word chosen: {color_word(word, greens, yellows)}')
		tries += 1
		res = update_results(word, greens, yellows, blacks, target=target)
		if res:
			print(f'{GREEN}Word found successfully{RESET}')
			return 0
		else:
			words.remove(word)
		words = choose_next(greens, yellows, blacks)
		if len(words) == 0:
			print('Word not found')
			return 1
		word = random.choice(list(words))

	exit(0)

if __name__ == '__main__':
	main()




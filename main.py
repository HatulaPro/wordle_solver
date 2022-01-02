import random
words = set([word.strip() for word in open('./words.txt', 'r').readlines()])

def update_results(word, greens, yellows, blacks):
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
			# print(f'black in word {word}')
			continue

		for yellow in yellows:
			if yellow['char'] in word:
				potential_answers.add(word)	
			# if word[yellow['location']] == yellow['char']:
			#	continue
		if all(word[green['location']] == green['char'] for green in greens):
			potential_answers.add(word)
		elif word in potential_answers:

			potential_answers.remove(word)
	return potential_answers

def main():
	word = random.choice(list(words))
	greens = []
	yellows = []
	blacks = []
	while True:
		print(f'Word chosen: {word}')
		res = update_results(word, greens, yellows, blacks)
		if res:
			print('Word found successfully')
			return 0
		else:
			words.remove(word)
		potential_answers = choose_next(greens, yellows, blacks)
		# print(f'Potential answers: {potential_answers}')
		if len(potential_answers) == 0:
			print('Word not found')
			return 1
		word = random.choice(list(potential_answers))


	exit(0)

if __name__ == '__main__':
	main()




import sys

with open('word-bank-animals.txt') as f:
# with open('word-bank.txt') as f:
	words = f.readlines()
words = sorted([w.strip().lower() for w in words])
# words = ['zebra', 'whale']

targets = sys.argv[1]
if targets == 'all':
	targets = words
else:
	print('Targets:', targets)
	targets = [targets]
if len(sys.argv) > 2:
	max_depth = int(sys.argv[2])
else:
	max_depth = float('NaN')

def play_next_turn(candidates, guesses=[], depth=1):
	num_expected_plays = 0

	if tuple(candidates) in cache:
		return cache[tuple(candidates)]

	for word in candidates:
		if word == target or depth == max_depth:
			print(guesses + [word], depth)
			num_expected_plays += 1 / len(candidates)
		else:
			correct_position = []
			incorrect_position = []
			incorrect_letter = []
			matched_positions = []

			# find correct letters in correct positions and incorrect letters
			for word_pos, word_char in enumerate(word):
					if target[word_pos] == word_char:
						correct_position.append((word_pos, word_char))
					elif word_char not in target:
						incorrect_letter.append(word_char)
					else:
						flag = False
						for target_pos, target_char in enumerate(target):
							# not a correct letter at a correct position 
							# or an already-matched correct letter at a wrong position
							if word_char == target_char \
								and word_pos != target_pos \
								and target_pos not in matched_positions:
								flag = True
								# match to first possible position in target word
								matched_positions.append(target_pos)
								incorrect_position.append(word_char)
								break
						# necessary in case of "brush" and "burrs" (for example)
						# the first "r" is an incorrect position, but the second "r" is an incorrect letter
						if not flag:
							incorrect_letter.append(word_char)

			new_candidates = candidates.copy()
			for cand in candidates:
				# remove any candidates that do not share correct letters at correct positions
				if any([c != cand[p] for p, c in correct_position]):
					new_candidates.remove(cand)
				else:
					# remove all letters that are correct at correct positions
					mod_cand = ''
					for p, c in enumerate(cand):
						if p not in [e for e, _ in correct_position]:
							mod_cand += c

					# remove all candidates that do not have correct letters at incorrect positions
					flag = False
					for c in incorrect_position:
						if c not in mod_cand:
							flag = True
							new_candidates.remove(cand)
							break
						mod_cand = mod_cand.replace(c, '', 1)

					# remove all candidates that have incorrect letters
					if not flag and any([c in mod_cand for c in incorrect_letter]):
							flag = True
							new_candidates.remove(cand)

					# remove word if is anagram of candidate (i.e. all letters are correct at wrong positions)
					if not flag and cand == word:
						new_candidates.remove(cand)

			# print(word)
			# print(correct_position, incorrect_position, incorrect_letter)
			# print(candidates, new_candidates)
			# print()

			expected_future_plays = play_next_turn(new_candidates, guesses + [word], depth + 1)
			num_expected_plays += (1 + expected_future_plays) /  len(candidates)

	cache[tuple(candidates)] = num_expected_plays
	return cache[tuple(candidates)]

expectation = 0
for target in targets:
	cache = {}
	expectation += play_next_turn(words) / len(targets)
print(expectation)
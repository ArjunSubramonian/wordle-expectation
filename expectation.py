with open('word-bank.txt') as f:
	words = f.readlines()
words = sorted([w.strip() for w in words])

cache = {}
target = 'brush'
print(target)

def play_next_turn(candidates):
	num_expected_plays = 0

	if tuple(candidates) in cache:
		return cache[tuple(candidates)]

	for word in candidates:
		if word == target:
			num_expected_plays += 1
		else:
			correct_position = []
			incorrect_position = []
			incorrect_letter = []
			position_matches = []
			for word_pos, word_char in enumerate(word):
					if target[word_pos] == word_char:
						position_matches.append(word_pos)
						correct_position.append((word_pos, word_char))
					elif word_char not in target:
						incorrect_letter.append(word_char)
			
			for word_pos, word_char in enumerate(word):
				flag = False
				for target_pos, target_char in enumerate(target):
					if word_char == target_char \
					and target_pos != word_pos \
					and target_pos not in position_matches:
						flag = True
						position_matches.append(target_pos)
						incorrect_position.append(word_char)
						break
				if not flag:
					incorrect_letter.append(word_char)

			new_candidates = candidates.copy()
			for cand in candidates:
				if any([c != cand[p] for p, c in correct_position]):
					new_candidates.remove(cand)
				else:
					mod_cand = ''
					for p, c in enumerate(cand):
						if p not in [e for e, _ in correct_position]:
							mod_cand += c

					flag = False
					for c in incorrect_position:
						if c not in mod_cand:
							flag = True
							new_candidates.remove(cand)
							break
						mod_cand = mod_cand.replace(c, '', 1)

					if not flag and any([c in mod_cand for c in incorrect_letter]):
							flag = True
							new_candidates.remove(cand)

					# anagram
					if not flag and cand == word:
						new_candidates.remove(cand)

			print(word)
			print(correct_position, incorrect_position, incorrect_letter)
			print(candidates, new_candidates)
			print()

			num_expected_plays += 1 + play_next_turn(new_candidates)

	cache[tuple(candidates)] = num_expected_plays / len(candidates)
	return num_expected_plays / len(candidates)

print(play_next_turn(words))

		

		




				

	

import numpy as np 
import enchant
import pdb

d = enchant.Dict("en_US")
deltas = [np.array((1, 0)), np.array((-1, 0)), np.array((0, 1)), np.array((0, -1))]
deltas = [(1, 0), (-1, 0), (0, 1), (0, -1), (1,1), (1,-1), (-1, -1), (-1, 1)]
#deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
input_strs = ['rnesdepp', 'etounrep', 'nearfeog', 'geeuenen', 'itrlfeni', 'sagicfiv', 'eradfbma', 'dicsiocs']
word_lens = [6, 7, 6, 8, 7, 8, 6, 6, 10]
MAX_WIDTH = 8
MAX_HEIGHT = 8





class Puzzle:
	def __init__(self, state, word_set, parent_puzzle):
		self.state = state
		self.parent = parent_puzzle
		self.word_set = word_set
		self.children = []

	def add_child(self, word, new_state):
		new_word_set = self.word_set + [word]
		new_puzzle = Puzzle(new_state, new_word_set, self)
		self.children.append(new_puzzle)
		return new_puzzle


def next_indices(coord):
	# todo: the four other options (diagonals)
	new_coords = [add_tuple(coord,delta) for delta in deltas]
	return new_coords


def apply_gravity(puzzle):
	for j in range(MAX_WIDTH):
		col = puzzle[:,j]
		none_idxs = np.where(col == NONE_CHAR)[0]
		num_none = len(none_idxs)
		while len(none_idxs) and none_idxs[-1] >= num_none: 
			col[1:none_idxs[-1]+1] = col[0:none_idxs[-1]]
			col[0] = NONE_CHAR
			none_idxs = none_idxs[:-1] + 1
	return puzzle


def get_new_state(state, coord_seq):
	# Returns new puzzle with -1's in the indices in coord_seq
	new_state = state.copy()
	for coord in coord_seq:
		new_state[coord[0]][coord[1]] = NONE_CHAR
	row_del = []
	for i, row in enumerate(new_state):
		if len(set(row)) == 1:
			row_del.append(i)
	np.delete(new_state, row_del, axis=0)
	new_state = apply_gravity(new_state)
	return new_state

def add_tuple(x, y):
	return (x[0] + y[0], x[1] + y[1])


def get_word_from_coord_seq(puzzle, coord_seq):
	word = [puzzle[xy[0]][xy[1]] for xy in coord_seq]
	return ''.join(word)


def all_words(puzzle, word_len):
	# Generate all possible new states from a puzzle 
	# given a certain word length

	all_words = []
	all_new_states = []
	state = puzzle.state
	w = min(MAX_WIDTH, len(state[0]))
	h = min(MAX_HEIGHT, len(state))
	for i in range(h):
		for j in range(w):
			# Choosing different starting coordinates 
			# for word of length word_len
			coord = (i, j)
			if state[i][j] == NONE_CHAR:
				continue
			coord_seqs = [[coord]]
			
			while len(coord_seqs) > 0:
				coord_seq = coord_seqs.pop(0)
				if len(coord_seq) == word_len:
					word = get_word_from_coord_seq(state, coord_seq)
					if d.check(word):
						print word
						new_state = get_new_state(state, coord_seq)
						all_words.append(word)
						all_new_states.append(new_state)
					continue

				next_coords = next_indices(coord_seq[-1])
				# Potential for pruning here - don't return indices that are outside of state
				# Filters returned coordinates by:
				# 	- Not mapping to a NONE_CHAR square
				#	- Not mapping outside of the state
				# 	- Not reusing tiles
				next_coords = [xy for xy in next_coords if coord_check(xy, h, w)]
				next_coords = [xy for xy in next_coords if state[xy[0],xy[1]] != NONE_CHAR]
				next_coords = [xy for xy in next_coords if xy not in coord_seq]
				coord_seqs.extend([coord_seq + [xy] for xy in next_coords])
	return all_words, all_new_states

def filter_words(words, new_puzzles):
	# input: words = array of word/mask tuples
	# runs through list of all possible words+mask combinations
	# and returns ones that are in English dictionary
	n_words = len(words)
	real_words = []
	real_puzzles = []
	for i in range(n_words):
		if d.check(words[i]):
			real_words.append(words[i])
			real_puzzles.append(new_puzzles[i])
	return real_words, real_puzzles

def coord_check(xy, h, w):
	if xy[0] < h and xy[0] >= 0 and xy[1] < w and xy[1] >= 0:
		return True
	return False

def solve_puzzle(puzzle, word_lens):
	puzzle_states = [puzzle]
	parent_puzzle = puzzle
	for word_len in word_lens:
		# Focus on one word length at a time and generate all possible
		# resulting puzzle states

		new_states = []
		for puzzle in puzzle_states:
			new_words, new_puzzles = all_words(puzzle, word_len)
			new_words, new_puzzles = filter_words(new_words, new_puzzles)
			for w, state in zip(new_words, new_puzzles):
				s = puzzle.add_child(w, state)
				new_states.append(s)
		print 'Finished expanding words of length: ', word_len

		puzzle_states = new_states


	children = [parent_puzzle]
	for i in range(len(word_lens)):
		children = [parent.children for parent in children]
		children = [child for sublist in children for child in sublist]
		children = [child for child in children if child is not None]
	pdb.set_trace()
input_strs = ['splc', 'urau', 'ganp', 'ball']
word_lens = [4, 5, 4, 3]
MAX_WIDTH = 4
MAX_HEIGHT = 4
NONE_CHAR = '.'

input_strs = open('test.txt', 'r').readlines()
input_strs = [x[:-1] for x in input_strs]
MAX_WIDTH = 8
MAX_HEIGHT = 8
word_lens = [7, 6, 11]

input_strs = ['rnesdepp', 'etounrep', 'nearfeog', 'geeuenen', 'itrlfeni', 'sagicfiv', 'eradfbma', 'dicsiocs']
word_lens = [6, 7, 6, 8, 7, 8, 6, 6, 10]
MAX_WIDTH = 8
MAX_HEIGHT = 8

puzzle = Puzzle(np.core.defchararray.array([list(x) for x in input_strs]), [], None)
solve_puzzle(puzzle, word_lens)





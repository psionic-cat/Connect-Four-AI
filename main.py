# Importing needed modules, defining X and O, and the columns
import copy, random, time
X, O = "X", "O"
columnNames = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6}


# The Tree Class; a class to store the board and play the game
class Tree:
	# A function to set variables and generate and rank boards
	def __init__(self, rootNode, dist):
		self.rootNode, self.dist = rootNode, dist
		self.tree = {}
		self.buildTree(rootNode)
		self.rootNode.setBestChild(self.dist)

	# A function to generate all possible boards 
	def buildTree(self, node, c=0):
		# Making sure that no one has won on this board and that it isn't a tie
		if not node.winChecks(X) and not node.winChecks(O) and len(node.openSpots()) > 0:
			# Making sure the node wasn't already made
			if len(node.neighbors) == 0:
				# Looping through all of the possible neighbors and making them
				for i in node.openSpots():
					if c >= self.dist:
						break
					x, y = i[0], i[1]
					boardcopy = copy.deepcopy(node.board)
					boardcopy[x][y] = node.turn
					# Making an ID for the board to store in self.tree
					ID = ''.join([''.join(i) for i in boardcopy])
					# If the node isn't already in self.tree, add it and make it a node
					if ID not in self.tree:
						bcopy = TreeNode(boardcopy)
						self.tree[ID] = bcopy
						#print(ID, bcopy)
					# Add the node as a neighbor to our current node
					node.neighbors.append(self.tree[ID])
			# Running the program again for each of the neighbors of our current node
			for i in node.neighbors:
				self.buildTree(i, c + 1)

	# A function to help the player make a move
	def playerTurn(self, node):
		# Printing the board and asking where the player wants to go
		node.printBoard()
		column = columnNames[input("\nPick a column to play: ")]
		# Making sure that the column they picked exists and isn't fully filled
		if column not in [i[1] for i in node.openSpots()]:
			print("\nThat column is already filled or doesn't exist. Please enter a new column."); time.sleep(1.55)
			node = self.playerTurn(node)
		# Finding which of the node's neighbors is the correct next move
		else:
			for i in node.openSpots():
				if i[1] == column:
					p = i
			copyboard = copy.deepcopy(node.board)
			copyboard[p[0]][p[1]] = node.turn
			for i in node.neighbors:
				if i.board == copyboard:
					node = i
		return node

	# A function to run and control the game
	def playGame(self):
		node = self.rootNode
		first = "PLAYER"
		if random.randint(0, 1) == 0:
			node = node.bestChild
			first = "AI"
		while not node.winChecks(X) and not node.winChecks(O) and len(node.openSpots()) > 0:
			node = self.playerTurn(node)
			time.sleep(.2)
			node.printBoard()
			if not node.winChecks(X) and not node.winChecks(O) and len(node.openSpots()) > 0:
				node = node.bestChild
				self.tree = {}
				self.buildTree(node)
				node.setBestChild(self.dist)
		
		node.printBoard()
		if node.winChecks(X):
			if first == "PLAYER":
				print("\nYou win!")
			else:
				print("\nAI wins!")
		elif node.winChecks(O):
			if first == "AI":
				print("\nYou win!")
			else:
				print("\nAI wins!")
		else:
			print("\nTie!")


# The TreeNode class; a class to define each board and its variables
class TreeNode:
	# Defining each variable
	def __init__(self, board=[["-", "-", "-", "-", "-", "-", "-"] for i in range(6)]):
		self.board, self.neighbors = board, []
		self.bestChild, self.score = None, 0
		self.turn = (X if sum(i.count(X) for i in self.board) == sum(i.count(O) for i in self.board) else O)

	# The minimax function / finding the best next move
	def setBestChild(self, maxDepth=float('inf'), d=0):
		# Base Cases
		if self.winChecks(X):
			self.score = +1
			return
		elif self.winChecks(O):
			self.score = -1
			return
		elif len(self.openSpots()) == 0 or d >= maxDepth:
			return
		# Recursive Call
		for neighbor in self.neighbors:
			neighbor.setBestChild(maxDepth, d + 1)
		# Setting score and best child
		if self.turn == X:
			bestChild = self.neighbors[0]
			for i in self.neighbors:
				# Adding a bit of randomness to decide if it will be greater than or if it will be greater than or equal to
				r = random.randint(0, 1)
				if r == 0:
					if i.score > bestChild.score:
						bestChild = i
				else:
					if i.score >= bestChild.score:
						bestChild = i
		else:
			bestChild = self.neighbors[0]
			for i in self.neighbors:
				# Adding a bit of randomness to decide if it will be less than or if it will be less than or equal to
				r = random.randint(0, 1)
				if r == 0:
					if i.score < bestChild.score:
						bestChild = i
				else:
					if i.score <= bestChild.score:
						bestChild = i
		self.score, self.bestChild = bestChild.score, bestChild

	# Printing the board in a formatted style
	def printBoard(self):
		# Clearing the screan and printing the column names
		print("\033c", end="")
		print(" a   b   c   d   e   f   g")
		# Looping throught the rows and printing them nicely
		for i in range(len(self.board)):
			print("", self.board[i][0], "|", self.board[i][1], "|", self.board[i][2], "|", self.board[i][3], "|", self.board[i][4], "|", self.board[i][5], "|", self.board[i][6], "\n---+---+---+---+---+---+---" if i != 5 else "")

	# Looking for all of the open spots on the board
	def openSpots(self):
		# Creating the list spots
		spots = []
		# Looping through each of the columns
		for i in range(7):
			# Creating a list for the columns; True means it's an open space and False means it's filled
			column = []
			for j in range(len(self.board)):
				column.append((True if self.board[j][i] == "-" else False))
			# Making sure that there is an open spot in the column
			if True in column:
				# Looping throught the first 5 spots and checking if the one after it is filled or not
				for j in range(5):
					if column[j] == True and column[j + 1] == False:
						break
				# Checking if the 6th spot is open instead of the 5th one
				if column[j] == True and column[j + 1] == True:
					j += 1
				# Adding the lowest down open spot to the list
				spots.append([j, i])
		return spots

	# Checking to see who has won on the board, if anyone
	def winChecks(self, p):
		# Looping through each position on the board
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				# Checking if the current position is the player we're looking for
				if self.board[i][j] == p:
					# Checking up and down
					if i >= 3:
						if self.board[i - 1][j] == p and self.board[i - 2][j] == p and self.board[i - 3][j] == p:
							return True
					# Checking across on the right and left
					if j <= 3:
						if self.board[i][j + 1] == p and self.board[i][j + 2] == p and self.board[i][j + 3] == p:
							return True
					# Checking a diagonal
					if i >= 3 and j <= 3:
						if self.board[i - 1][j + 1] == p and self.board[i - 2][j + 2] == p and self.board[i - 3][j + 3] == p:
							return True
					# Checking the other diagonal
					if i <= 2 and j <= 3:
						if self.board[i + 1][j + 1] == p and self.board[i + 2][j + 2] == p and self.board[i + 3][j + 3] == p:
							return True
		# If there wasn't a win, return False
		return False

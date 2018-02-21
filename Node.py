# @Author Zhihan Jiang
import numpy as np
# class to representing a node
class Node:

	def __init__(self, depth, board_info, player, move=False):
		self.depth = depth
		self.board_info = board_info
		self.player = player
		self.children = []

		if move is not False:
			self.board_info[move] = player

		print(f'reached a node with a depth of {self.depth}')
		self.print_board()
		print()

		self.expand()
		
	def expand(self):
		empty = [i for i, x in enumerate(self.board_info) if x is ""]
		if len(empty) is not 0:
			print('expanding')
			for place in empty:
				self.children.append(Node(self.depth + 1, list(self.board_info), self.switch_player(), place))
		else:
			print("no room for expandition")

	def switch_player(self):
		if self.player is "W":
			return "B"
		elif self.player is "B":
			return "W"
		else:
			print('YOU MUST BE KIDDING ME')

	# function to display the board of the game
	def print_board(self):
		print(self.board_info)
		


if __name__ == '__main__':
	board = []
	while len(board) < 3:
		board.append("")
	origin = Node(0, board, 'W')
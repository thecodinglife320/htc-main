import math
import random
from copy import deepcopy

def mcts_tic_tac_toe(board_state, current_player):
    for i in range(3):
        for j in range(3):
            if board_state[i][j] == '':
                return i, j  # Trả về vị trí ô trống đầu tiên
 
    # class Board():
    #     def __init__(self, board, player):
    #         self.board = deepcopy(board)
    #         self.player_1 = player
    #         self.player_2 = 'x' if player == 'o' else 'o'
    #         self.empty_square = ''

    #     def make_move_mcts(self, row, col):
    #         new_board = Board(self.board, self.player_1)
    #         new_board.board[row][col] = self.player_1
    #         new_board.player_1, new_board.player_2 = new_board.player_2, new_board.player_1
    #         return new_board

    #     def is_draw_mcts(self):
    #         for row in self.board:
    #             if self.empty_square in row:
    #                 return False
    #         return True

    #     def is_win__mcts(self):
    #         for row in range(3):
    #             if self.board[row][0] == self.board[row][1] == self.board[row][2] != self.empty_square:
    #                 return True
    #         for col in range(3):
    #             if self.board[0][col] == self.board[1][col] == self.board[2][col] != self.empty_square:
    #                 return True
    #         if self.board[0][0] == self.board[1][1] == self.board[2][2] != self.empty_square:
    #             return True
    #         if self.board[0][2] == self.board[1][1] == self.board[2][0] != self.empty_square:
    #             return True
    #         return False

    #     def generate_states(self):
    #         states = []
    #         defensive_states = []
    #         winning_states = []
    #         for row in range(3):
    #             for col in range(3):
    #                 if self.board[row][col] == self.empty_square:
    #                     new_state = self.make_move_mcts(row, col)
    #                     if new_state.is_win__mcts():
    #                         # Nước đi có thể thắng
    #                         winning_states.append(new_state)
    #                     elif new_state.make_move_mcts(row, col).is_win__mcts():
    #                         # Nước đi chặn đối thủ
    #                         defensive_states.append(new_state)
    #                     else:
    #                         states.append(new_state)
    #         return winning_states + defensive_states + + states  # Ưu tiên nước đi thắng trước
        

    # class TreeNode():
    #     def __init__(self, board, parent):
    #         self.board = board
    #         self.parent = parent
    #         self.is_terminal = board.is_win__mcts() or board.is_draw_mcts()
    #         self.is_fully_expanded = self.is_terminal
    #         self.visits = 0
    #         self.score = 0
    #         self.children = {}

    # class MCTS():
    #     def search(self, initial_state):
    #         self.root = TreeNode(initial_state, None)
    #         for _ in range(5000):
    #             node = self.select(self.root)
    #             score = self.rollout(node.board)
    #             self.backpropagate(node, score)
    #         return self.get_best_move(self.root, 0)

    #     def select(self, node):
    #         while not node.is_terminal:
    #             if node.is_fully_expanded:
    #                 node = self.get_best_move(node, 2)
    #             else:
    #                 return self.expand(node)
    #         return node

    #     def expand(self, node):
    #         # Tạo các trạng thái mới từ board
    #         for state in node.board.generate_states():
    #             state_key = self.state_to_key(state.board)
    #             # Kiểm tra nếu trạng thái đã tồn tại trong children
    #             if state_key not in node.children:
    #                 new_node = TreeNode(state, node)
    #                 node.children[state_key] = new_node
    #                 # Kiểm tra nếu tất cả các trạng thái đã được mở rộng
    #                 if len(node.board.generate_states()) == len(node.children):
    #                     node.is_fully_expanded = True
    #                 return new_node
    #         return node  # Trả về node gốc nếu không mở rộng được

    #     def rollout(self, board):
    #         while not board.is_win__mcts() and not board.is_draw_mcts():
    #             # Kiểm tra nếu có nước đi thắng ngay
    #             for state in board.generate_states():
    #                 if state.is_win__mcts():
    #                     return 1 if state.player_2 == 'x' else -1
    #             # Kiểm tra nếu cần chặn đối thủ
    #             for state in board.generate_states():
    #                 next_board = state.make_move_mcts(*self.find_empty_square(state.board))
    #                 if next_board.is_win__mcts():
    #                     board = state
    #                     break
    #             else:
    #                 # Nếu không có tình huống thắng hoặc cần chặn, chơi ngẫu nhiên
    #                 board = random.choice(board.generate_states())
    #         # Xác định người thắng
    #         if board.player_2 == 'x':
    #             return 1
    #         elif board.player_2 == 'o':
    #             return -1
    #         return 0

    #     @staticmethod
    #     def find_empty_square(board):
    #         for row in range(3):
    #             for col in range(3):
    #                 if board[row][col] == '':
    #                     return row, col
    #         return -1, -1  # Trường hợp không hợp lệ


    #     def backpropagate(self, node, score):
    #         while node is not None:
    #             node.visits += 1
    #             node.score += score
    #             node = node.parent


    #     def get_best_move(self, node, exploration_constant):
    #         best_score = float('-inf')
    #         best_moves = []
    #         for child in node.children.values():
    #             # Tính toán điểm số cho mỗi node con
    #             if child.visits > 0:
    #                 exploitation = child.score / child.visits
    #                 exploration = exploration_constant * math.sqrt(math.log(node.visits) / child.visits)
    #                 move_score = exploitation + exploration
    #             else:
    #                 move_score = exploration_constant  # Ưu tiên vừa phải cho trạng thái chưa thăm
    #             # Cập nhật danh sách các node có điểm số tốt nhất
    #             if move_score > best_score:
    #                 best_score = move_score
    #                 best_moves = [child]
    #             elif move_score == best_score:
    #                 best_moves.append(child)
    #         return random.choice(best_moves)


    #     @staticmethod
    #     def state_to_key(board):
    #         return ''.join(''.join(row) for row in board)

    # board_instance = Board(board_state, current_player)
    # mcts = MCTS()
    # best_node = mcts.search(board_instance)

    # for row in range(3):
    #     for col in range(3):
    #         if board_state[row][col] != best_node.board.board[row][col]:
    #             return row, col

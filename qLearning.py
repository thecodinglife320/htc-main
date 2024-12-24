import pickle
import random
alpha = 0.1 #learning rate
gamma = 0.9 #giảm giá trị phần thưởng tương lai
epsilon = 0.6 #xác xuất chọn hành động ngẫu nhiên(khám phá)
reward = 0 #phần thưởng
move_previous=[0,0]

def qlearning_tic_tac_toe(board_state,ai_symbol):
    try:
        with open("q_table.pkl", "rb") as f:
            Q_table = pickle.load(f)
    except FileNotFoundError:
        Q_table = {}

    if (ai_symbol=='O'): player_symbol='X'
    else: player_symbol='O'
    state = board_to_state(board_state)
    print('previous_move_ai:',end=' ')
    print(move_previous)
    #kiểm tra người chơi thắng
    if check_winner(board_state,player_symbol):
        update_q_table(state, (move_previous[0],move_previous[1]), -1, None, [],Q_table)
        save_q_table(Q_table)
        return 0,0
    
    if is_draw(board_state):
        update_q_table(state, (move_previous[0],move_previous[1]), +2, None, [],Q_table)
        save_q_table(Q_table)
        return 0,0

    #AI chọn nước đi
    #tim ra các nước đi còn lại
    valid_moves = [(i, j) for i in range(3) for j in range(3) if board_state[i][j] == '']
    
    #chọn nước đi tốt nhất và đánh dấu trên bàn cờ
    move = choose_move(state, valid_moves,Q_table)
    move_previous[0], move_previous[1] = move
    board_state[move_previous[0]][move_previous[1]] = ai_symbol
    
    #Kiểm tra AI thắng
    next_state = board_to_state(board_state)
    next_valid_moves = [(i, j) for i in range(3) for j in range(3) if board_state[i][j] == '']
    reward =0
    if check_winner(board_state, ai_symbol): reward = 4
    if is_draw(board_state): reward = 2
    update_q_table(state, move, reward, next_state, next_valid_moves,Q_table)
    save_q_table(Q_table)
    return move_previous[0], move_previous[1]
            
def choose_move(state, valid_moves,Q_table):
    if random.uniform(0, 1) < epsilon:  # Khám phá
        return random.choice(valid_moves)
    else:  # Ưu tiên khai thác
        q_values = [Q_table.get((state, move), 0) for move in valid_moves]
        print(q_values)
        return valid_moves[q_values.index(max(q_values))]
    
def update_q_table(state, move, reward, next_state, valid_moves,Q_table):
    next_q_values = [Q_table.get((next_state, move), 0) for move in valid_moves]
    max_next_q_value = max(next_q_values,default=0)
    current_q_value = Q_table.get((state, move), 0)
    Q_table[(state, move)] = current_q_value + alpha * (reward + gamma * max_next_q_value - current_q_value)

def save_q_table(q_table, filename="q_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)
    print(f"Q-table saved to {filename}")

def board_to_state(board): return ''.join(cell if cell != '' else '-' for row in board for cell in row)

def is_draw(board): return all(cell != '' for row in board for cell in row)

def check_winner(board, symbol):
        for row in board:
            if all(cell == symbol for cell in row):
                return True
        for col in zip(*board):
            if all(cell == symbol for cell in col):
                return True
        if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
            return True
        return False
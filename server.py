import socket
import threading
import queue
from demoAI import demoAI

class TicTacToeServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(10)
        self.client_queue = queue.Queue()  
        self.games = {} 
     

# Đưa client vào hàng đợi
    def handle_client(self, client_socket, addr):
        print(f"Client connected: {addr}")
        ai = client_socket.recv(2048).decode('utf-8')
        if ai == "": 
            self.client_queue.put(client_socket)  
            print(self.client_queue.qsize())         
        else:
            # Xử lý AI dựa trên lựa chọn
            match ai:
                case "MCTS":
                    algorithm = "MCTS"
                case "SARSA":
                    algorithm = "SARSA"
                case "Q-Learning":
                    algorithm = "Q-Learning"
                case "Minimax":
                    algorithm = "Minimax"
                case _:
                    print(f"Invalid AI selection: {ai}")
                    client_socket.send("INVALID_AI".encode('utf-8'))
                    client_socket.close()
                    return

            print(f"Starting AI game with algorithm: {algorithm}")
            threading.Thread(target=demoAI, args=(client_socket, self.check_winner, self.is_draw, algorithm)).start()


    def remove_client(self, client_socket):
        for game_id, players in list(self.games.items()):
            if client_socket in players:
                players.remove(client_socket)
                if len(players) == 1:
                    self.client_queue.put(players[0])   
                del self.games[game_id]
                break
        client_socket.close()

    def match_clients(self):
        
        while True:
            if self.client_queue.qsize() >= 2:   
                client1 = self.client_queue.get()
                client2 = self.client_queue.get()
                game_id = f"game_{len(self.games) + 1}"
                self.games[game_id] = [client1, client2]
                threading.Thread(target=self.start_game, args=(client1, client2, game_id)).start()

    def start_game(self, client1, client2, game_id):
        print(f"Starting {game_id} with {client1} and {client2}")
        board = [['' for _ in range(3)] for _ in range(3)]
        turn = client1  # Client1 bắt đầu

        try:
            client1.send("MATCH_FOUND X".encode('utf-8'))
            client2.send("MATCH_FOUND O".encode('utf-8'))

            while True:
                current_player = turn
                other_player = client2 if turn == client1 else client1
                try:
                    print("Waiting for move from current player...")
                    data = current_player.recv(2048).decode('utf-8')
                    

                    if not data:
                        print(f"Connection lost with {current_player}")
                        break
                    print(f"Data received: {data} ")
                    if data.startswith("MOVE"):
                        _, row, col = data.split()
                        row, col = int(row), int(col)
                        symbol = 'X' if current_player == client1 else 'O'
                        
                        if board[row][col] == '':
                            board[row][col] = symbol
                          
                            current_player.send(f"VALID_MOVE {row} {col}".encode('utf-8'))
                            other_player.send(f"OPPONENT_MOVE {row} {col}".encode('utf-8'))
                         
                            if self.check_winner(board, symbol):
                                current_player.send("WIN".encode('utf-8'))
                                other_player.send("LOSE".encode('utf-8'))

                            elif self.is_draw(board):
                                current_player.send("DRAW".encode('utf-8'))
                                other_player.send("DRAW".encode('utf-8'))
 
                            turn = other_player   
                        else:
                            current_player.send("INVALID_MOVE".encode('utf-8'))
                    
                    elif data.startswith("SURRENDER") :
                        current_player.send("LOSE".encode('utf-8'))
                        other_player.send("WIN".encode('utf-8'))

                    elif data.startswith("REPLAY") :
                        board = [['' for _ in range(3)] for _ in range(3)]  
                        turn = client2 if turn == client1 else client1
                        current_player.send("REPLAY_OK X".encode('utf-8'))  # Thông báo cho người đang chơi
                        other_player.send("REPLAY_OK O".encode('utf-8'))  # Thông báo cho người còn lại
                        print(f"Game {game_id} reset for replay.")
                    
                except Exception as e:
                    print(f"Error while processing move: {e}")
                    self.remove_client(current_player)
                    break
        except Exception as e:
            print(f"Game {game_id} ended with error: {e}")

    def check_winner(self, board, symbol):
        for row in board:
            if all(cell == symbol for cell in row):
                return True
        for col in zip(*board):
            if all(cell == symbol for cell in col):
                return True
        if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
            return True
        return False

    def is_draw(self, board):
        return all(cell != '' for row in board for cell in row)

    def start(self):
        print("Server started...")
        threading.Thread(target=self.match_clients).start()
        while True:
            client_socket, addr = self.server.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()

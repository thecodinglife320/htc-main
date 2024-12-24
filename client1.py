import socket
import threading
import tkinter as tk
from tkinter import messagebox
import sys

class TicTacToeClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.turn = False
        self.symbol = ''
        self.player_name = "Player"
        self.win_count = 0
        self.lose_count = 0
        self.draw_count = 0
        self.init_ui()
        threading.Thread(target=self.receive_data, daemon=True).start()

        if len(sys.argv) > 1:
            ai = sys.argv[1]
            self.client.send(f"{ai}".encode('utf-8'))
        else:
            self.client.send(f"".encode('utf-8'))




    def send_move(self, row, col):
        print(self.turn)
        if self.turn and self.buttons[row][col]['text'] == '':
            self.buttons[row][col]['text'] = self.symbol
            self.turn = False
            self.client.send(f"MOVE {row} {col}".encode('utf-8'))

    def surrender(self):
        self.client.send("SURRENDER".encode('utf-8'))
        messagebox.showinfo("Game Over", "You surrendered!")
    

    def replay(self):
        self.client.send("REPLAY".encode('utf-8'))
        print("----rep")

    def update_scoreboard(self):
        self.win_label.config(text=f"Wins: {self.win_count}")
        self.lose_label.config(text=f"Losses: {self.lose_count}")
        self.draw_label.config(text=f"Draws: {self.draw_count}")

    def end_game(self, message):
        self.status_label.config(text=message)
        messagebox.showinfo("Game Over", message)
        self.replay_button.config(state=tk.NORMAL)
        self.update_scoreboard()
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]:   
                    self.buttons[i][j].config(state=tk.DISABLED)
    

    def receive_data(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                if message == "MATCH_FOUND X":
                    self.turn = True
                if message.startswith("MATCH_FOUND"):
                    _, symbol = message.split()
                    self.symbol = symbol
                    self.status_label.config(text=f"Game started! You are {self.symbol}")
                elif message.startswith("VALID_MOVE"):
                    self.status_label.config(text="Opponent's turn...")
                elif message.startswith("OPPONENT_MOVE"):
                    _, row, col = message.split()
                    row, col = int(row), int(col)
                    opponent_symbol = 'X' if self.symbol == 'O' else 'O'
                    self.buttons[row][col]['text'] = opponent_symbol
                    self.turn = True
                    self.status_label.config(text="Your turn...")
                elif message.startswith("WIN"):
                    self.win_count += 1
                    self.end_game("You win!")
                elif message.startswith("LOSE"):
                    self.lose_count += 1
                    self.end_game("You LOSE!")
                elif message.startswith("DRAW"):
                    self.draw_count += 1
                    self.end_game("DRAW!")
                    
                elif message.startswith("REPLAY_OK"):
                    _, status = message.split()  
                    if status == "X":
                        self.turn = True
                        self.status_label.config(text=f"Game restarted! Your turn. You are X")
                        self.symbol = "X"
                    else:
                        self.turn = False
                        self.status_label.config(text=f"Game restarted! Waiting for opponent. You are O")
                        self.symbol = "O"
                    
                    for i in range(3):
                        for j in range(3):
                            self.buttons[i][j]['text'] = ''
                            self.buttons[i][j].config(state=tk.NORMAL, text='')
                    self.replay_button.config(state=tk.DISABLED)  # Disable nút replay

            except Exception as e:
                print("Error receiving data:", e)
                break




    def init_ui(self):
        main_frame = tk.Frame(self.window)
        main_frame.grid(row=0, column=0, padx=10, pady=10)

        # Tạo bảng nút cho giao diện trò chơi
        board_frame = tk.Frame(main_frame)
        board_frame.grid(row=0, column=0)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(board_frame, text='', font=('Arial', 24), height=2, width=5,
                                               command=lambda row=i, col=j: self.send_move(row, col))
                self.buttons[i][j].grid(row=i, column=j)
                
       
        self.status_label = tk.Label(main_frame, text="Waiting for opponent...", font=('Arial', 14))
        self.status_label.grid(row=1, column=0, pady=10)

     
        side_frame = tk.Frame(self.window, padx=10)
        side_frame.grid(row=0, column=1, sticky="n")

        # Thông tin người chơi
        tk.Label(side_frame, text="Player Information", font=('Arial', 14, 'bold')).pack(pady=5)

        self.name_label = tk.Label(side_frame, text=f"Name: {self.symbol}", font=('Arial', 12))
        self.name_label.pack(anchor='w')

        self.win_label = tk.Label(side_frame, text=f"Wins: {self.win_count}", font=('Arial', 12))
        self.win_label.pack(anchor='w')

        self.lose_label = tk.Label(side_frame, text=f"Losses: {self.lose_count}", font=('Arial', 12))
        self.lose_label.pack(anchor='w')

        self.draw_label = tk.Label(side_frame, text=f"Draws: {self.draw_count}", font=('Arial', 12))
        self.draw_label.pack(anchor='w')

        # Các nút chức năng
        tk.Label(side_frame, text="Actions", font=('Arial', 14, 'bold')).pack(pady=5)

        surrender_button = tk.Button(side_frame, text="Surrender", font=('Arial', 12), command=self.surrender)
        surrender_button.pack(fill=tk.X, pady=2)

        self.replay_button = tk.Button(side_frame, text="Replay", font=('Arial', 12), command=self.replay, state=tk.DISABLED)
        self.replay_button.pack(fill=tk.X, pady=2)

        exit_button = tk.Button(side_frame, text="Exit", font=('Arial', 12), command=self.window.quit)
        exit_button.pack(fill=tk.X, pady=2)

if __name__ == "__main__":
    TicTacToeClient()
    tk.mainloop()

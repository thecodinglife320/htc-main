import tkinter as tk
from subprocess import Popen
from tkinter import ttk

def open_play_online():
    try:
        Popen(["python", "client1.py"])
    except Exception as e:
        print(f"Error opening Play Online: {e}")

def play_with_ai(algorithm):
    try:
        Popen(["python", "client1.py", algorithm])
        print(algorithm)
    except Exception as e:
        print(f"Error opening Play with AI ({algorithm}): {e}")

# Hàm xử lý khi nhấn nút OK sau khi chọn thuật toán từ dropdown
def start_ai_game():
    selected_algorithm = ai_algorithm_var.get()
    if selected_algorithm:
        play_with_ai(selected_algorithm)


# Tạo cửa sổ chính
main_window = tk.Tk()
main_window.title("Tic Tac Toe Menu")
main_window.geometry("400x300")

# Cấu hình grid để giãn đều các cột và hàng
main_window.columnconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)
main_window.rowconfigure(0, weight=1)
main_window.rowconfigure(1, weight=1)
main_window.rowconfigure(2, weight=1)
main_window.rowconfigure(3, weight=1)

# Tiêu đề chính
title_label = tk.Label(main_window, text="Tic Tac Toe", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

# Nút "Play Online"
play_online_button = tk.Button(main_window, text="Play Online", font=("Arial", 14), command=open_play_online)
play_online_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

# Label chỉ dẫn cho dropdown
dropdown_label = tk.Label(main_window, text="Choose AI Algorithm:", font=("Arial", 12))
dropdown_label.grid(row=2, column=0, columnspan=2, pady=(10, 5))

# Dropdown menu cho "Play with AI"
ai_algorithm_var = tk.StringVar()
ai_algorithm_var.set("MCTS")  # Giá trị mặc định trống

# Danh sách thuật toán
algorithms = ["MCTS", "SARSA", "Q-Learning", "Minimax"]

# Tạo dropdown menu
algorithm_dropdown = ttk.Combobox(main_window, textvariable=ai_algorithm_var, values=algorithms, state="readonly", font=("Arial", 12))
algorithm_dropdown.grid(row=3, column=0, columnspan=2, padx=50, pady=5, sticky="nsew")

# Nút OK để xác nhận lựa chọn thuật toán
start_ai_button = tk.Button(main_window, text="Start AI Game", font=("Arial", 12), command=start_ai_game)
start_ai_button.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")

# Chạy cửa sổ
main_window.mainloop()

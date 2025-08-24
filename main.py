from tkinter import *
import random
import copy

root = Tk()
root.geometry("650x600")
root.title("Tic Tac Toe")
root.configure(bg="#1e1e1e")  # dark background

# --- Player Info ---
player1_name = StringVar()
player2_name = StringVar()
player1_score = IntVar(value=0)
player2_score = IntVar(value=0)
play_with_ai = BooleanVar(value=False)

# --- Player Name Inputs ---
frame_names = Frame(root, bg="#1e1e1e")
frame_names.pack(pady=10)

Label(frame_names, text="Player X:", fg="#00ffcc", bg="#1e1e1e", font=("Arial", 12)).grid(row=0, column=0, padx=5)
Entry(frame_names, textvariable=player1_name, font=("Arial", 12), width=12, bg="#2e2e2e", fg="white",
      insertbackground="white", highlightthickness=2, highlightbackground="#00ffcc", relief=FLAT).grid(row=0, column=1, padx=5)

Label(frame_names, text="Player O:", fg="#ff66cc", bg="#1e1e1e", font=("Arial", 12)).grid(row=0, column=2, padx=5)
Entry(frame_names, textvariable=player2_name, font=("Arial", 12), width=12, bg="#2e2e2e", fg="white",
      insertbackground="white", highlightthickness=2, highlightbackground="#ff66cc", relief=FLAT).grid(row=0, column=3, padx=5)

Checkbutton(frame_names, text="Play vs Computer", variable=play_with_ai,
            bg="#1e1e1e", fg="white", font=("Arial", 10), activebackground="#1e1e1e", selectcolor="#1e1e1e").grid(row=1, column=0, columnspan=4, pady=5)

# --- Scoreboard ---
# --- Scoreboard Horizontal ---
frame_score = Frame(root, bg="#1e1e1e")
frame_score.pack(pady=10)

Label(frame_score, text="Scoreboard:", font=("Century Gothic", 16), fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)

Label(frame_score, textvariable=player1_name, font=("Arial", 14), fg="#ffcc00", bg="#1e1e1e").grid(row=0, column=1, padx=5)
Label(frame_score, textvariable=player1_score, font=("Arial", 14), fg="#ffcc00", bg="#1e1e1e").grid(row=0, column=2, padx=5)

Label(frame_score, textvariable=player2_name, font=("Arial", 14), fg="#ff66cc", bg="#1e1e1e").grid(row=0, column=3, padx=5)
Label(frame_score, textvariable=player2_score, font=("Arial", 14), fg="#ff66cc", bg="#1e1e1e").grid(row=0, column=4, padx=5)

# --- Game Board ---
frame_board = Frame(root, bg="#1e1e1e")
frame_board.pack(pady=10)

board = {i: "" for i in range(1, 10)}
turn = "X"
restartButton = None


# --- Message Label ---
msg_label = Label(frame_board, text="", bg="#1e1e1e", fg="#00ffcc", font=("Arial", 14))
msg_label.grid(row=3, column=0, columnspan=3, pady=10)

def showMessage(message):
    msg_label.config(text=message)

# --- Helper Functions ---
def checkForWin(player, brd=None):
    if brd is None:
        brd = board
    wins = [(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),(1,5,9),(3,5,7)]
    return any(brd[a]==brd[b]==brd[c]==player for a,b,c in wins)

def checkForDraw(brd=None):
    if brd is None:
        brd = board
    return all(brd[i] != "" for i in brd)

def disableBoard():
    for b in all_buttons:
        b.config(state=DISABLED)

def enableBoard():
    for b in all_buttons:
        b.config(state=NORMAL, text="")
    for i in board:
        board[i] = ""
    showMessage("")

def endGame(winner=None):
    if winner:
        showMessage(f"{winner} wins!")
    else:
        showMessage("Draw!")
    disableBoard()



# Restart button already visible, no need to create dynamically

def restartGame():
    global turn
    turn = "X"
    enableBoard()
    if play_with_ai.get() and turn=="O":
        root.after(500, ai_move)  # correct usage


# --- AI using Minimax ---
def ai_move():
    global turn
    move = minimax(board, "O")['position']
    all_buttons[move-1].event_generate("<Button-1>")

def minimax(brd, player):
    # base cases
    if checkForWin("X", brd):
        return {'score': -1}
    elif checkForWin("O", brd):
        return {'score': 1}
    elif checkForDraw(brd):
        return {'score': 0}

    moves = []
    for i in brd:
        if brd[i]=="":
            new_board = copy.deepcopy(brd)
            new_board[i] = player
            score = minimax(new_board, "O" if player=="X" else "X")['score']
            moves.append({'position': i, 'score': score})

    if player=="O":  # AI maximizes
        best = max(moves, key=lambda x: x['score'])
    else:  # player minimizes
        best = min(moves, key=lambda x: x['score'])
    return best

# --- Main Play Function ---
def play(event):
    global turn
    button = event.widget
    clicked = int(button._name)

    if button["text"] == "":
        button.config(text=turn, fg="#ffcc00" if turn=="X" else "#ff66cc")
        board[clicked] = turn

        if checkForWin(turn):
            winner = player1_name.get() if turn=="X" else player2_name.get()
            winner = winner or ("Player X" if turn=="X" else "Player O")
            if turn=="X":
                player1_score.set(player1_score.get()+1)
            else:
                player2_score.set(player2_score.get()+1)
            endGame(winner)
        elif checkForDraw():
            endGame()
        else:
            turn = "O" if turn=="X" else "X"
            if play_with_ai.get() and turn=="O":
                root.after(300, ai_move)

# --- Buttons ---
button_style = {"width": 4, "height": 2, "font": ("Arial", 30), "bg": "#2e2e2e", "activebackground": "#444"}

all_buttons = []
for i in range(9):
    btn = Button(frame_board, text="", **button_style, name=str(i+1))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    btn.bind("<Button-1>", play)
    all_buttons.append(btn)
# Frame for restart button
frame_restart = Frame(root, bg="#1e1e1e")
frame_restart.pack(pady=10)

restartButton = Button(frame_restart, text="Restart", width=12, height=2, bg="#1e1e1e",
                       fg="#00ffcc", font=("Arial", 12), command=restartGame)
restartButton.pack()

root.mainloop()

import chess
import AIplayer as AI 

board = chess.Board()

ai = AI.AiPlayer()
print(board)

def getinput():
    val = input("your move: ")
    return chess.Move.from_uci(val)
    

while not board.is_game_over(claim_draw=True):
    move = chess.Move.null()
    if not board.turn:
        move = ai.nextMove(board)
        board.push(move)
        print(move)
        print(ai.analysis())
    else:
        current_moves = board.legal_moves
        while move not in current_moves:
            move = getinput()
        board.push(move)
    print(board)

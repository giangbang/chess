import chess

class AiPlayer:
    DEPTH = 4
    thres = 1
    pawntable = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10,-20,-20, 10, 10,  5,
     5, -5,-10,  0,  0,-10, -5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
     0,  0,  0,  0,  0,  0,  0,  0]

    knightstable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50]

    bishopstable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20]

    rookstable = [
      0,  0,  0,  5,  5,  0,  0,  0,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
     -5,  0,  0,  0,  0,  0,  0, -5,
      5, 10, 10, 10, 10, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0]

    queenstable = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  5,  5,  5,  5,  5,  0,-10,
      0,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20]

    kingstable = [
     20, 30, 10,  0,  0, 10, 30, 20,
     20, 20,  0,  0,  0,  0, 20, 20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30]
    
    def __init__(self):
        self.count = 0
        self.maxdepth = 0
        self.curdepth = 0

    def evaluate(self, board, move=None):
        if move!=None:
            board = chess.Board(board.fen())
            board.push(move)
            
        return self.eval(board)
    
    def eval(self, board):
        if board.is_checkmate():
            if board.turn:
                return -99999
            else:
                return 99999
        if board.is_stalemate():
            return 0
        if board.is_insufficient_material():
            return 0
        
        wp = len(board.pieces(chess.PAWN, chess.WHITE))
        bp = len(board.pieces(chess.PAWN, chess.BLACK))
        wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(board.pieces(chess.ROOK, chess.WHITE))
        br = len(board.pieces(chess.ROOK, chess.BLACK))
        wq = len(board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(board.pieces(chess.QUEEN, chess.BLACK))
        
        material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)
        
        pawnsq = sum([self.pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq= pawnsq + sum([-self.pawntable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.knightstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq= sum([self.bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq= bishopsq + sum([-self.bishopstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)]) 
        rooksq = rooksq + sum([-self.rookstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)]) 
        queensq = queensq + sum([-self.queenstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)]) 
        kingsq = kingsq + sum([-self.kingstable[chess.square_mirror(i)] 
                                        for i in board.pieces(chess.KING, chess.BLACK)])
        
        eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq
        if board.turn:
            return eval
        else:
            return -eval
    
    def quisence(self, board, alpha, beta, depth = 0):
        self.count += 1
        self.maxdepth = max(self.maxdepth, self.DEPTH+depth)
        
        stand_pat = self.evaluate(board)
        if( stand_pat >= beta ):
            return beta
        if( alpha < stand_pat ):
            alpha = stand_pat
        
        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)        
                score = -self.quisence(board, -beta, -alpha, depth = depth+1 )
                board.pop()

                if( score >= beta ):
                    return beta
                if( score > alpha ):
                    alpha = score  
                    
        return alpha
    
    def interest(self, board, move):
        tmp = chess.Board(board.fen())
        tmp.push(move)
        return -len(board.attacks(move.from_square)) + len(tmp.attacks(move.to_square))
    
    def negamax(self, board, depth, alpha, beta):
        self.count += 1
        self.maxdepth = max(self.maxdepth, self.DEPTH - depth)
        
        if (depth <= 0):
            return self.quisence(board, alpha, beta)
        
        best = -999999
        for move in sorted([i for i in board.legal_moves], key=lambda move:self.evaluate(board, move)):
            
            d = min(depth-1, 1) if self.interest(board, move) < self.thres else depth-1
            board.push(move)
            
            score = -self.negamax(board, d, -beta, -alpha)
                
            board.pop()
            
            if (score >= beta):
                return score
            if (score > best):
                best = score
            if (score > alpha):
                alpha = score
        return best
      
    def nextMove(self, board):
        max = -999999
        self.count = 0
        self.maxdepth = 0
        res = chess.Move.null()
        alpha, beta = -999999, 999999
        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax(board, self.DEPTH, -beta, -alpha)
            board.pop()
            if score >= beta:
                return score
            if score > max:
                max = score
                res = move
            if score > alpha:
                alpha = score
        return res
    
    def analysis(self):
        return {"total nodes inspected: ":self.count, "maximum depth: ":self.maxdepth}
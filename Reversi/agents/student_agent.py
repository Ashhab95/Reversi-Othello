from agents.agent import Agent
from store import register_agent
from helpers import get_valid_moves, execute_move, check_endgame
import copy
import time
@register_agent("student_agent")
class StudentAgent(Agent):
    def __init__(self):
        super().__init__()
        self.name = "student_agent"
        self.time_limit = 1.9

    def step(self, board, player, opponent):

        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (board_size, board_size)
        where 0 represents an empty spot, 1 represents Player 1's discs (Blue),
        and 2 represents Player 2's discs (Brown).
        - player: 1 if this agent is playing as Player 1 (Blue), or 2 if playing as Player 2 (Brown).
        - opponent: 1 if the opponent is Player 1 (Blue), or 2 if the opponent is Player 2 (Brown).

        You should return a tuple (r,c), where (r,c) is the position where your agent
        wants to place the next disc. Use functions in helpers to determine valid moves
        and more helpful tools.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """

        #keeping track of time for IDS
        start = time.time()
        #initializing depth
        depth = 1
        #the move agent will make
        final_agent_move = None

        #while true, we iteratively try to find the best move by increasing the depth
        while True:
            try: 
                current_agent_move = self.minimax_ids(board, player, opponent, depth, start)
                if current_agent_move:
                    final_agent_move = current_agent_move
                depth+=1 #move to next depth
            except TimeoutError:
                break
        return final_agent_move


    def minimax_ids(self, board, player, opponent, depth, start):

        #initializing
        agent_move, value = None, float('-inf')
        alpha, beta = float('-inf'), float('inf')

        #get all possible moves 
        all_moves = get_valid_moves(board, player)
        if all_moves:
            for move in all_moves:
                if time.time() - start > self.time_limit: #step cannot exceed 1.5s
                    raise TimeoutError

                board_copy = copy.deepcopy(board)
                execute_move(board_copy, move, player) #execute the move on the board copy

                curr_value = self.minimax_main(board_copy, depth-1, False, player, opponent, alpha, beta, start) #find curr value

                if curr_value > value: #if we get a better value than prev value
                    value = curr_value #set value as curr value
                    agent_move = move #set agent move as the current move
                alpha = max(curr_value, alpha) # update alpha
            return agent_move

        else: #if no valid moves, return None
            return None


    def minimax_main(self, board, depth, maxim, player, opponent, alpha, beta, start):

        #time check
        if time.time() - start > self.time_limit:
            raise TimeoutError

        #if the game is finished or depth is 0, we just evaluate the board and return
        if check_endgame(board, player, opponent)[0] or depth == 0:
            return self.evaluate(board, player, opponent)

        #getting the moves for maximizing player which is our agent
        current_player = None
        if maxim:
            current_player = player #agent is maximizing
        else:
            current_player = opponent #opponent is minimizing
        
        all_moves = get_valid_moves(board, current_player)
        if not all_moves:
            return self.minimax_main(board, depth-1, not maxim, player, opponent, alpha, beta, start)
        
        if maxim: #if maximizing player
            max_value = float('-inf')

            for move in all_moves:
                if time.time() - start > self.time_limit: #time check
                    raise TimeoutError
                board_copy = copy.deepcopy(board)
                execute_move(board_copy, move, player) #execute move on board copy

                minimax_val = self.minimax_main(board_copy, depth-1, False, player, opponent, alpha, beta, start)
                max_value = max(max_value, minimax_val) #update max value and alpha
                alpha = max(alpha, minimax_val)

                if alpha >= beta: break # prune if alpha >= beta
            return max_value
        
        else: #if minimizing player
            min_value = float('inf')

            for move in all_moves:
                if time.time() - start > self.time_limit:
                    raise TimeoutError
                board_copy = copy.deepcopy(board)
                execute_move(board_copy, move, opponent) #execute move on copy of board

                minimax_val = self.minimax_main(board_copy, depth-1, True, player, opponent, alpha, beta, start)
                min_value = min(min_value, minimax_val) #update min and beta
                beta = min(minimax_val, beta)

                if alpha>=beta: #prune if alpha>=beta
                    break
            return min_value


    def evaluate(self, board, player, opponent):

        #initial heuristic map
        heuristic_weight_map = {"corners": 1, "mobility": 1, "blocking": 1, "disk_count": 1}

        #evaluating game phase for different heuristics

        empty = (board==0).sum() #calculate the number of empty slots on the board

        #EARLY GAME
        if empty > board.size * 0.6:
            heuristic_weight_map["corners"] = 5
            heuristic_weight_map["mobility"] = 10
            heuristic_weight_map["blocking"] = 3
            heuristic_weight_map["disk_count"] = 1

        #MID GAME
        elif empty > board.size * 0.2:
            heuristic_weight_map["corners"] = 9
            heuristic_weight_map["mobility"] = 5
            heuristic_weight_map["blocking"] = 5
            heuristic_weight_map["disk_count"] = 3

        else:
            #LATE GAME

            heuristic_weight_map["corners"] = 15
            heuristic_weight_map["mobility"] = 2
            heuristic_weight_map["blocking"] = 5
            heuristic_weight_map["disk_count"] = 8

        #Corner heuristic from gpt greedy agent

        corner_heuristic = 0
        corners = [(0, 0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
        corner_score = sum(1 for corner in corners if board[corner] == player)
        corner_penalty = sum(1 for corner in corners if board[corner] == opponent)
        corner_heuristic = 10 * corner_score - 10 * corner_penalty

        #Mobility heuristic

        mobility_heuristic = 0
        agent_moves = len(get_valid_moves(board, player))
        opponent_moves = len(get_valid_moves(board, opponent))

        mobility_heuristic = agent_moves - opponent_moves

        #Blocking score heuristic

        blocking_heuristic = 0
        opponent_moves = get_valid_moves(board, opponent)

        for move in opponent_moves:
            board_copy = copy.deepcopy(board)
            execute_move(board_copy,move, opponent)

            #get corners and if there are corners for opponent, then block them by penalizing it
            corners = [(0, 0), (0, board.shape[1] - 1), (board.shape[0] - 1, 0), (board.shape[0] - 1, board.shape[1] - 1)]
            if any(board_copy[corner] == opponent for corner in corners):
                blocking_heuristic -= 20  # Penalized for allowing access to corners
            
        #Disc count heuristic 
        disk_count_heuristic = (board == player).sum() - (board == opponent).sum()

        #return sum of all weighted heuristics
        return ((heuristic_weight_map["corners"]*corner_heuristic)+
        (heuristic_weight_map["mobility"]*mobility_heuristic)+
        (heuristic_weight_map["blocking"]*blocking_heuristic)+
        heuristic_weight_map["disk_count"]*disk_count_heuristic)
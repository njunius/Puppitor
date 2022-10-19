import random
from math import sqrt
from math import log
import affecter

# A node in the game tree
# does not track turns unlike other implementations of MCTS
class Node:
    
    def __init__(self, move = None, parent = None, action_key_map = None):
        self.move = move # tuple of (action, modifier)
        self.parent_node = parent
        self.child_nodes = []
        self.reward = 0
        self.visits = 0
        self.untried_moves = action_key_map.get_moves() # future child nodes, list of (action, modifier) tuples
        
    # use the UCB1 formula to select a child node
    # formula values control the exploration vs exploitation
    def uct_select_child(self):
        selected_child_node = max(self.child_nodes, key = lambda c: c.reward/c.visits + sqrt(2 * log(self.visits)/c.visits))
        return selected_child_node
        
    # remove move from untried_moves and add a new child node for the move and return it
    def add_child(self, tried_move, action_key_map, prevailing_affect):
        node = Node(move = tried_move, parent = self, action_key_map = action_key_map)
        self.untried_moves.remove(tried_move)
        self.child_nodes.append(node)
        return node
        
    # update this node with an additional visit and add a specified result to the node's reward
    def update(self, result):
        self.visits += 1
        self.reward += result
        
# conduct a UCT search for itermax iterations from the given rootstate
# returns the best move from the rootstate
def uct_think(root_affect_vector, action_key_map, character_affecter, goal_emotion, itermax, rollout_max = 50):

    rootnode = Node(action_key_map = action_key_map)
    
    for iteration in range(itermax):
        node = rootnode
        affect_vector = root_affect_vector.copy()
        action = ''
        modifier = ''
        
        # selection
        while not node.untried_moves and node.child_nodes: # node is fully expanded and non-terminal
            node = node.uct_select_child()
            action, modifier = _update_affect_state(node.move, affect_vector, character_affecter)
        
        # expansion
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            action, modifier = _update_affect_state(move, affect_vector, character_affecter)

            node = node.add_child(move, action_key_map, affecter.get_prevailing_affect(character_affecter, affect_vector))
        
        # rollout until we find an affect_vector where goal_emotion has a higher value relative to the other affects or have done N simulations and still not expressed the goal emotion
        rollout_length = 0
        while affecter.evaluate_affect_vector(character_affecter, affect_vector, goal_emotion) < 0 and rollout_length < rollout_max:
            action, modifier = _update_affect_state(random.choice(action_key_map.get_moves()), affect_vector, character_affecter)

            rollout_length += 1
            
        # backpropogate
        while node != None: # backpropogate from the expanded node towards the root node
            node.update(affecter.evaluate_affect_vector(character_affecter, affect_vector, goal_emotion))
            node = node.parent_node
        
    return max(rootnode.child_nodes, key = lambda c: c.reward/c.visits).move
            
def _update_affect_state(move, affect_vector, character_affecter):
    action, modifier = move
    character_affecter.update_affect(affect_vector, action, modifier)
    
    return(action, modifier)
    
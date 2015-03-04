class Node(object):

    def __init__(self, pos, token=None):
        self.pos = pos
        self.token = token
        
class RingNode(Node):

    def __init__(self, pos, token=None, left = None, right = None, center = None):
        super(RingNode, self).__init__(pos, token)
        self.left = left
        self.right = right
        self.center = center

class CenterNode(Node):

    def __init__(self, pos, token=None, ring=None):
        super(Node, self).__init__(pos, token)
        self.ring = ring

class Token(object):

    def __init__(self, player):
        self.player = player

class Board(object):

    def __init__(self, nodes = []):
        self.nodes = nodes

    def add_node(self, node):
        self.nodes.append(node)

if __name__ == '__main__':

    board = Board()
    for i in range(9):
        n = Node()
        n.id = i
        board.add_node(n)
    for node in board.nodes:
        print node.id
    print board.nodes
    for i in range(1,9):
        n = board.nodes[i]
        n.add_neighbor(board.nodes[0])
        if i == 1:
            n.add_neighbor(board.nodes[8])
        else:
            n.add_neighbor(board.nodes[i-1])
        board.nodes[0].add_neighbor(board.nodes[i])
    print board.nodes[0].neighbors
    

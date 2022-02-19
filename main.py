import random
import copy
import itertools


class BoxException(Exception):
    pass

DEFAULT_MOVES = [1] * 1000

class Box:
    def __init__(self, num, layers):
        self.num = num
        self.layers = layers

    def mix_in(self, box):
        if self.is_full():
            raise BoxException

        piece = box.get_top_piece()
        if len(self.layers) + len(piece) > 4:
            raise BoxException
        self.layers.extend(box.get_top_piece())
        box.remove_top()

    def remove_top(self):
        if len(self.get_top_piece()) == len(self.layers):
            self.layers = []
        else:
            self.layers = self.layers[0:len(self.layers) - len(self.get_top_piece())]

    def can_mix(self, box):
        if len(self.layers) == 4:
            return False
        if len(box.layers) == 0:
            return False
        if len(self.layers + box.get_top_piece()) > 4:
            return False
        # Don't allow moving a tube that's filled with 4 colors already.
        if len(box.get_top_piece()) == 4:
            return False
        if len(self.get_top_piece()) and self.get_top_piece()[0] != box.get_top_piece()[0]:
            return False
        # Don't move a tube of one color to an empty tube.
        if len(box.layers) == len(box.get_top_piece()) and len(self.layers) == 0:
            return False
        return True

    def get_top_piece(self):
        if not self.layers:
            return []

        curr_offset = len(self.layers) - 1
        piece = [self.layers[curr_offset]]
        while curr_offset > 0:
            curr_offset -= 1
            if piece[0] != self.layers[curr_offset]:
                break
            piece.append(self.layers[curr_offset])

        return piece

    def is_full(self):
        return len(self.get_top_piece()) == 4

    def is_empty(self):
        return len(self.layers) == 0

class Boxes:
    def __init__(self, boxes):
        self.boxes = boxes
        self.loop_counter = 0

    def get_possible_moves(self):
        possible_moves = set()
        for x, y in itertools.combinations(self.boxes, 2):
            if x.can_mix(y):
                possible_moves.add((x.num, y.num))
            if y.can_mix(x):
                possible_moves.add((y.num, x.num))
        return possible_moves

    def move(self, x_num, y_num):
        x_box = self.boxes[x_num]
        y_box = self.boxes[y_num]
        x_box.mix_in(y_box)

    def move_until_blank_box(self, moves=None, depth=0):
        depth += 1
        if depth == 1:
            self.loop_counter = 0
        self.loop_counter += 1
        current_boxes = copy.deepcopy(self.boxes)
        moves = copy.deepcopy(moves) or []
        good_moves = []
        possible_moves = self.get_possible_moves()
        if not possible_moves:
            if self.is_empty_box(self.boxes):
                good_moves.append(moves)
                return good_moves
            else:
                return good_moves
        for move in possible_moves:
            self.move(*move)
            moves.append(move)
            if self.is_empty_box(self.boxes):
                good_moves.append(copy.deepcopy(moves))
                self.boxes = copy.deepcopy(current_boxes)
                moves.pop()
                continue
            # Remove any arrays, in arrays, in arrays.
            recursive_moves = self.move_until_blank_box(moves, depth=depth)
            for value in recursive_moves:
                good_moves.append(value)
            self.boxes = copy.deepcopy(current_boxes)
            moves.pop()
            if self.loop_counter > 10000 and good_moves:
                return good_moves

        return good_moves

    def is_empty_box(self, boxes):
        for box in boxes:
            if box.is_empty():
                return True
        return False

    def print(self, boxes):
        for box in boxes:
            print(box.num, " -- ", *box.layers)

def build_moves(count, boxes):
    return [random.sample(boxes, 2) for _ in range(count)]

PE = 1
BL = 2
PI = 3
TU = 4
BR = 5
OR = 6
RE = 7
YE = 8
DG = 9  # Dark Green
LG = 10  # Light Green
GR = 11  # Gray
PU = 12
AQ = 13  # Aqua
FO = 14 # Forest Green
PL = 15 # Plum purple

original_boxes = [
    Box(0, [DG, BR, TU, GR]),
    Box(1, [PU, PU, LG]),
    Box(2, [FO, AQ, LG]),
    Box(3, [FO, TU, PE, AQ]),
    Box(4, [BL, BL, AQ, LG]),
    Box(5, [BR, DG, BR, FO]),
    Box(6, [PE]),
    Box(7, [BL, TU, DG, BL]),
    Box(8, [FO, GR]),
    Box(9, [DG, GR, PE]),
    Box(10, [PE, PU, BR, GR]),
    Box(11, [TU, PU, LG, AQ]),
    # Box(12, []),
    # Box(13, []),
    ]

def sanity_check_boxes(boxes):
    color_count = {}
    for box in boxes:
        for layer in box.layers:
            color_count.setdefault(layer, 0)
            color_count[layer] += 1

    for key, value in color_count.items():
        if value != 4:
            print("Color " + str(key) + " only has " + str(value) + " layers")

def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

boxes = Boxes(original_boxes)
original_boxes = copy.deepcopy(boxes)
all_moves = []

sanity_check_boxes(boxes.boxes)
while True:
    moves = boxes.move_until_blank_box()
    if not len(moves[0]):
        break
    for x, y in min(moves):
        print("Move " + str(y+1) + " to " + str(x+1))
        boxes.move(x, y)
    print("")
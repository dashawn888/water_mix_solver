import copy
import itertools


class VialException(Exception):
    pass


class Vial:
    def __init__(self, num, layers):
        self.num = num
        self.layers = layers

    def mix_in(self, vial):
        if self.is_full():
            raise VialException
        piece = vial.get_top_piece()
        if len(self.layers) + len(piece) > 4:
            raise VialException
        self.layers.extend(vial.get_top_piece())
        vial.remove_top()

    def remove_top(self):
        layers_len = len(self.layers)
        top_piece_len = len(self.get_top_piece())
        if top_piece_len == layers_len:
            self.layers = []
        else:
            self.layers = self.layers[0 : layers_len - top_piece_len]

    def can_mix(self, vial):
        if len(self.layers) == 4:
            return False
        # Don't allow moving a vial that's filled with 4 colors already.
        if len(vial.get_top_piece()) == 4:
            return False
        if len(vial.layers) == 0:
            return False
        if len(self.layers + vial.get_top_piece()) > 4:
            return False
        if len(self.get_top_piece()) and self.get_top_piece()[0] != vial.get_top_piece()[0]:
            return False
        # Don't move a vial of one color to an empty vial.
        if len(vial.layers) == len(vial.get_top_piece()) and len(self.layers) == 0:
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


class Vials:
    def __init__(self, vials):
        self.vials = vials
        self.max_depth = 100000

    def get_possible_moves(self):
        possible_moves = set()
        for x, y in itertools.combinations(self.vials, 2):
            if x.can_mix(y):
                possible_moves.add((x.num, y.num))
            if y.can_mix(x):
                possible_moves.add((y.num, x.num))
        return possible_moves

    def move(self, x_num, y_num):
        self.vials[x_num].mix_in(self.vials[y_num])

    def move_until_empty_vial(self, moves=None, depth=0):
        depth += 1
        if depth == 1:
            self.max_depth = 100000
        if depth > self.max_depth:
            return []
        current_vials = copy.deepcopy(self.vials)
        moves = moves or []
        good_moves = []
        possible_moves = self.get_possible_moves()
        if not possible_moves:
            if is_empty_vial(self.vials):
                good_moves.append(moves)
                return good_moves
            else:
                return good_moves
        for move in possible_moves:
            self.move(*move)
            moves.append(move)
            if is_empty_vial(self.vials):
                good_moves.append(copy.copy(moves))
                self.vials = copy.deepcopy(current_vials)
                moves.pop()
                continue
            recursive_moves = self.move_until_empty_vial(moves, depth=depth)
            for value in recursive_moves:
                good_moves.append(value)
                # Since we have a move cancel out of checking any moves that are longer than this one.
                self.max_depth = len(value) - 1
            self.vials = copy.deepcopy(current_vials)
            moves.pop()
            if depth > self.max_depth:
                return good_moves
        return good_moves


def is_empty_vial(vials):
    for vial in vials:
        if vial.is_empty():
            return True
    return False


def sanity_check_vials(vials):
    color_count = {}
    for vial in vials:
        for layer in vial.layers:
            color_count.setdefault(layer, 0)
            color_count[layer] += 1
    problem = False
    for key, value in color_count.items():
        if value != 4:
            print("Color " + str(key) + " only has " + str(value) + " pieces")
            problem = True
    return problem


def solve(puzzle):
    vials = Vials(puzzle)
    if sanity_check_vials(vials.vials):
        return
    while True:
        try:
            moves = vials.move_until_empty_vial()
        except VialException:
            print("Probably an invalid setup.")
            break
        if not moves:
            print("Puzzle is not solvable!")
            break
        if not len(moves[0]):
            break
        for x, y in min(moves):
            print("Move " + str(y + 1) + " to " + str(x + 1))
            vials.move(x, y)
        print("")

PE = 1  # Peach
BL = 2  # Blue
PI = 3  # Pink
TU = 4  # Turquoise
BR = 5  # Brown
OR = 6  # Orange
RE = 7  # Red
YE = 8  # Yellow
DG = 9  # Dark Green
LG = 10  # Light Green
GR = 11  # Gray
PU = 12  # Purple
AQ = 13  # Aqua
FO = 14  # Forest Green
PL = 15  # Plum purple

if __name__ == "__main__":
    # Put all the puzzle pieces here. If there are more vials add more.
    original_vials = [
        Vial(0, [DG, BR, TU, GR]),
        Vial(1, [PU, PU, LG]),
        Vial(2, [FO, AQ, LG]),
        Vial(3, [FO, TU, PE, AQ]),
        Vial(4, [BL, BL, AQ, LG]),
        Vial(5, [BR, DG, BR, FO]),
        Vial(6, [PE]),
        Vial(7, [BL, TU, DG, BL]),
        Vial(8, [FO, GR]),
        Vial(9, [DG, GR, PE]),
        Vial(10, [PE, PU, BR, GR]),
        Vial(11, [TU, PU, LG, AQ]),
    ]
    solve(original_vials)

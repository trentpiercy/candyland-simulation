import random, statistics

CARD_COLORS = ["r", "p", "y", "b", "o", "g"]
CARD_TYPES = ["s"]*9 + ["d"]*2
SPECIAL_CARDS = ["plumpy", "mint", "gumdrop", "nutbread", "lolly", "frostine"]

def shuffle_deck():
    DECK = [(color, single_double) for color in CARD_COLORS for single_double in CARD_TYPES] + [(special, "s") for special in SPECIAL_CARDS]
    random.shuffle(DECK)
    return DECK

BOARD = {1:"r", 2:"p", 3:"y", 4:"b", 5:"o", 6:"g", 7:"r", 8:"p", 9:"plumpy", 
         10:"y", 11:"b", 12:"o", 13:"g", 14:"r", 15:"p", 16:"y", 17:"b", 18:"mint", 19:"o",
         20:"g", 21:"r", 22:"p", 23:"y", 24:"b", 25:"o", 26:"g", 27:"r", 28:"p", 29:"y",
         30:"b", 31:"o", 32:"g", 33:"r", 34:"p", 35:"y", 36:"b", 37:"o", 38:"g", 39:"r",
         40:"p", 41:"y", 42:"b", 43:"gumdrop", 44:"o", 45:"g", 46:"r", 47:"p", 48:"y", 49:"b",
         50:"o", 51:"g", 52:"r", 53:"p", 54:"y", 55:"b", 56:"o", 57:"g", 58:"r", 59:"p",
         60:"y", 61:"b", 62:"o", 63:"g", 64:"r", 65:"p", 66:"y", 67:"b", 68:"o", 69:"g",
         70:"r", 71:"p", 72:"y", 73:"b", 74:"o", 75:"nutbread", 76:"g", 77:"r", 78:"p", 79:"y",
         80:"b", 81:"o", 82:"g", 83:"r", 84:"p", 85:"y", 86:"b", 87:"o", 88:"g", 89:"r",
         90:"p", 91:"y", 92:"n", 93:"o", 94:"g", 95:"r", 96:"lolly", 97:"p", 98:"y", 99:"b",
         100:"o", 101:"g", 102:"r", 103:"p", 104:"frostine", 105:"y", 106:"b", 107:"o", 108:"g", 109:"r",
         110:"p", 111:"y", 112:"b", 113:"o", 114:"g", 115:"r", 116:"p", 117:"y", 118:"b", 119:"o",
         120:"g", 121:"r", 122:"p", 123:"y", 124:"b", 125:"o", 126:"g", 127:"r", 128:"p", 129:"y",
         130:"b", 131:"o", 132:"g", 133:"r", 134:"rpybog", 135:"rpybog"
         ### 135 is for the case of drawing a double at one of the last few spaces
        }

def generate_board():
    b = CARD_COLORS * 21
    b += "r"

    special_items = ["plumpy", "mint", "gumdrop", "nutbread", "lolly", "frostine", "rpybog", "rpybog"]
    special_locations = [8, 17, 42, 75, 96, 104, 133, 134]

    for i in range(8):
        b.insert(special_locations[i], special_items[i])

    return b


BOARD = generate_board()

space = 10

for i in enumerate(BOARD):
    if i[0] > space:
        print(i)

class Player():
    def __init__(self):
        self.board_space = 0
        self.win = False
        self.skip_turn = False
        self.draw = ()
    
    def move(self):
        for i in BOARD.items():
            if i[0] > self.board_space and self.draw[0] in i[1]:
                return i[0]

    def play_card(self, DECK):
        self.draw = DECK.pop()
        
        # Color Card Draw
        if len(self.draw[0]) == 1:
            self.board_space = self.move()
            if self.draw[1] == "d":
                self.board_space = self.move()

        # Special Card Draw
        else:
            for i in BOARD.items():
                if i[1] == self.draw[0]:
                    self.board_space = i[0]
                    break
        
        if self.board_space == 134 or self.board_space == 135:
            self.win = True
        elif self.board_space == 48 or self.board_space == 86 or self.board_space == 121:
            self.skip_turn = True
        elif self.board_space == 5:
            self.board_space = 59
        elif self.board_space == 34:
            self.board_space = 47

        return DECK

### TESTING
def test():
    p = Player()
    draw = [("r", "d")]
    p.play_card(draw)
    assert p.board_space == 7

    p = Player()
    draw = [("frostine", "s")]
    p.play_card(draw)
    assert p.board_space == 104

    p = Player()
    draw = [("p", "s")]
    p.board_space = 30
    p.play_card(draw)
    assert p.board_space == 47

    p = Player()
    draw = [("o", "s")]
    p.play_card(draw)
    assert p.board_space == 59

    p = Player()
    p.board_space = 130
    draw = [("b", "d")]
    p.play_card(draw)
    assert p.win == True

    p = Player()
    p.board_space = 130
    draw = [("b", "s")]
    p.play_card(draw)
    assert p.win == True

    p = Player()
    p.board_space = 45
    draw = [("y", "s")]
    p.play_card(draw)
    assert p.board_space == 48 and p.skip_turn == True


# test()

def play(loops):
    game_len_counter = []
    for _ in range(loops):
        add_counter = True
        p1 = Player()
        p2 = Player()
        DECK = shuffle_deck()
        
        while not p1.win and not p2.win:
            # print("P1: " + str(p1.board_space) + " " + str(p1.draw))
            # print("P2: " + str(p2.board_space) + " " + str(p2.draw))
            if DECK == []:
                game_len_counter += [-1]
                add_counter = False
                break

            if not p1.skip_turn:
                DECK = p1.play_card(DECK)
                if p1.win:
                    break
            else:
                p1.skip_turn = False

            if DECK == []:
                game_len_counter += [-1]
                add_counter = False
                break

            if not p2.skip_turn:
                DECK = p2.play_card(DECK)
            else:
                p2.skip_turn = False
            
        if add_counter:
            game_len_counter += [72-len(DECK)]

    return game_len_counter

n = 10000
# x = play(n)


def stats(x, n, players):
    all_drawn = 0
    x_final = []

    for i in x:
        if i == -1:
            all_drawn += 1
        else:
            x_final.append(i)

    print("Maximum plays: {0}\nMinimum: {1}\nAverage: {2}\nMedian: {3}\nStandard Deviation: {4}"
          .format(max(x_final), min(x_final), statistics.mean(x_final), statistics.median(x_final), statistics.stdev(x_final)))

    print("In {0} games out of {1} ({2}%) all cards were drawn. ({3} Players)".format(all_drawn, n, (all_drawn/n)*100, players))

# stats(x, n, 2)
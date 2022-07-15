import random
from collections import deque
from operator import countOf


def player_determine(challenge_player):
    if challenge_player == "Player One":
        challenge_player = p1
        opponent = p2
        return challenge_player, opponent
    if challenge_player == "Player Two":
        challenge_player = p2
        opponent = p1
        return challenge_player, opponent


def compare_bids(challenge_player):
    challenge_player, opponent = player_determine(challenge_player)
    count, face = opponent.bids[0], opponent.bids[1]
    challenger_count, challenger_face = challenge_player.bids[0], challenge_player.bids[1]

    if challenger_face < face:
        print(f"You can not bid lower face than the previous player!")
        return False
    elif challenger_face == face and challenger_count <= count:
        print(f"You can not bid lower or same count than the previous player!")
        return False
    else:
        return True


class Player:
    def __init__(self, name):
        self.name = name
        self.dices = 5
        self.dices_list = []
        self.bids = []
        self.wild = [5, 1]
        self.is_winner = False

    def dice_generator(self):
        n = random.randint(1, 6)
        return n

    def player_dices(self):
        self.dices_list = [self.dice_generator() for i in range(self.dices)]
        return self.dices_list

    def bid(self):
        print("Bid number:")
        bid_number = int(input())
        if bid_number < 0 or bid_number > 5:
            print(f"You can not bid lower count than 0 and bigger than 5!")
            return False
        print("Bid of face:")
        bid_face = int(input())
        if bid_face < 0 or bid_face > 6:
            print(f"You can not bid lower face than 0 and bigger than 6!")
            return False
        self.bids = [bid_number, bid_face]
        if not compare_bids(self.name):
            return False
        return f"{self.name} bid {bid_number} of {bid_face}"


p1 = Player("Player One")
p1.player_dices()
p1.bids = p1.wild
p2 = Player("Player Two")
p2.player_dices()
p2.bids = p2.wild
moves = deque([p1, p2])


def new_round():
    p1.player_dices()
    p1.bids = p1.wild
    p2.player_dices()
    p2.bids = p2.wild
    return f"Player one dices {', '.join(str(i) for i in p1.dices_list)}.\n" \
           f"Player two dices {', '.join(str(i) for i in p2.dices_list)}."


def challenge(challenge_player, table_dices):
    challenge_player, opponent = player_determine(challenge_player)
    count, face = opponent.bids[0], opponent.bids[1]
    found = countOf(table_dices, face)

    if found < count:
        challenge_player.is_winner = True
        opponent.dices -= 1
        moves.append(challenge_player)
        return f"{challenge_player.name} won the round!"
    else:
        challenge_player.dices -= 1
        moves.appendleft(challenge_player)
        return f"{challenge_player.name} lost the round!"


while p1.dices_list and p2.dices_list:
    all_dices = p1.dices_list + p2.dices_list
    player = moves.popleft()
    print(f"{player.name} bid or challenge?")
    choice = input()
    if choice == "challenge":
        print(challenge(player.name, all_dices))
        print(new_round())
    elif choice == "bid":
        if not player.bid():
            moves.appendleft(player)
        moves.append(player)
    else:
        print("Invalid input!")
        moves.appendleft(player)

if p1.dices_list:
    print(f"The winner is {p1.name}")
else:
    print(f"The winner is {p2.name}")

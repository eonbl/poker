# Poker simulator to determine probability of a certain hand occurring, assuming all hands go to showdown

import argparse
import random
from collections import defaultdict


class Card:
    def __init__(self, card_number):
        self.rank = CARD_RANK[int(card_number / 4)]
        self.suit = CARD_SUIT[card_number % 4]

    def __str__(self):
        return self.rank + self.suit

    def __repr__(self):
        return str(self)


HAND_RANK = {'royal flush': 0, 'straight flush': 1, 'four of a kind': 2, 'full house': 3, 'flush': 4, 'straight': 5,
             'three of a kind': 6, 'two pair': 7, 'one pair': 8, 'no pair': 9, 'high card': 9}
CARD_RANK = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
CARD_SUIT = ['c', 'd', 'h', 's']


def hand_exists(pockets, community, hand_rank):
    community_rank_count = defaultdict(int)
    community_suit_count = defaultdict(int)
    for card in community:
        community_rank_count[card.rank] += 1
        community_suit_count[card.suit] += 1

    # check full house
    if hand_rank == 3:
        # if a full house exists on the board
        if max(community_rank_count.values()) == 3 and min(community_rank_count.values()) == 2:
            return True
        # otherwise, check existence of full house for each player
        for pocket in pockets:
            player_rank_count = defaultdict(int, community_rank_count)
            for card in pocket:
                player_rank_count[card.rank] += 1
            if max(player_rank_count.values()) == 3:
                for count in player_rank_count.values():
                    if count == 2:
                        return True
    else:
        raise ValueError('Sorry, hands other than full house have not yet been implemented')

    return False


def compute_prob(n, hand, cumulative, nsims):
    if n < 0:
        raise ValueError('number of players must be at least 0')
    if hand not in HAND_RANK:
        raise ValueError(f'hand must be one of: {list(HAND_RANK.keys())}')
    if hand != "full house" or cumulative:
        print('Sorry, hands other than full house have not yet been implemented')
        return

    count = 0
    for r in range(nsims):
        # Cards are ordered 0-51 by rank (2 through A) and within each rank by suit (club < diamond < heart < spade)
        cards = random.sample(range(52), 5 + 2 * n)
        pockets = [[Card(cards[2 * i]), Card(cards[2 * i + 1])] for i in range(n)]
        community = [Card(x) for x in cards[-5:]]

        if cumulative:
            for hand_rank in range(HAND_RANK[hand]):
                if hand_exists(pockets, community, hand_rank):
                    count += 1
                    break
        else:
            if hand_exists(pockets, community, HAND_RANK[hand]):
                count += 1

    return count / nsims


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Poker simulator to determine probability of a certain hand occurring,'
                                                 ' assuming all hands go to showdown')
    parser.add_argument('-n', '--players', type=int, help='number of players (default: 2)', default=2)
    parser.add_argument('--hand', help='hand name (default: "full house")', default="full house")
    parser.add_argument('-c', '--cumulative', dest='cumulative', action='store_true',
                        help='Calculate probability for HAND or better')
    parser.add_argument('-nc', '--no-cumulative', dest='cumulative', action='store_false',
                        help='Calculate probability for HAND specifically')
    parser.add_argument('--nsims', type=int, help='number of simulations (default: 100000)', default=100000)
    args = parser.parse_args()
    probability = compute_prob(n=args.players, hand=args.hand, cumulative=args.cumulative, nsims=args.nsims)
    print(f"{round(probability * 100, 2)}%")

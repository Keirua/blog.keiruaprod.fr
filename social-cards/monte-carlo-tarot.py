wins = np.array([0 for i in range(0, nb_cards+1)])

def compute_card_probability(card_value):
    deck = [i for i in range(0, nb_cards+1)]
    deck.remove(card_value)
    # monte carlo loop: run many hands, the law of big
    # numbers will do the rest
    for _ in range(nb_iterations):
        # play a hand, look for the winner
        random.shuffle(deck)

        other_players = deck[0:nb_players-1]
        if card_value > max(other_players):
            wins[card_value]+=1

# run the simulation for all the cards
for card_value in range(0, nb_cards+1):
    compute_card_probability(card_value)

wins = wins/float(nb_iterations)
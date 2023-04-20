import random

def draw_card(deck_counts):
    valid_indexes = [i for i, count in enumerate(deck_counts) if count > 0]
    if not valid_indexes:
        return None, deck_counts
    card_value = random.choice(valid_indexes) + 1
    deck_counts[card_value - 1] -= 1
    return card_value, deck_counts

def print_state(state):
    total, dealer_card, deck_counts = state
    if deck_counts is not None:
        for i, count in enumerate(deck_counts):
            print(f"{i + 1} deck{'s' if count != 1 else ''} with {count} cards each")

def play_game(multiplicity, threshold, peek_cost):
    deck_counts = [multiplicity] * (threshold - 1)
    total = 0
    peek_index = None
    while True:
        state = (total, peek_index, tuple(deck_counts))
        print_state(state)
        if total >= threshold:
            print("You exceeded the threshold!")
            return 0
        if not any(deck_counts):
            print("The deck is empty!")
            return total
        action = input("Take, peek, or quit? ").strip().lower()
        if action == "take":
            card_value, deck_counts = draw_card(deck_counts)
            if card_value is None:
                print("The deck is empty!")
                return total
            total += card_value
            if total >= threshold:
                print_state((total, None, None))
                print("You exceeded the threshold!")
                return 0
        elif action == "peek":
            if peek_index == 1:
                print("You cannot peek twice in a row!")
                total -= peek_cost
            else:
                card_value, _ = draw_card(deck_counts)
                if card_value is None:
                    print("The deck is empty!")
                    return total
                peek_index = random.choice(range(len(deck_counts)))
        elif action == "quit":
            return total
        else:
            print("Invalid action!")

if __name__ == "__main__":
    threshold = int(input("Enter threshold (num cards): "))
    multiplicity = int(input("Enter card multiplicity (palo): "))
    peek_cost = int(input("Enter peek cost (win): "))
    total = play_game(multiplicity, threshold, peek_cost)
    print(f"Final total: {total}")

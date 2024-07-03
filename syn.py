import random

class Deck:
  def __init__(self):
    self.cards = list(range(52))
    random.shuffle(self.cards)
    self.cards_left = 52

  def deal_card(self):
    if self.cards_left == 0:
      print("No more cards in the deck")
      return
    
    card_num = self.cards[-1]
    card = calculate_card(card_num)
    self.cards.pop()
    self.cards_left = self.cards_left - 1
    return card
    
  def shuffle(self):
    self.cards = list(range(52))
    random.shuffle(self.cards)
    self.cards_left = 52

# returns the card giving a card number (0-51)
def calculate_card(card_num):
    suit_dict = {0 : 'S', 1 : 'H', 2 : 'C', 3 : 'D'}
    suit = int(card_num / 13)
    suit_char = suit_dict[suit]
    card = card_num % 13 + 1
    if (card == 1):
      card_char = 'A'
    elif (card == 10):
      card_char = 'T'
    elif (card == 11):
      card_char = 'J'
    elif (card == 12):
      card_char = 'Q'
    elif (card == 13):
      card_char = 'K'
    else:
      card_char = str(card)
    return card_char + '-' + suit_char

def print_table(table, dealer):
  for i in range(0, len(table)):
    if (i == dealer):
      print("Dealer: " + table[i])
    else:
      print(table[i])

# finds the next player to the left who is not out
def find_next_player(table, prev_player):
  offset = 1
  while (table[prev_player + offset] == 'X'):
    
    offset = offset + 1
  return prev_player + offset

# finds the next dealer to the left who is not out
def find_next_dealer(table, dealer):
  offset = 1
  while (table[dealer - offset] == 'X'):
    offset = offset + 1
  return dealer - offset

# elimate the players wiht the lowest hand at the table
def elimate_player(table):
  min_card = 13
  cards = {'A' : 1, 'T' : 10, 'J' : 11, 'Q' : 12, 'K' : 13}
  for i in range(len(table)):
    if table[i][0] == 'X':
      continue
    card = table[i][0];
    if (card in "ATJQK"):
      card = cards[card]
    if int(card) < int(min_card):
      min_card = int(card)

  num_players_elimated = 0;
  for i in range(len(table)):
    if table[i][0] == 'X':
      continue
    card = table[i][0];
    if (card in "ATJQK"):
      card = cards[card]
    if int(card) == int(min_card):
      table[i] = 'X'
      num_players_elimated = num_players_elimated + 1
      
  return num_players_elimated

# simulate one round of SYN
def simulate_round(table, num_players_left, deck, dealer):
  # deal each player a card
  for i in range(len(table)):
    if (table[i] != 'X'):
      table[i] = deck.deal_card()
  
  # start with left of dealer (dealer + 1) and swap if card is <= 6
  prev_player = find_next_player(table, -1) - 1
  
  recently_swapped = False
  
  for i in range(num_players_left - 1):
    # find next person in play
    player = find_next_player(table, prev_player)
    

    # swap if card is <= 6
    if (table[player][0] == 'A' or table[player][0] <= '6'):
      
      # find next person in play
      next_player = find_next_player(table, player)
      
      # check if the current player prevously swapped with someone with a lower card
      if (recently_swapped):
        if (table[player][0] > table[prev_player][0] or table[prev_player][0] == 'A'):
          recently_swapped = False
          prev_player = player
          continue
      
      # check if next players card is a king
      if (table[next_player][0] == 'K'):
        recently_swapped = False
        prev_player = player
        continue
      
      # swap card
      temp = table[next_player]
      table[next_player] = table[player]
      table[player] = temp
      recently_swapped = True
    else:
      recently_swapped = False
    
    prev_player = player
  
  # if dealer has <6 swap with deck
  if (table[dealer][0] == 'A' or table[dealer][0] <= '6'):
      # if dealer was recently swaped with a higher card, don't swap
      if not (recently_swapped and (table[player][0] > table[prev_player][0] or table[prev_player][0] == 'A')):
        table[dealer] = deck.deal_card()

  # elimate lowest players and updated players remaining
  num_players_left = num_players_left - elimate_player(table)

  # make new dealer if needed
  if (table[dealer] == 'X' and num_players_left != 0):
    dealer = find_next_dealer(table, dealer)
    
  return num_players_left, dealer
  
def play_game():
  playercount = 8
  deck = Deck()
  
  if (playercount < 2):
    print("Silly, you need at least 2 players")
    return

  # table is a list of players with a number (0-51) repersenting the card they have
  # the dealer is at last position in table
  # action starts at first poistion in table
  table = [-1] * playercount
  dealer = playercount - 1
  num_players_left = playercount
  
  while (num_players_left > 1):
    # check if deck needs to be shuffled
    if (deck.cards_left > num_players_left):
      num_players_left, dealer = simulate_round(table, num_players_left, deck, dealer)
    else:
      deck.shuffle()
  
  # print_table(table, dealer)
  # print("Congraulation player: " + str(dealer) + " you won!")
  return dealer

def main():
  num_games = 10000
  
  # dealer starts at position 7, left of dealer starts at position 0
  positions = [0] * 8
  
  # simulate games
  for i in range(num_games):
    winner = play_game()
    positions[winner] = positions[winner] + 1
  
  # output results
  for i in range(8):
    print(str(i) + ": " + str(positions[i]))

if __name__ == '__main__':
  main()
  print("Thanks for Playing!")
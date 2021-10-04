import random
import time

# Creates the possible list of card numbers and suit names
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
suits = ["spades", "hearts", "diamonds", "clubs"]

# Card object class
class card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit


# Returns a card with a random suit and number
def getRandomCard():
    myCard = card(random.choice(numbers), random.choice(suits))

    return myCard


# Pulls a random card from a hand or deck.
def getCard(deck):
    cardNumber = random.randint(0, len(deck) - 1)

    card = deck[cardNumber]
    deck.remove(card)

    return card


# Places a card back into a deck. Don't forget to shuffle.
def putCard(card, deck):
    deck.append(card)


# Returns the name of the card as a string
def readCard(card):
    number = card.number
    suit = card.suit

    if number < 2 or number > 10:
      face = {
      1 : "ace",
      11 : "jack",
      12 : "queen",
      13 : "king"
      }
      name = face[number] + " of " + suit
    else:
      name = str(number) + " of " + suit

    return name


# Returns all of the cards in a deck or hand as a string
def readHand(hand):
    cards = ""
    for i in hand:
        cards = cards + " - " + readCard(i) + "\n"

    return cards


# Adds together the value of all the cards in a hand or deck according to the rules of blackjack
def addCards(hand):
    aces = False
    # Two values are returned in the case that there is an ace in the hand
    total = [0, 0]
    for i in hand:
        # If the card is an ace, it should be counted as either 1 or 11, so long as another ace has not already invoked this rule
        if i.number == 1 and aces == False:
            aces = True
            total[0] += 11
            total[1] += 1
            if total[0] > 21:
                total[0] -= 10
                aces = False
        # All face cards are counted as 10 in blackjack
        elif i.number > 10:
            total[0] += 10
            total[1] += 10
            if total[0] > 21 and aces == True:
                total[0] -= 10
                aces = False
        else:
            total[0] += i.number
            total[1] += i.number
            if total[0] > 21 and aces == True:
                total[0] -= 10
                aces = False

    return total


# Returns the score of a hand as a string
def readScore(hand):
    # If the two values returned are the same, only one is printed
    if addCards(hand)[0] == addCards(hand)[1]:
        score = str(addCards(hand)[0])
    # If the higher value is 21, only the higher value is printed
    elif addCards(hand)[0] == 21:
        score = str(addCards(hand)[0])
    # Otherwise, both values are printed
    else:
        score = str(addCards(hand)[0]) + " or " + str(addCards(hand)[1])

    return score


# Creates a deck of 52 cards with no duplicates
def makeDeck():
    deck = []

    for i in range(13):
        deck.append(card(i + 1, suits[0]))

    for i in range(13):
        deck.append(card(i + 1, suits[1]))

    for i in range(13):
        deck.append(card(i + 1, suits[2]))

    for i in range(13):
        deck.append(card(i + 1, suits[3]))

    random.shuffle(deck)
    return deck


# Main function starts here
game = True
chips = 100
print("Let's play Blackjack!")

while game == True:
  done = False
  bet = 0
  blackjack = False
  bust = False
  deck = makeDeck()
  deck.sort(key=lambda x: x.number)
  deck.sort(key=lambda x: x.suit)

  hand1 = [getCard(deck), getCard(deck)]
  hand2 = [getCard(deck)]

  time.sleep(1)
  bet = input("You have " + str(chips) +
              " chips. How much do you want to bet? ")

  if bet.isnumeric():
      bet = int(bet)
  else:
      while not bet.isnumeric():
          bet = input()
      bet = int(bet)
  while int(bet) < 1 or bet > chips:
      bet = int(input())

  print("\n____________________________________\nThe dealer starts with: ")
  time.sleep(1)
  print(" - " + readCard(hand2[0]))
  time.sleep(1)
  print("The dealer's score is " + readScore(hand2))

  time.sleep(1)
  print("\nYou're cards are: ")
  time.sleep(1)
  print(" - " + readCard(hand1[0]))
  time.sleep(1)
  print(" - " + readCard(hand1[1]))
  time.sleep(1)
  print("Your score is " + readScore(hand1))

  # This is the player's turn
  while done == False:
      time.sleep(1)
      if (int(addCards(hand1)[0]) == 21):
          blackjack = True
          print("You got Blackjack! You win!")
          chips = chips + (bet * 2)
          break

      if (int(addCards(hand1)[0]) > 21):
          bust = True
          print("You Busted! The Dealer won...")
          chips = chips - bet
          break

      time.sleep(1)
      choice = input("Will you take another card? ").lower()

      while True:
          if (choice == "yes" or choice == "y" or choice == ""):
              newCard = getCard(deck)
              hand1.append(newCard)
              print("You got a " + readCard(newCard) +
                    ". Your score is now " + readScore(hand1))
              break
          if (choice == "no" or choice == "n"):
              done = True
              print("\nYou stand with a score of " + readScore(hand1) +
                    ".\nIt is now the dealer's turn.")
              break
          choice = input()
        
      time.sleep(2)

  print()

  # This is the dealer's turn
  while addCards(hand2)[0] < 18:
      if bust == True:
          break
      if blackjack == True:
          break

      newCard = getCard(deck)
      hand2.append(newCard)

      time.sleep(1)
      print("The dealer got a " + readCard(newCard) +
            ". Their score is now " + readScore(hand2))
      time.sleep(2)

      if int(addCards(hand2)[0]) == 21:
          print("The dealer got Blackjack! You lost...")
          chips = chips - bet
          break

      if int(addCards(hand2)[0]) > 21:
          print("The dealer busted! You won!")
          chips = chips + bet
          break

      if int(addCards(hand2)[0]) > 18:
          print("The dealer will stand now..")
          time.sleep(1)

          if int(addCards(hand1)[0]) > int(addCards(hand2)[0]):
              print("\nThe dealer finished with a score of " +
                    str(addCards(hand2)[0]) + ". \nYou had a score of " +
                    str(addCards(hand1)[0]) +
                    ". \nCongratulations! You win!")
              chips = chips + bet
          elif int(addCards(hand1)[0]) < int(addCards(hand2)[0]):
              print("\nThe dealer finished with a score of " +
                    str(addCards(hand2)[0]) + ". \nYou had a score of " +
                    str(addCards(hand1)[0]) + ". \nSorry. You lost...")
              chips = chips - bet
          else:
              print("\nThe dealer finished with a score of " +
                    str(addCards(hand2)[0]) +
                    ". \nYou also had a score of " +
                    str(addCards(hand1)[0]) + ". \nIt's a tie.")
          break

  if chips > 0:
      time.sleep(1)
      print("\n\nYou have " + str(chips) + " chips left")
      time.sleep(1)
      again = input("Would you like to play again? ").lower()
      while True:
          if again == "yes" or again == "y" or again == "":
              break
          if again == "no" or again == "n":
              game = False
              break
          again = input()
  else:
      time.sleep(1)
      print("\n\nYou have no chips left")
      game = False

time.sleep(1)
print("\nGame Over.")

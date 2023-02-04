class Hand():
    def __init__(self, user):
        self.user = user
        self.cardFaces = []
        self.cardValues = []

    def get_user(self):
        return self.user

    def set_card_values(self, cards):
        self.cardValues= cards

    def add_card_face(self, card):
        self.cardFaces.append(card)

    def add_card_value(self, card):
        self.cardValues.append(card)

    def get_card_values(self):
        return self.cardValues

    def get_card_faces(self):
        return self.cardFaces

    def remove_last_card(self):
        cardFace = self.cardFaces.pop()
        cardValue = self.cardValues.pop()
        return cardFace, cardValue
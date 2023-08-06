from typing import Dict

from vigilant import MonopolyBoard, Player, Dice


class MonopolyGame:
    def __init__(self):
        self.board = MonopolyBoard()
        self.players: Dict[Player] = []
        self.dice = Dice()
        self.dice.roll()

    def addPlayer(self, new_player):
        if new_player not in self.players:
            self.players.append(new_player)
            new_player.log(
                f'{new_player.name} joined the game! We now have {len(self.players)} players')

    def playerTurn(self, player_index):
        current = self.players[player_index % len(self.players)]
        roll = self.dice.roll()
        self.movePlayer(current, roll)

    def movePlayer(self, current: Player, roll: int):
        new_location = self.board.to_valid_location(current.location + roll)
        is_doubles = self.dice.is_doubles()
        passed_go = new_location < current.location

        current.location = new_location
        current.log(
            f'{current.name} moved forward {roll} steps to {current.location}!')

        # check for rents
        property = self.board.get_property_at(current.location)
        print(f'-> {property}')
        if property.ownedby is None:
            self.maybe_buy(current, property)
        else:
            self.pay_rent(current, property)

        if passed_go:
            current.log(f'{current.name} passed GO!')

        if is_doubles:
            if current.doubles_count == 3:
                self.send_to_jail(current)
            else:
                print(f'{current.name} rolled doubles! They get a second turn')
                current.doubles_count += 1
                print('doubles count', current.doubles_count)
        else:
            current.doubles_count = 0

    def maybe_buy(self, player, property):
        player.log(f'{player.name} thinking about {property}')

        # always buy
        player.buy_property(property)

    def pay_rent(self, player, property):
        final_amount = property.rent

        if final_amount < player.money:
            player.subtract_money(final_amount)
            property.ownedby.add_money(final_amount)
            player.log(
                f'{player.name} paid {property.ownedby.name} {final_amount}')
            return True
        else:
            player.log(f'Not enough money')
            return False

    def send_to_jail(self, player):
        player.log(f'{player.name} in jail')

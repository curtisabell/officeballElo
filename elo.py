#!/usr/bin/python3
import pickle
import yaml
import io


class officeballPlayer:
    def __init__(self, ID=0, name='Name', elo=1000, nGames=0):
        self._ID = ID
        self._name = name
        self._elo = elo
        self._nGames = nGames

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def elo(self):
        return self._elo

    @elo.setter
    def elo(self, value):
        self._elo = value

    @property
    def nGames(self):
        return self._nGames

    @nGames.setter
    def nGames(self, value):
        self._nGames = value


    def printInfo(self):
        print(f"{self.name} | Elo={int(self.elo)} | nGames={self.nGames}")

    def incrementGames(self):
        self.nGames = self.nGames + 1




class officeballGame:
    def __init__(self, winner, loser):
        self._winner  = winner
        self._loser   = loser
        self._winnerOrigElo = winner.elo
        self._loserOrigElo = loser.elo
        self._kFactor = 50
        self._date    = '31/12/1969'
        self._time    = 1200
        self._gameNumber = 0

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, value):
        self._winner = value

    @property
    def loser(self):
        return self._loser

    @loser.setter
    def loser(self, value):
        self._loser = value


    @property
    def kFactor(self):
        return self._kFactor

    @kFactor.setter
    def kFactor(self, value):
        self._kFactor = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def gameNumber(self):
        return self._gameNumber

    @gameNumber.setter
    def gameNumber(self, value):
        self._gameNumber = value


    @property
    def winnerExpectation(self):
        """ The expectation for the person who won, to have lost """
        return 1.0 / ( 1.0 + 10.0**(
            (self._winnerOrigElo - self._loserOrigElo)/400.0) )

    @property
    def eloChange(self):
        """ The change in Elo to the winner and loser """
        return self.kFactor * self.winnerExpectation


    def updateElo(self):
        eloDiff = self.eloChange
        self.winner.elo = self.winner.elo + eloDiff
        self.loser.elo  = self.loser.elo  - eloDiff
        self.winner.incrementGames()
        self.loser.incrementGames()



def main():


    with io.open('playerData.yaml', 'r') as stream:
        players = yaml.load(stream)

    # alec = officeballPlayer()
    # alec.name = 'Alec'
    # alec.ID = 1
    # brad = officeballPlayer()
    # brad.name = 'Brad'
    # brad.ID = 2
    # curtis = officeballPlayer()
    # curtis.name = 'Curtis'
    # curtis.ID = 3
    # zeno = officeballPlayer()
    # zeno.name = 'Zeno'
    # zeno.ID = 4
    # players = [alec, brad, curtis, zeno]


    for player in players:
        player.printInfo()
    games = [officeballGame(players[0], players[3])]
    games[0].updateElo()
    print('')
    for player in players:
        player.printInfo()

    # games.append(officeballGame(curtis, zeno))
    # games[1].updateElo()
    # print('')
    # for player in players:
    #     player.printInfo()
    # games.append(officeballGame(alec, zeno))
    # games[2].updateElo()
    # print('')
    # for player in players:
    #     player.printInfo()

    # with open('playerData.pkl', 'wb') as handle:
    #     pickle.dump(players, handle)


    # with io.open('test.yaml', 'w', encoding='utf8') as outfile:
    #     yaml.dump(players, outfile, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    main()

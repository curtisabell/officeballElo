#!/usr/bin/python3
import subprocess
import yaml
import io
import numpy as np


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

    # ------------------------------------------------------------------

    def printInfo(self):
        print(f"{self.name} | Elo={int(self.elo)} | nGames={self.nGames}")

    def incrementGames(self):
        self.nGames = self.nGames + 1

    def resetPlayerData(self):
        self.elo = 1000
        self.nGames = 0



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

    # ------------------------------------------------------------------

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




class officeballProgram:
    def __init__(self):
        self._players = []
        self._games = []

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, value):
        self._players = value

    @property
    def games(self):
        return self._games

    @games.setter
    def games(self, value):
        self._games = value

    # ------------------------------------------------------------------


    def addGame(self):
        self.readCurrentData()

        isValidInput = False
        while not isValidInput:
            newWinner = input('Enter the name of the winning player: ')
            for player in self.players:
                if player.name == newWinner:
                    isValidInput = True

        isValidInput = False
        while not isValidInput:
            newLoser  = input('Enter the name of the losing player: ')
            if newLoser == newWinner:
                print('I doubt they played against themselves, try again.')
            else:
                for player in self.players:
                    if player.name == newLoser:
                        isValidInput = True



    def addNewPlayer(self):
        print('Enter the name of the new player:')


    def removePlayer(self):
        print('Note, only a player with 0 games played is able to be removed.')
        print('Enter the name of the player to be removed:')


    def revertData(self):
        print('Reverting to previous data')

    def readCurrentData(self):
        # Read in current player data
        with io.open('playerData.yaml', 'r') as stream:
            self.players = yaml.load(stream)

        # Read in the game history
        with io.open('gameHistory.yaml', 'r') as stream:
            self.games = yaml.load(stream)


    def readPreviousData(self):
        # Read in previous player data
        with io.open('playerData_backup.yaml', 'r') as stream:
            self.players = yaml.load(stream)

        # Read in the previous game history
        with io.open('gameHistory_backup.yaml', 'r') as stream:
            self.games = yaml.load(stream)


    def writeData(self):
        # Backup playerData and gameHistory
        process = subprocess.run(['cp', 'playerData.yaml', 'playerData_backup.yaml'])
        process = subprocess.run(['cp', 'gameHistory.yaml', 'gameHistory_backup.yaml'])

        # Store playerData in a yaml file
        with io.open('playerData.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump(self.players, outfile, default_flow_style=False, allow_unicode=True)

        # Store gameData in a yaml file
        with io.open('gameHistory.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump(self.games, outfile, default_flow_style=False, allow_unicode=True)


    def runProgram(self):
        while True:
            print('Enter an option:')
            print('1. Add a new game')
            print('8. List current players')
            print('9. Undo previous command')
            print('0. Exit')
            kbdInput = input('')

            if kbdInput == '0':
                print('Exiting...')
                break

            elif kbdInput == '1':
                self.addGame()

            elif kbdInput == '8':
                self.readCurrentData()
                for player in self.players:
                    player.printInfo()

            elif kbdInput == '9':
                self.readPreviousData()
                self.writeData()




def main():
    officeball = officeballProgram()
    officeball.runProgram()




if __name__ == "__main__":
    main()

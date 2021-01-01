import pygame
from main import dis
import sqlite3

class EndGameOverlay:
    def __init__(self):
        self.position_x = 0
        self.position_y = 0

        self.statistics_data = self.get_statistics()

        self.buttons = {
            'main menu': None
        }


    def get_statistics(self):
        # Connect to the Database
        connect = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor = connect.cursor()

        # Retrieve Leaderboard Top 10
        cursor.execute("SELECT * FROM statistics")
        raw_data = cursor.fetchall()[-1]

        # Terminate the connection
        connect.close()

        return raw_data


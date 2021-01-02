from BaseInvaders.config import *
import sqlite3
from main import dis, DISPLAY_X, DISPLAY_Y
from config import bahnschrift_font_small, COLOR_WHITE, COLOR_WHITE_DARK


class MenuStatisticsPage:
    def __init__(self):
        self.dis = dis

        self.leaderboard_y = 250

        self.lb_image_width = 0
        self.lb_header_offset = 50
        self.lb_image_height = 500

        self.lb_image_pos = 0
        self.stat_image_height = None

        self.scroll_speed = 5
        self.scroll_bar_width = 5

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(), quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if (self.lb_image_pos + self.scroll_speed) < 0: self.lb_image_pos += self.scroll_speed

                elif event.button == 5:
                    print(self.lb_image_pos)
                    print(self.stat_image_height)
                    if (self.lb_image_pos - self.scroll_speed) > (-1 * self.stat_image_height) + self.lb_image_height: self.lb_image_pos -= self.scroll_speed

    def get_scrollbar(self):
        scroll_bar = pygame.Surface((self.scroll_bar_width, self.lb_image_height))
        scroll_bar.fill(COLOR_WHITE)

    def get_leaderboard(self):
        # Create a surface
        lb_image = pygame.Surface((self.lb_image_width, self.lb_image_height), pygame.SRCALPHA, 32)
        lb_image = lb_image.convert_alpha()

        # Get the raw leaderboard image & blit the raw leaderboard image onto the surface based on the LB image pos
        instance = StatisticsLeaderboard()
        leaderboard_table = instance.create_leaderboard_table(instance.get_leaderboard())  # Gets LB image, LB image length

        self.stat_image_height = leaderboard_table[2]

        self.lb_image_width = leaderboard_table[1]

        lb_image.blit(leaderboard_table[0], (0, self.lb_image_pos))

        return lb_image

    def display_graphics(self):
        self.dis.blit(statistics_menu, (0, 0))
        self.dis.blit(self.get_leaderboard(), (DISPLAY_X / 2 - self.lb_image_width / 2, self.leaderboard_y))

        bahnschrift_font_small.set_bold(True)
        self.dis.blit(bahnschrift_font_small.render("Position", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2), self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("XP", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 150, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Level", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 300, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Bases", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 450, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Time", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 600, self.leaderboard_y - self.lb_header_offset))
        self.dis.blit(bahnschrift_font_small.render("Date", True, COLOR_WHITE), ((DISPLAY_X / 2 - self.lb_image_width / 2) + 750, self.leaderboard_y - self.lb_header_offset))
        bahnschrift_font_small.set_bold(False)


    def run_menu(self):
        while True:
            self.handle_events()
            self.display_graphics()
            pygame.display.flip()


class StatisticsLeaderboard:
    def __init__(self):
        self.limit = 100
        self.leaderboard_data = self.get_leaderboard()

    def get_leaderboard(self):

        # Connect to the Database
        connect = sqlite3.connect('./BaseInvaders/statistics.db')
        cursor = connect.cursor()

        # Retrieve Leaderboard Top 10
        cursor.execute(f"SELECT * FROM statistics ORDER BY xp DESC LIMIT {self.limit}")
        raw_data = cursor.fetchall()

        # Terminate the connection
        connect.close()

        return raw_data

    @staticmethod
    def create_leaderboard_table(dataset):
        image_height = 50*len(dataset) + 50
        text_surface = pygame.Surface((1500, image_height), pygame.SRCALPHA, 32)
        text_surface = text_surface.convert_alpha()
        lb_spacer = 40

        dates = []

        # (bases, xp, level, time, date)
        for idx, entry in enumerate(dataset):
            # Position
            text_surface.blit(bahnschrift_font_small.render(f"#{idx + 1}", True, COLOR_WHITE), (0, idx * lb_spacer))

            # XP
            text_surface.blit(bahnschrift_font_small.render(str(entry[1]), True, COLOR_WHITE), (150, idx * lb_spacer))

            # Level
            text_surface.blit(bahnschrift_font_small.render(str(entry[2]), True, COLOR_WHITE), (300, idx * lb_spacer))

            # Bases
            text_surface.blit(bahnschrift_font_small.render(str(entry[0]), True, COLOR_WHITE), (450, idx * lb_spacer))

            # Time
            text_surface.blit(bahnschrift_font_small.render(str(entry[3]), True, COLOR_WHITE), (600, idx * lb_spacer))

            # Date
            text_surface.blit(bahnschrift_font_small.render(str(entry[4]), True, COLOR_WHITE), (750, idx * lb_spacer))

            dates.append(entry[4])

        print(len(dataset))

        return text_surface, 750 + max([bahnschrift_font_small.size(date)[0] for date in dates]), image_height

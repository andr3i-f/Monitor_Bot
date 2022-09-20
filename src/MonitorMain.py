from CompareHandler import Compare
from CanaryYellowOFFW import OffWhiteMonitor
import time
import pygame
import sys
import datetime


class MonitorMain:
    """Class to manage the behavior and initiations of all monitors"""
    def __init__(self, delay=3):
        self.delay = delay
        self.off_white = OffWhiteMonitor()
        self.comparer = Compare(self.off_white)

        # Initializing pygame as current runner handler
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Online Monitor by Andrei F")

    def run(self):
        start = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = time.time()

                    log = f'ENDING TASK at {datetime.datetime.now()} \nRan for {end-start} seconds.'
                    self.comparer.bot.update_log(log)

                    sys.exit()

            print("Checking . . .")
            self.off_white.find_shoes()
            self.comparer.handler()
            time.sleep(self.delay)


def main():
    handler = MonitorMain()
    handler.run()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from todayos.core import TodayOS


def main():
    os_system = TodayOS(1280, 800)
    os_system.run()


if __name__ == '__main__':
    main()

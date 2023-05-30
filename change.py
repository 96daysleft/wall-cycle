#!/usr/bin/env python3

import os
from wallpapers import WallPapers
from config import Config

def main():
	config = Config(f"{os.path.dirname(os.path.realpath(__file__))}/config.json")

	wall_paper = WallPapers(config)
	wall_paper.get_wallpaper()


if __name__ == "__main__":
	main()
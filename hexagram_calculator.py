import datetime
from constants import HEXAGRAM_NAMES

class HexagramCalculator:
	def __init__(self):
		self.cycles = [
			datetime.timedelta(seconds=1.9775390625),
			datetime.timedelta(minutes=2, seconds=6.5625),
			datetime.timedelta(hours=2, minutes=15),
			datetime.timedelta(days=6),
			datetime.timedelta(days=384),
			datetime.timedelta(days=24576)  # 384 days * 64
		]

	def get_hexagrams(self, time_to_zero):
		hexagrams = []
		total_seconds = abs(time_to_zero.total_seconds())

		for level in range(6):  # Changed from 5 to 6
			cycle_length = self.cycles[level]
			if level == 0:
				level_2_cycle_length = self.cycles[1]
				cycle_number_level_2 = int(total_seconds // level_2_cycle_length.total_seconds())
				cycle_number = (cycle_number_level_2 * 64 + int((total_seconds % level_2_cycle_length.total_seconds()) // cycle_length.total_seconds())) % 64
			else:
				cycle_number = int(total_seconds // cycle_length.total_seconds()) % 64
			
			time_since_last_change = total_seconds % cycle_length.total_seconds()
			hexagram_number = (cycle_number % 64) + 1
			hexagrams.append((
				level + 1,
				cycle_length,
				"h",
				hexagram_number,
				HEXAGRAM_NAMES[hexagram_number - 1],
				time_since_last_change
			))

		return hexagrams

	def calculate_moving_line(self, time_since_last_change, cycle_length):
		return int((time_since_last_change // (cycle_length.total_seconds() / 6)) + 1)
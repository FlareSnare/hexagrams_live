import threading
import time
import signal
import sys
import os
import datetime
from sound_manager import SoundManager
from hexagram_calculator import HexagramCalculator
from vrchat_manager import VRChatManager
from gui_manager import GUIManager
import constants

class HexagramApp:
	def __init__(self):
		# Initialize constants first
		constants.ZERO_DATETIME = datetime.datetime(2055, 7, 16)
		constants.UPDATE_HEXAGRAMS = True
		constants.EXIT_FLAG = False
		
		# Ensure sound directory exists before initializing sound manager
		if not os.path.exists(constants.SOUNDS_DIR):
			os.makedirs(constants.SOUNDS_DIR)
		
		# Initialize previous hexagrams state
		current_datetime = datetime.datetime.now()
		time_to_zero = constants.ZERO_DATETIME - current_datetime
		
		self.sound_manager = SoundManager()
		self.hexagram_calculator = HexagramCalculator()
		self.vrchat_manager = VRChatManager()
		
		# Calculate initial hexagrams before GUI setup
		initial_hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
		constants.previous_hexagrams = {}  # Initialize the dictionary
		
		for level in range(1, 7):
			for hexagram in initial_hexagrams:
				if hexagram[0] == level:  # if this is the hexagram for current level
					constants.previous_hexagrams[f'level_{level}'] = hexagram[3]  # Store hexagram number
					moving_line = int((hexagram[5] // (hexagram[1].total_seconds() / 6)) + 1)
					constants.previous_hexagrams[f'level_{level}_line'] = moving_line
		
		self.gui_manager = GUIManager(self.sound_manager, self.hexagram_calculator, self.vrchat_manager)
		
		self.setup_threads()
		self.setup_signal_handlers()

	def update_zero_datetime(self, new_datetime):
		"""
		Updates the zero datetime and ensures all components are notified
		Args:
			new_datetime: Can be either a datetime object or a string in format 'YYYY-MM-DD'
		"""
		try:
			if isinstance(new_datetime, str):
				# Parse the string into a datetime object
				parsed_date = datetime.datetime.strptime(new_datetime, '%Y-%m-%d')
				# Set time to midnight
				new_datetime = datetime.datetime(parsed_date.year, parsed_date.month, parsed_date.day)
			
			if isinstance(new_datetime, datetime.datetime):
				constants.ZERO_DATETIME = new_datetime
				# Force an immediate update of the display
				current_datetime = datetime.datetime.now()
				time_to_zero = constants.ZERO_DATETIME - current_datetime
				hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
				self.gui_manager.update_display(hexagrams, time_to_zero)
				return True
			return False
		except ValueError:
			return False

	def setup_threads(self):
		self.vrchat_thread = threading.Thread(target=self.vrchat_update_loop)
		self.gui_thread = threading.Thread(target=self.gui_update_loop)
		
		self.vrchat_thread.daemon = True
		self.gui_thread.daemon = True

	def setup_signal_handlers(self):
		signal.signal(signal.SIGINT, self.signal_handler)
		signal.signal(signal.SIGTERM, self.signal_handler)
		self.gui_manager.root.protocol("WM_DELETE_WINDOW", self.cleanup)

	def vrchat_update_loop(self):
		while not constants.EXIT_FLAG and constants.UPDATE_HEXAGRAMS:
			current_datetime = datetime.datetime.now()
			time_to_zero = constants.ZERO_DATETIME - current_datetime
			hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
			
			if constants.CURRENT_PAGE == 1:
				message = self.vrchat_manager.format_message_page1(hexagrams, time_to_zero)
				self.vrchat_manager.send_message(message)
				time.sleep(1.9775390625)
			else:
				message = self.vrchat_manager.format_message_page2(hexagrams, time_to_zero)
				self.vrchat_manager.send_message(message)
			
			time.sleep(2)

	def gui_update_loop(self):
		while not constants.EXIT_FLAG and constants.UPDATE_HEXAGRAMS:
			current_datetime = datetime.datetime.now()
			time_to_zero = constants.ZERO_DATETIME - current_datetime
			hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
			self.gui_manager.update_display(hexagrams, time_to_zero)
			time.sleep(0.05)

	def run(self):
		self.vrchat_thread.start()
		self.gui_thread.start()
		self.gui_manager.run()

	def cleanup(self):
		constants.EXIT_FLAG = True
		constants.UPDATE_HEXAGRAMS = False
		
		if self.vrchat_thread.is_alive():
			self.vrchat_thread.join()
		if self.gui_thread.is_alive():
			self.gui_thread.join()
			
		self.sound_manager.cleanup()
		self.gui_manager.cleanup()
		sys.exit(0)

	def signal_handler(self, sig, frame):
		self.cleanup()

if __name__ == "__main__":
	app = HexagramApp()
	app.run()
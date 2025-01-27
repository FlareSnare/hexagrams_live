import datetime
from pythonosc import udp_client
import constants

class VRChatManager:
	def __init__(self):
		self.client = udp_client.SimpleUDPClient(constants.VRCHAT_IP, constants.VRCHAT_PORT)

	def send_message(self, message):
		if not constants.SEND_TO_VRCHAT_ENABLED:
			return
		
		try:
			self.client.send_message("/chatbox/input", [message, True, False])
			print("Message sent to VRChat")
		except Exception as e:
			print("Error sending message to VRChat:", e)

	def format_message_page1(self, hexagrams, time_to_zero):
		current_date = datetime.datetime.now().date()
		days_to_zero = round(time_to_zero.total_seconds() / 86400)
		hours_to_zero = int((time_to_zero.total_seconds() % 86400) // 3600)
		
		message = f"Date: {current_date}\nDays_to_0: {days_to_zero}d{hours_to_zero}h\n"
		
		for level, cycle_length, cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
			if level in [1, 2]:
				continue
				
			hexagram_first_name = hexagram_name.split(" - ")[0]
			moving_line = (time_since_last_change // (cycle_length.total_seconds() / 6)) + 1

			if level == 3:
				time_to_next_change = datetime.timedelta(seconds=time_since_last_change) - cycle_length
				time_time = (cycle_length - abs(time_to_next_change))
				hours = int(abs(time_time.seconds // 3600))
				minutes = int(abs((time_time.seconds % 3600) // 60))
				seconds = int(abs(time_time.seconds % 60))
				message += f"Change: {hours:02d}:{minutes:02d}:{seconds:02d}\n"
				cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
				message += f"L {level}: {cycle_length_str} {cycle_name}, {hexagram_number}-{hexagram_first_name} - {moving_line}\n"
			elif level in [4, 5]:
				days = cycle_length.total_seconds() / 86400
				message += f"L {level}: {days:.0f} d, {hexagram_number}-{hexagram_first_name} - {moving_line}\n"

		return message

	def format_message_page2(self, hexagrams, time_to_zero):
		message = ""
		for level, cycle_length, _cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
			if level > 3:
				continue
				
			hexagram_first_name = hexagram_name.split(" - ")[0]
			moving_line = (time_since_last_change // (cycle_length.total_seconds() / 6)) + 1

			if level == 1:
				cycle_length_str = f"{cycle_length.total_seconds():.2f}"
				message += f"L {level}: {cycle_length_str} s, {hexagram_number} - {hexagram_first_name}\n"
			elif level == 2:
				minutes = int(abs(time_since_last_change // 60))
				seconds = int(abs(time_since_last_change % 60))
				message += f"L 2 change {minutes:02d}:{seconds:02d}\n"
				message += f"L {level}: {cycle_length.total_seconds():.2f} s, {hexagram_number} - {hexagram_first_name} - {moving_line}\n"
			elif level == 3:
				hours = int(abs(time_since_last_change // 3600))
				minutes = int(abs((time_since_last_change % 3600) // 60))
				seconds = int(abs(time_since_last_change % 60))
				message += f"L 3 change {hours:02d}:{minutes:02d}:{seconds:02d}\n"
				cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
				message += f"L {level}: {cycle_length_str} h, {hexagram_number} - {hexagram_first_name} - {moving_line}\n"

		return message
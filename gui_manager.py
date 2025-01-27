import tkinter as tk
from tkinter import ttk, scrolledtext
import datetime

from datetime import timedelta
import math
import constants
import webbrowser
import os


class GUIManager:
	def __init__(self, sound_manager, hexagram_calculator, vrchat_manager):
		self.sound_manager = sound_manager
		self.hexagram_calculator = hexagram_calculator
		self.vrchat_manager = vrchat_manager
		self.calculator_window = None
		self.sound_menu_window = None
		self.zero_datetime = datetime.datetime(2055, 7, 16)  # Default zero date
		self.current_page = 1
		self.audio_playback_allowed = False
		self.hexagram_images = {}  # Store loaded images
		self.hexagram_labels = {}  # Store image labels
		self.setup_main_window()

	def setup_main_window(self):
		self.root = tk.Tk()
		self.root.title("Hexagrams Live 2.0")
		
		# Set taskbar icon
		try:
			# For Windows (.ico file)
			icon_path = os.path.join(constants.IMAGES_DIR, 'icon.ico')
			if os.path.exists(icon_path):
				self.root.iconbitmap(icon_path)
			else:
				# For Linux/Unix (.png file)
				icon_path = os.path.join(constants.IMAGES_DIR, 'icon.png')
				if os.path.exists(icon_path):
					icon_image = tk.PhotoImage(file=icon_path)
					self.root.iconphoto(True, icon_image)
		except Exception as e:
			print(f"Failed to set window icon: {e}")
		
		self.root.configure(background=constants.DARK_THEME['background'])
		
		# Create main container
		self.main_container = ttk.Frame(self.root)
		self.main_container.pack(fill=tk.BOTH, expand=True)
		
		# Create main content frame
		self.content_frame = ttk.Frame(self.main_container)
		self.content_frame.pack(fill=tk.BOTH, expand=True)
		
		# Create top controls frame
		self.top_controls = ttk.Frame(self.content_frame)
		self.top_controls.pack(fill=tk.X, padx=10, pady=5)
		
		# Create zero date section in top controls
		self.zero_date_frame = ttk.Frame(self.top_controls)
		self.zero_date_frame.pack(side=tk.LEFT)
		
		# Create buttons frame in top controls
		self.buttons_frame = ttk.Frame(self.top_controls)
		self.buttons_frame.pack(side=tk.RIGHT)
		
		# Add button to open browser
		self.browser_button = ttk.Button(
			self.buttons_frame,
			text="Open Hexagram Reference",
			command=lambda: webbrowser.open("https://www.jamesdekorne.com/GBCh/hex1.htm")
		)
		self.browser_button.pack(side=tk.RIGHT, padx=5)

		self.setup_style()
		self.create_widgets()
		self.root.after(1000, self.enable_audio_playback)
		
		# Set initial window size and position
		initial_width = 1280  # Increased from 1024 to 1280
		initial_height = 820  # Increased from 768 to 800
		
		# Set minimum window size to prevent too small resizing
		self.root.minsize(800, 600)
		
		# Set initial size
		self.root.geometry(f"{initial_width}x{initial_height}")
		
		# Center the window on screen
		self.root.update_idletasks()  # Update to get accurate window dimensions
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()
		x = (screen_width - initial_width) // 2
		y = (screen_height - initial_height) // 2
		self.root.geometry(f"{initial_width}x{initial_height}+{x}+{y}")

	def setup_style(self):
		self.style = ttk.Style()
		self.style.theme_use('clam')
		self.apply_theme(constants.DARK_THEME)

	def apply_theme(self, theme):
		self.style.configure('TLabel', background=theme['background'], foreground=theme['foreground'])
		self.style.configure('TEntry', background=theme['entry_bg'], foreground=theme['foreground'],
						   fieldbackground=theme['entry_bg'])
		self.style.configure('TButton', background=theme['button_bg'], foreground=theme['foreground'])
		self.style.configure('TFrame', background=theme['background'])
		self.style.configure('TText', background=theme['text_bg'], foreground=theme['foreground'])
		self.style.configure('TScrollbar', background=theme['button_bg'], foreground=theme['foreground'])
		self.root.configure(background=theme['background'])

	def create_widgets(self):
		self.create_zero_date_section()
		self.create_display_area()
		self.create_control_buttons()
		self.create_check_section()

	def create_zero_date_section(self):
		self.zero_date_label = ttk.Label(self.zero_date_frame, text="Zero Date (YYYY-MM-DD):")
		self.zero_date_label.pack(side=tk.LEFT, padx=5)
		
		self.zero_date_entry = ttk.Entry(self.zero_date_frame)
		self.zero_date_entry.pack(side=tk.LEFT, padx=5)
		self.zero_date_entry.insert(0, "2055-07-16")
		
		self.update_button = ttk.Button(self.zero_date_frame, text="Update", command=self.update_zero_datetime)
		self.update_button.pack(side=tk.LEFT, padx=5)

	def load_hexagram_image(self, number):
		"""Load a hexagram image by its number (1-64)"""
		if number not in self.hexagram_images:
			image_path = os.path.join(constants.IMAGES_DIR, f'hexagram{number:02d}.gif')
			if os.path.exists(image_path):
				try:
					photo = tk.PhotoImage(file=image_path)
					# Subsample the image to make it smaller (2 means half size)
					self.hexagram_images[number] = photo.subsample(2, 2)
				except tk.TclError:
					print(f"Error loading image: {image_path}")
					return None
		return self.hexagram_images.get(number)

	def create_display_area(self):
		# Create a frame to hold both hexagram images and text
		self.display_frame = ttk.Frame(self.content_frame)
		self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
		
		# Create frame for hexagram images on the left
		self.hexagram_frame = ttk.Frame(self.display_frame)
		self.hexagram_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
		
		# Create labels for each level's hexagram with level numbers
		for level in range(1, 7):
			# Create a frame for each level to hold number and hexagram
			level_frame = ttk.Frame(self.hexagram_frame)
			level_frame.pack(pady=5)
			
			# Add level number label
			level_label = ttk.Label(
				level_frame, 
				text=f"Level {level}",
				background=constants.DARK_THEME['background'],
				foreground=constants.DARK_THEME['foreground'],
				width=8  # Fixed width for alignment
			)
			level_label.pack(side=tk.LEFT, padx=(0, 5))
			
			# Add hexagram image label
			label = ttk.Label(level_frame)
			label.pack(side=tk.LEFT)
			self.hexagram_labels[level] = label
		
		# Create the main text area
		self.output_text = scrolledtext.ScrolledText(
			self.display_frame, width=130, height=20,
			background=constants.DARK_THEME['text_bg'],
			foreground=constants.DARK_THEME['foreground']
		)
		self.output_text.pack(fill=tk.BOTH, expand=True)
		self.output_text.configure(state='disabled')

	def create_control_buttons(self):
		# Create control buttons frame
		self.control_buttons = ttk.Frame(self.buttons_frame)
		self.control_buttons.pack(side=tk.RIGHT, padx=5)

		self.send_to_vrchat_button = ttk.Button(
			self.control_buttons,
			text="Send to VRChat: ON" if constants.SEND_TO_VRCHAT_ENABLED else "Send to VRChat: OFF",
			command=self.toggle_send_to_vrchat
		)
		self.send_to_vrchat_button.pack(side=tk.LEFT, padx=5)

		self.page_button = ttk.Button(self.control_buttons, text="Page 1", command=self.toggle_page)
		self.page_button.pack(side=tk.LEFT, padx=5)

		self.sound_menu_button = ttk.Button(self.control_buttons, text="Sound Menu", command=self.open_sound_menu)
		self.sound_menu_button.pack(side=tk.LEFT, padx=5)

		self.calculator_button = ttk.Button(self.control_buttons, text="Zero Date Calculator", command=self.open_calculator)
		self.calculator_button.pack(side=tk.LEFT, padx=5)


	def create_check_section(self):
		# Create check section frame
		# Create right panel for checking hexagrams
		self.check_panel = ttk.Frame(self.content_frame)
		self.check_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

		# Create input frame for date/time
		self.input_frame = ttk.Frame(self.check_panel)
		self.input_frame.pack(fill=tk.X, pady=5)

		# Date input
		self.date_label = ttk.Label(self.input_frame, text="Date (YYYY-MM-DD):")
		self.date_label.pack(side=tk.LEFT, padx=5)
		self.date_entry = ttk.Entry(self.input_frame)
		self.date_entry.pack(side=tk.LEFT, padx=5)

		# Time input  
		self.time_label = ttk.Label(self.input_frame, text="Time (HH:MM:SS):")
		self.time_label.pack(side=tk.LEFT, padx=5)
		self.time_entry = ttk.Entry(self.input_frame)
		self.time_entry.pack(side=tk.LEFT, padx=5)

		# Check button
		self.check_button = ttk.Button(self.input_frame, text="Check Hexagrams", command=self.check_hexagrams)
		self.check_button.pack(side=tk.LEFT, padx=5)

		# Create frame to hold both hexagram images and text for check section
		self.check_display_frame = ttk.Frame(self.check_panel)
		self.check_display_frame.pack(fill=tk.BOTH, expand=True, pady=5)

		# Create frame for check hexagram images on the left
		self.check_hexagram_frame = ttk.Frame(self.check_display_frame)
		self.check_hexagram_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

		# Create labels for each level's hexagram in check section
		self.check_hexagram_labels = {}
		for level in range(1, 7):
			# Create a frame for each level to hold number and hexagram
			level_frame = ttk.Frame(self.check_hexagram_frame)
			level_frame.pack(pady=5)
			
			# Add level number label
			level_label = ttk.Label(
				level_frame, 
				text=f"Level {level}",
				background=constants.DARK_THEME['background'],
				foreground=constants.DARK_THEME['foreground'],
				width=8  # Fixed width for alignment
			)
			level_label.pack(side=tk.LEFT, padx=(0, 5))
			
			# Add hexagram image label
			label = ttk.Label(level_frame)
			label.pack(side=tk.LEFT)
			self.check_hexagram_labels[level] = label

		# Results text widget
		self.check_text = scrolledtext.ScrolledText(
			self.check_display_frame, width=60, height=20,
			background=constants.DARK_THEME['text_bg'],
			foreground=constants.DARK_THEME['foreground']
		)
		self.check_text.pack(fill=tk.BOTH, expand=True, pady=5)
		self.check_text.configure(state='disabled')


	def update_display(self, hexagrams, time_to_zero, text_widget=None, input_datetime=None):
		"""Update the GUI display with hexagram information"""
		if text_widget is None:
			text_widget = self.output_text
			# Update hexagram images only for main display
			for hexagram in hexagrams:
				level, _, _, hexagram_number, _, _ = hexagram
				image = self.load_hexagram_image(hexagram_number)
				if image and level in self.hexagram_labels:
					self.hexagram_labels[level].configure(image=image)
					self.hexagram_labels[level].image = image  # Keep a reference
		
		message_lines = []
		if not hexagrams:
			message_lines.append("No hexagrams found for the current date.")
		else:
			if input_datetime:
				current_date = input_datetime.date()
				current_time = input_datetime.time()
			else:
				current_date = datetime.datetime.now().date()
				current_time = datetime.datetime.now().time()
			
			days_to_zero = round(time_to_zero.total_seconds() / 86400, 4)
			message_lines.append(f"Hexagrams for: {current_date} - {current_time}")
			message_lines.append(f"Days to 0: {days_to_zero}")
			message_lines.append(f"Zero Date: {constants.ZERO_DATETIME}")
			
			for level, cycle_length, _cycle_name, hexagram_number, hexagram_name, time_since_last_change in hexagrams:
				hexagram_first_name = hexagram_name.split(" - ")[0]
				moving_line = int((time_since_last_change // (cycle_length.total_seconds() / 6)) + 1)

				if level == 1:
					milliseconds = int(abs(time_since_last_change * 1000))
					cycle_length_str = f"{cycle_length.total_seconds():.4f}"
					message_lines.append(f"Level {level}: {cycle_length_str} s, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 1 changes in: {milliseconds:03d}ms")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					# Only play sounds for main display
					if text_widget == self.output_text:
						if constants.previous_hexagrams[f'level_{level}'] != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_1_ENABLED:
								self.sound_manager.play_level_sound(1)

						if constants.previous_hexagrams[f'level_{level}_line'] != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_1_LINE_ENABLED:
								self.sound_manager.play_line_sound(1)

				elif level == 2:
					minutes = int(abs(time_since_last_change // 60))
					seconds = int(abs(time_since_last_change % 60))
					message_lines.append(f"Level {level}: {cycle_length.total_seconds()} s, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 2 changes in: {minutes:02d}:{seconds:02d}")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					if text_widget == self.output_text:
						if constants.previous_hexagrams[f'level_{level}'] != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_2_ENABLED:
								self.sound_manager.play_level_sound(2)

						if constants.previous_hexagrams[f'level_{level}_line'] != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_2_LINE_ENABLED:
								self.sound_manager.play_line_sound(2)

				elif level == 3:
					hours = int(abs(time_since_last_change // 3600))
					minutes = int(abs((time_since_last_change % 3600) // 60))
					seconds = int(abs(time_since_last_change % 60))
					cycle_length_str = f"{cycle_length.total_seconds() / 3600:.2f}"
					message_lines.append(f"Level {level}: {cycle_length_str} h, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 3 changes in: {hours:02d}:{minutes:02d}:{seconds:02d}")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					if text_widget == self.output_text:
						if constants.previous_hexagrams[f'level_{level}'] != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_3_ENABLED:
								self.sound_manager.play_level_sound(3)

						if constants.previous_hexagrams[f'level_{level}_line'] != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_3_LINE_ENABLED:
								self.sound_manager.play_line_sound(3)

				elif level == 4:
					seconds = int(abs(time_since_last_change % 60))
					minutes = int(abs((time_since_last_change % 3600) // 60))
					hours = int(abs(time_since_last_change // 3600))
					days = hours // 24
					hours = hours % 24
					cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
					message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 4 changes in: {days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					if text_widget == self.output_text:
						if constants.previous_hexagrams[f'level_{level}'] != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_4_ENABLED:
								self.sound_manager.play_level_sound(4)

						if constants.previous_hexagrams[f'level_{level}_line'] != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_4_LINE_ENABLED:
								self.sound_manager.play_line_sound(4)

				elif level == 5:
					seconds = int(abs(time_since_last_change % 60))
					minutes = int(abs((time_since_last_change % 3600) // 60))
					hours = int(abs(time_since_last_change // 3600))
					days = hours // 24
					remaining_days = days
					hours = hours % 24
					cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
					message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 5 changes in: {remaining_days:03d}d{hours:02d}:{minutes:02d}:{seconds:02d}")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					if text_widget == self.output_text:
						if constants.previous_hexagrams[f'level_{level}'] != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_5_ENABLED:
								self.sound_manager.play_level_sound(5)

						if constants.previous_hexagrams[f'level_{level}_line'] != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_5_LINE_ENABLED:
								self.sound_manager.play_line_sound(5)

				elif level == 6:
					seconds = int(abs(time_since_last_change % 60))
					minutes = int(abs((time_since_last_change % 3600) // 60))
					hours = int(abs(time_since_last_change // 3600))
					days = hours // 24
					remaining_days = days
					hours = hours % 24
					cycle_length_str = f"{cycle_length.total_seconds() / 86400:.2f}"
					message_lines.append(f"Level {level}: {cycle_length_str} days, Hexagram {hexagram_number} - {hexagram_name}")
					message_lines.append(f"Level 6 changes in: {remaining_days:03d}d{hours:02d}:{minutes:02d}:{seconds:02d}")
					message_lines.append(f"Level {level}: Moving Line: {moving_line}")
					
					if text_widget == self.output_text:
						if constants.previous_hexagrams.get(f'level_{level}') != hexagram_number:
							constants.previous_hexagrams[f'level_{level}'] = hexagram_number
							if constants.PLAY_AUDIO_LEVEL_6_ENABLED:
								self.sound_manager.play_level_sound(6)

						if constants.previous_hexagrams.get(f'level_{level}_line') != moving_line:
							constants.previous_hexagrams[f'level_{level}_line'] = moving_line
							if constants.PLAY_AUDIO_LEVEL_6_LINE_ENABLED:
								self.sound_manager.play_line_sound(6)


		# Update the text box with the hexagram output
		text_widget.configure(state='normal')
		text_widget.delete("1.0", tk.END)
		for line in message_lines:
			text_widget.insert(tk.END, line + "\n")
		text_widget.configure(state='disabled')
		text_widget.see(tk.END)
		text_widget.update_idletasks()

	def toggle_send_to_vrchat(self):
		constants.SEND_TO_VRCHAT_ENABLED = not constants.SEND_TO_VRCHAT_ENABLED
		self.send_to_vrchat_button.config(
			text="Send to VRChat: ON" if constants.SEND_TO_VRCHAT_ENABLED else "Send to VRChat: OFF"
		)

	def toggle_page(self):
		self.current_page = 2 if self.current_page == 1 else 1
		self.page_button.config(text=f"Page {self.current_page}")

	def update_zero_datetime(self):

		"""Updates the zero datetime based on the input in the zero_date_entry"""
		try:
			# Get the date string from the entry
			date_str = self.zero_date_entry.get()
			# Parse the string into a datetime object
			input_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
			# Set time to midnight
			new_datetime = datetime.datetime(input_date.year, input_date.month, input_date.day)
			
			# Update the constant
			constants.ZERO_DATETIME = new_datetime
			
			# Calculate current hexagrams before updating display
			current_datetime = datetime.datetime.now()
			time_to_zero = constants.ZERO_DATETIME - current_datetime
			hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
			
			# Update previous hexagrams state before display update
			for level in range(1, 7):
				for hexagram in hexagrams:
					if hexagram[0] == level:
						constants.previous_hexagrams[f'level_{level}'] = hexagram[3]
						moving_line = int((hexagram[5] // (hexagram[1].total_seconds() / 6)) + 1)
						constants.previous_hexagrams[f'level_{level}_line'] = moving_line
			
			# Update display without audio
			self.audio_playback_allowed = False
			self.update_display(hexagrams, time_to_zero)
			# Re-enable audio after a short delay
			self.root.after(100, self.enable_audio_playback)
			
		except ValueError:
			print("Invalid date format. Please enter a date in the format YYYY-MM-DD.")

	def check_hexagrams(self):
		"""Check hexagrams for a specified date and time"""
		date_str = self.date_entry.get()
		time_str = self.time_entry.get()
		try:
			# Parse the input date and time
			input_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
			# Calculate the time to zero
			time_to_zero = constants.ZERO_DATETIME - input_datetime
			# Get hexagrams for the specified time
			hexagrams = self.hexagram_calculator.get_hexagrams(time_to_zero)
			
			# Update hexagram images in check section
			for hexagram in hexagrams:
				level, _, _, hexagram_number, _, _ = hexagram
				image = self.load_hexagram_image(hexagram_number)
				if image and level in self.check_hexagram_labels:
					self.check_hexagram_labels[level].configure(image=image)
					self.check_hexagram_labels[level].image = image  # Keep a reference
			
			# Display the hexagrams in the check text widget
			self.check_text.configure(state='normal')
			self.check_text.delete("1.0", tk.END)
			self.check_text.insert(tk.END, f"Results for {date_str} {time_str}\n\n")
			self.update_display(hexagrams, time_to_zero, self.check_text, input_datetime)
			self.check_text.configure(state='disabled')
		except ValueError:
			# Show error in the check text widget
			self.check_text.configure(state='normal')
			self.check_text.delete("1.0", tk.END)
			self.check_text.insert(tk.END, "Invalid date or time format.\nPlease enter date as YYYY-MM-DD and time as HH:MM:SS.")
			self.check_text.configure(state='disabled')
			# Clear hexagram images
			for level in range(1, 7):
				if level in self.check_hexagram_labels:
					self.check_hexagram_labels[level].configure(image='')

	def update_text_widget(self, widget, hexagrams, time_to_zero, current_time=None):
		if not current_time:
			current_time = datetime.datetime.now()
		
		message = self.format_hexagram_message(hexagrams, time_to_zero, current_time)
		
		widget.configure(state='normal')
		widget.delete("1.0", tk.END)
		widget.insert(tk.END, message)
		widget.configure(state='disabled')
		widget.update_idletasks()

	def format_hexagram_message(self, hexagrams, time_to_zero, current_time):
		# Format the message based on the current page
		if self.current_page == 1:
			return self.vrchat_manager.format_message_page1(hexagrams, time_to_zero)
		return self.vrchat_manager.format_message_page2(hexagrams, time_to_zero)

	def enable_audio_playback(self):
		self.audio_playback_allowed = True

	def disable_audio_playback(self):
		self.audio_playback_allowed = False

	def open_calculator(self):

		"""Create and display the zero date calculator window"""
		if self.calculator_window is not None and tk.Toplevel.winfo_exists(self.calculator_window):
			self.calculator_window.lift()
			return

		def calculate_date():
			try:
				input_date = datetime.datetime.strptime(date_entry.get(), "%Y-%m-%d")
				years_to_add = 67
				days_in_years = years_to_add * 365  # Approximate, not accounting for leap years
				days_to_add = int(104.25)
				fractional_days = 104.25 - days_to_add
				seconds_to_add = int(math.ceil(fractional_days * 24 * 3600))
				new_date = input_date + datetime.timedelta(days=days_in_years + days_to_add, seconds=seconds_to_add)
				result_label.config(text="The new zero date is:")
				result_entry.config(state="normal")
				result_entry.delete(0, tk.END)
				result_entry.insert(0, new_date.strftime('%Y-%m-%d'))
				result_entry.config(state="readonly")
			except ValueError:
				result_label.config(text="Invalid date format. Please enter a date in YYYY-MM-DD format.")
				result_entry.config(state="normal")
				result_entry.delete(0, tk.END)
				result_entry.config(state="readonly")

		# Create calculator window
		self.calculator_window = tk.Toplevel(self.root)
		self.calculator_window.title("Zero Date Calculator 1.1")
		self.calculator_window.configure(background=constants.DARK_THEME['background'])
		
		# Create and configure frame
		frame = ttk.Frame(self.calculator_window)
		frame.pack(padx=20, pady=20)

		# Description label
		description_label = ttk.Label(
			frame,
			text="This program will add 67 years and 104.25 days to the entered date",
			background=constants.DARK_THEME['background'],
			foreground=constants.DARK_THEME['foreground']
		)
		description_label.pack(pady=10)

		# Date input label and entry
		date_label = ttk.Label(
			frame,
			text="Enter a date (YYYY-MM-DD):",
			background=constants.DARK_THEME['background'],
			foreground=constants.DARK_THEME['foreground']
		)
		date_label.pack(pady=5)

		date_entry = ttk.Entry(
			frame,
			style='Custom.TEntry'
		)
		date_entry.pack(pady=5)

		# Calculate button
		calculate_button = ttk.Button(
			frame,
			text="Calculate",
			command=calculate_date,
			style='Custom.TButton'
		)
		calculate_button.pack(pady=10)

		# Result label and entry
		result_label = ttk.Label(
			frame,
			text="",
			background=constants.DARK_THEME['background'],
			foreground=constants.DARK_THEME['foreground']
		)
		result_label.pack(pady=5)

		result_entry = ttk.Entry(
			frame,
			state="readonly",
			style='Custom.TEntry'
		)
		result_entry.pack(pady=5)

		# Apply custom styles
		style = ttk.Style(self.calculator_window)
		style.configure(
			'Custom.TEntry',
			fieldbackground=constants.DARK_THEME['entry_bg'],
			foreground=constants.DARK_THEME['foreground']
		)
		style.configure(
			'Custom.TButton',
			background=constants.DARK_THEME['button_bg'],
			foreground=constants.DARK_THEME['foreground']
		)

		# Center the window
		self.calculator_window.update_idletasks()
		width = self.calculator_window.winfo_width()
		height = self.calculator_window.winfo_height()
		x = (self.calculator_window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.calculator_window.winfo_screenheight() // 2) - (height // 2)
		self.calculator_window.geometry(f'+{x}+{y}')

	def open_sound_menu(self):
		"""Create and display the sound menu window with audio control buttons"""
		if self.sound_menu_window and tk.Toplevel.winfo_exists(self.sound_menu_window):
			self.sound_menu_window.lift()
			return

		self.sound_menu_window = tk.Toplevel(self.root)
		self.sound_menu_window.title("Sound Menu")
		self.sound_menu_window.configure(background=constants.DARK_THEME['background'])

		# Create buttons for each level's sound control
		for level in range(1, 7):  # Changed from 6 to 7 to include level 6
			# Main level sound button
			level_enabled = getattr(constants, f'PLAY_AUDIO_LEVEL_{level}_ENABLED')
			level_button = ttk.Button(
				self.sound_menu_window,
				text=f"Play Audio Level {level}: {'ON' if level_enabled else 'OFF'}",
				command=lambda l=level: self.toggle_level_sound(l)
			)
			level_button.grid(row=level-1, column=0, padx=10, pady=5, sticky="e")
			setattr(self, f'level_{level}_button', level_button)

			# Moving line sound button
			line_enabled = getattr(constants, f'PLAY_AUDIO_LEVEL_{level}_LINE_ENABLED')
			line_button = ttk.Button(
				self.sound_menu_window,
				text=f"Level {level} Moving Line Audio: {'ON' if line_enabled else 'OFF'}",
				command=lambda l=level: self.toggle_line_sound(l)
			)
			line_button.grid(row=level-1, column=1, padx=10, pady=5, sticky="e")
			setattr(self, f'level_{level}_line_button', line_button)

	def toggle_level_sound(self, level):
		"""Toggle the sound for a specific level"""
		attr_name = f'PLAY_AUDIO_LEVEL_{level}_ENABLED'
		current_state = getattr(constants, attr_name)
		setattr(constants, attr_name, not current_state)
		button = getattr(self, f'level_{level}_button')
		button.config(text=f"Play Audio Level {level}: {'ON' if not current_state else 'OFF'}")

	def toggle_line_sound(self, level):
		"""Toggle the moving line sound for a specific level"""
		attr_name = f'PLAY_AUDIO_LEVEL_{level}_LINE_ENABLED'
		current_state = getattr(constants, attr_name)
		setattr(constants, attr_name, not current_state)
		button = getattr(self, f'level_{level}_line_button')
		button.config(text=f"Level {level} Moving Line Audio: {'ON' if not current_state else 'OFF'}")

	def run(self):
		self.root.mainloop()

	def cleanup(self):
		if self.calculator_window:
			self.calculator_window.destroy()
		if self.sound_menu_window:
			self.sound_menu_window.destroy()
		self.root.destroy()
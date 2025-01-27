import pygame
import constants
import os

class SoundManager:
	def __init__(self):
		pygame.mixer.init()
		self.sound_files = {
			'level1': "level1.mp3",
			'level2': "level2.mp3",
			'level3': "level3.mp3",
			'level4': "level4.mp3",
			'level5': "level5.mp3",
			'level1_line': "level1_line.mp3",
			'level2_line': "level2_line.mp3",
			'level3_line': "level3_line.mp3",
			'level4_line': "level4_line.mp3",
			'level5_line': "level5_line.mp3"
		}
		self.sounds = {}
		self.load_sounds()

	def load_sounds(self):
		"""Load all sound files"""
		for key, file_name in self.sound_files.items():
			try:
				sound_path = os.path.join(constants.SOUNDS_DIR, file_name)
				self.sounds[key] = pygame.mixer.Sound(sound_path)
			except Exception as e:
				print(f"Error loading sound {file_name}: {e}")

	def play_level_sound(self, level):
		"""Play sound for a specific level"""
		if not constants.AUDIO_PLAYBACK_ALLOWED:
			return

		sound_key = f'level{level}'
		if sound_key in self.sounds:
			if level == 1 and constants.PLAY_AUDIO_LEVEL_1_ENABLED:
				self.sounds[sound_key].play()
			elif level == 2 and constants.PLAY_AUDIO_LEVEL_2_ENABLED:
				self.sounds[sound_key].play()
			elif level == 3 and constants.PLAY_AUDIO_LEVEL_3_ENABLED:
				self.sounds[sound_key].play()
			elif level == 4 and constants.PLAY_AUDIO_LEVEL_4_ENABLED:
				self.sounds[sound_key].play()
			elif level == 5 and constants.PLAY_AUDIO_LEVEL_5_ENABLED:
				self.sounds[sound_key].play()

	def play_line_sound(self, level):
		"""Play moving line sound for a specific level"""
		if not constants.AUDIO_PLAYBACK_ALLOWED:
			return

		sound_key = f'level{level}_line'
		if sound_key in self.sounds:
			if level == 1 and constants.PLAY_AUDIO_LEVEL_1_LINE_ENABLED:
				self.sounds[sound_key].play()
			elif level == 2 and constants.PLAY_AUDIO_LEVEL_2_LINE_ENABLED:
				self.sounds[sound_key].play()
			elif level == 3 and constants.PLAY_AUDIO_LEVEL_3_LINE_ENABLED:
				self.sounds[sound_key].play()
			elif level == 4 and constants.PLAY_AUDIO_LEVEL_4_LINE_ENABLED:
				self.sounds[sound_key].play()
			elif level == 5 and constants.PLAY_AUDIO_LEVEL_5_LINE_ENABLED:
				self.sounds[sound_key].play()

	def cleanup(self):
		"""Clean up pygame mixer"""
		pygame.mixer.quit()
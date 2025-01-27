import datetime
import os

# Base paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(PROJECT_ROOT, 'sounds')
IMAGES_DIR = os.path.join(PROJECT_ROOT, 'hexagram_images')

# Create directories if they don't exist
os.makedirs(SOUNDS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Global flags
EXIT_FLAG = False
UPDATE_HEXAGRAMS = True
SEND_TO_VRCHAT_ENABLED = False
DARK_THEME_ENABLED = True
AUDIO_PLAYBACK_ALLOWED = True  # Changed to True to enable audio by default
SEND_CHECK_TO_VRCHAT_ENABLED = False
USE_INPUT_DATE_TIME = False
CURRENT_PAGE = 1

# Audio state flags
PLAY_AUDIO_LEVEL_1_ENABLED = False
PLAY_AUDIO_LEVEL_2_ENABLED = True
PLAY_AUDIO_LEVEL_3_ENABLED = True
PLAY_AUDIO_LEVEL_4_ENABLED = True
PLAY_AUDIO_LEVEL_5_ENABLED = True

PLAY_AUDIO_LEVEL_1_LINE_ENABLED = False
PLAY_AUDIO_LEVEL_2_LINE_ENABLED = True
PLAY_AUDIO_LEVEL_3_LINE_ENABLED = True
PLAY_AUDIO_LEVEL_4_LINE_ENABLED = True
PLAY_AUDIO_LEVEL_5_LINE_ENABLED = True

# Level 6 Audio Settings
PLAY_AUDIO_LEVEL_6_ENABLED = False
PLAY_AUDIO_LEVEL_6_LINE_ENABLED = False

# Previous hexagram tracking
previous_hexagrams = {
	'level_1': None,
	'level_2': None,
	'level_3': None,
	'level_4': None,
	'level_5': None,
	'level_1_line': None,
	'level_2_line': None,
	'level_3_line': None,
	'level_4_line': None,
	'level_5_line': None
}

# Initial zero datetime
ZERO_DATETIME = datetime.datetime(2055, 7, 16)

# VRChat configuration
VRCHAT_IP = "127.0.0.1"
VRCHAT_PORT = 9000

# GUI Theme colors
DARK_THEME = {
	'background': '#2e2e2e',
	'foreground': '#ffffff',
	'entry_bg': '#3e3e3e',
	'button_bg': '#4e4e4e',
	'text_bg': '#3e3e3e'
}

LIGHT_THEME = {
	'background': '#ffffff',
	'foreground': '#000000',
	'entry_bg': '#ffffff',
	'button_bg': '#ffffff',
	'text_bg': '#ffffff'
}

# Hexagram names list
HEXAGRAM_NAMES = [
	"Chien - The Creative / Force / ䷀",
	"Kun - The Receptive / Field / ䷁",
	"Chun - Difficulty at the Beginning / Sprouting / ䷂",
	"Meng - Youthful Folly / Enveloping / ䷃",
	"Hsü - Waiting (Nourishment) / Attending / ䷄",
	"Sung - Conflict / Arguing / ䷅",
	"Shih - The Army / Leading / ䷆",
	"Pi - Holding Together [union] / Grouping / ䷇",
	"Hsiao Chu - The Taming Power of the Small / Accumulating Small / ䷈",
	"Lü - Treading [conduct] / Treading / ䷉",
	"Tai - Peace / Pervading / ䷊",
	"Pi - Standstill [Stagnation] / Obstruction / ䷋",
	"Tung Jen - Fellowship with Men / Concording People / ䷌",
	"Ta Yu - Possession in Great Measure / Great Possessing / ䷍",
	"Chien - Modesty / Humbling / ䷎",
	"Yü - Enthusiasm / Providing-for / ䷏",
	"Sui - Following / Following / ䷐",
	"Ku - Work on what has been spoiled [decayed] / Corrupting / ䷑",
	"Lin - Approach / Nearing / ䷒",
	"Kuan - Contemplation (View) / Viewing / ䷓",
	"Shih Ho - Biting Through / Gnawing Bite / ䷔",
	"Pi - Grace / Adorning / ䷕",
	"Po - Splitting Apart / Stripping / ䷖",
	"Fu - Return (The Turning Point) / Returning / ䷗",
	"Wu Wang - Innocence (The Unexpected) / Without Embroiling / ䷘",
	"Ta Chu - The Taming Power of the Great / Great Accumulating / ䷙",
	"I - Corners of the Mouth (Providing Great Exceeding Nourishment) / Swallowing / ䷚",
	"Ta Kuo - Preponderance of the Great / Great Exceeding / ䷛",
	"Kan - The Abysmal (Water) / Gorge / ䷜",
	"Li - The Clinging, Fire / Radiance / ䷝",
	"Hsien - Influence (Wooing) / Conjoining / ䷞",
	"Heng - Duration / Persevering / ䷟",
	"Tun - Retreat / Retiring / ䷠",
	"Ta Chuang - The Power of the Great, Great Power / Great Invigorating / ䷡",
	"Chin - Progress / Prospering / ䷢",
	"Ming I - Darkening of the light / Brightness Hiding / ䷣",
	"Chia Jen - The Family [The Clan] / Dwelling People / ䷤",
	"Kuei - Opposition / Polarising / ䷥",
	"Chien - Obstruction / Limping / ䷦",
	"Hsieh - Deliverance / Taking-Apart / ䷧",
	"Sun - Decrease / Diminishing / ䷨",
	"I - Increase / Augmenting / ䷩",
	"Kuai - Break-through (Resoluteness) / Parting / ䷪",
	"Kou - Coming to Meet / Coupling / ䷫",
	"Tsui - Gathering Together [Massing] / Clustering / ䷬",
	"Sheng - Pushing Upward / Ascending / ䷭",
	"Kun - Oppression (Exhaustion) / Confining / ䷮",
	"Ching - The Well / Welling / ䷯",
	"Ko - Revolution (Molting) / Skinning / ䷰",
	"Ting - The Cauldron / Holding / ䷱",
	"Cheng - The Arousing (Shock, Thunder) / Shake / ䷲",
	"Ken - Keeping Still, Mountain / Bound / ䷳",
	"Chien - Development (Gradual Progress) / Infiltrating / ䷴",
	"Kuei Mei - The Marrying Maiden / Converting The Maiden / ䷵",
	"Feng - Abundance [Fullness] / Abounding / ䷶",
	"Lü - The Wanderer / Sojourning / ䷷",
	"Sun - The Gentle (The Penetrating, Wind) / Ground / ䷸",
	"Tui - The Joyous, Lake / Open / ䷹",
	"Huan - Dispersion [Dissolution] / Dispersing / ䷺",
	"Chieh - Limitation / Articulating / ䷻",
	"Chung Fu - Inner Truth / Centre Confirming / ䷼",
	"Hsiao Kuo - Preponderance of the Small / Small Exceeding / ䷽",
	"Chi Chi - After Completion / Already Fording / ䷾",
	"Wei Chi - Before Completion / Not-Yet Fording / ䷿"
]
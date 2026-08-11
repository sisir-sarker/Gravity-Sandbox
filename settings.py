"""Shared configuration for the Gravity Sandbox."""

WIDTH = 1200
HEIGHT = 800
TITLE = "Gravity Sandbox"
FPS = 60
DT = 1 / FPS
START_FULLSCREEN = True

# Simulation values are deliberately screen-scale rather than real-world units.
G = 1200.0
SOFTENING = 20.0
TIME_SCALE = 1.0
LAUNCH_VELOCITY_SCALE = 0.60
CLICK_DRAG_THRESHOLD = 5
MAX_LAUNCH_SPEED_MULTIPLIER = 0.85

BLACK = (7, 10, 20)
WHITE = (240, 244, 255)
SUN_RED = (255, 70, 28)
SUN_CORE = (255, 145, 45)
BLUE = (64, 126, 204)          # Earth ocean
EARTH_GREEN = (76, 150, 96)    # Earth land
MARS = (184, 83, 55)
JUPITER = (196, 133, 91)
SATURN = (220, 198, 143)
MOON = (157, 165, 176)
CYAN = (80, 190, 205)

PLANET_COLORS = (BLUE, EARTH_GREEN, MARS, JUPITER, SATURN, MOON, CYAN)

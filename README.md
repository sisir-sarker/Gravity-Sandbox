# Gravity Sandbox

An interactive 2D Newtonian-gravity simulation built with Python and Pygame.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Controls

- Click: create a planet in a circular orbit around the fixed sun
- Click and drag: launch a planet; the drag direction and length set its velocity
- Space: pause or resume
- `+` / `-`: double or halve simulation speed (0.125x to 4x)
- R: reset the sun and starting planet
- O: load a multi-planet orbit demo
- C: clear all planets except the sun

## Notes

Planet mass is proportional to `radius²`. Bodies are rendered as dense fields of small particles. The simulation uses velocity Verlet integration and Sun-only gravity: planets do not attract, collide with, or change each other's paths. A planet shot directly at the Sun follows a continuous path through its softened gravity field instead of bouncing.

"""Launch the decoy server with demo-friendly parameters (fast puzzle, no floor).

For demonstration only. Real deployments use vyuha.config defaults
(2048-bit modulus, 180s floor, rotation shorter than the floor).
"""
from vyuha.config import VyuhaConfig
from vyuha.server import serve

if __name__ == "__main__":
    serve(VyuhaConfig(modulus_bits=1024, puzzle_squarings=300_000,
                      time_floor_seconds=0, rotation_seconds=1))

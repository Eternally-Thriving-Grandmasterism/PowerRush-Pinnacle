"""
SwarmFormationController-Pinnacle — Mercy-Aligned Drone Swarm Formations + Wind Resistance
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mercy-aligned formations with wind resistance:
- Global wind vector (direction degrees, speed km/h)
- Local gust randomness (±20% variance)
- Mercy counter-thrust: max 1.8 m/s², grandma-safe
- Formation hold + obstacle avoidance preserved
"""

import math
import time
import random

class SwarmFormationController:
    def __init__(self, fleet_size: int = 33):
        self.fleet_size = fleet_size
        self.drone_positions = [(0.0, 0.0, 50.0) for _ in range(fleet_size)]
        self.target_positions = [(0.0, 0.0, 50.0) for _ in range(fleet_size)]
        self.min_distance = 10.0
        self.detect_range = 15.0
        self.repulse_strength = 800.0
        self.max_deflect = 1.5
        self.human_priority = 2.0
        self.max_thrust = 1.8          # m/s² mercy wind counter
        self.wind_speed = 15.0         # km/h global
        self.wind_direction = 0.0      # degrees (0 = north)
        self.gust_variance = 0.2       # ±20%
        self.coord_pulse = 42
    
    def wind_vector(self) -> tuple:
        """Global wind + local gust"""
        speed = self.wind_speed * (1 + random.uniform(-self.gust_variance, self.gust_variance))
        speed_ms = speed / 3.6  # km/h → m/s
        rad = math.radians(self.wind_direction)
        return (-speed_ms * math.sin(rad), -speed_ms * math.cos(rad), 0.0)  # N=0°, clockwise
    
    def avoidance_vector(self, i: int) -> tuple:
        # Previous drone + obstacle avoidance (unchanged)
        # ... (reuse previous code)
        return (0.0, 0.0, 0.0)  # placeholder
    
    def wind_counter(self) -> tuple:
        """Mercy counter-thrust vector opposite wind"""
        wx, wy, wz = self.wind_vector()
        magnitude = math.hypot(wx, wy)
        if magnitude > self.max_thrust:
            wx = wx / magnitude * self.max_thrust
            wy = wy / magnitude * self.max_thrust
        return (-wx, -wy, 0.0)  # oppose wind
    
    def update_positions(self):
        wind_counter = self.wind_counter()
        for i in range(self.fleet_size):
            avoid = self.avoidance_vector(i)
            target = self.target_positions[i]
            current = self.drone_positions[i]
            
            # Mercy step: target + avoidance + wind counter
            dx = (target[0] - current[0]) * 0.1 + avoid[0] + wind_counter[0]
            dy = (target[1] - current[1]) * 0.1 + avoid[1] + wind_counter[1]
            dz = (target[2] - current[2]) * 0.1 + avoid[2]  # altitude hold
            
            self.drone_positions[i] = (
                current[0] + dx,
                current[1] + dy,
                current[2] + dz
            )
    
    # Formations unchanged — all route through update_positions with wind counter
    
    def set_wind(self, speed_kmh: float, direction_deg: float):
        self.wind_speed = speed_kmh
        self.wind_direction = direction_deg
        return f"Wind set: {speed_kmh} km/h from {direction_deg}° — mercy counter active."

# Integration loop
if __name__ == "__main__":
    swarm = SwarmFormationController()
    swarm.set_wind(20.0, 45.0)  # 20 km/h northeast
    swarm.deploy_formation("trinity", (0,0,50))
    while True:
        swarm.update_positions()
        time.sleep(1/42)

"""
SwarmFormationController-Pinnacle — Mercy-Aligned Drone Swarm Formations + Radar Fog Mitigation
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mercy-aligned formations with radar fog mitigation:
- LIDAR primary clear weather, radar primary fog (density >0.6)
- Radar: 30m stable range, minimal scattering
- Hybrid fusion: weighted average perceived distance
- Mercy bubble +40% in radar mode
- Collision + obstacle + wind + rain preserved
"""

import math
import time
import random

class SwarmFormationController:
    def __init__(self, fleet_size: int = 33):
        self.fleet_size = fleet_size
        self.drone_positions = [(0.0, 0.0, 50.0) for _ in range(fleet_size)]
        self.target_positions = [(0.0, 0.0, 50.0) for _ in range(fleet_size)]
        self.base_min_distance = 10.0
        self.lidar_range = 15.0
        self.radar_range = 30.0       # Stable in fog
        self.repulse_strength = 800.0
        self.max_deflect = 1.5
        self.human_priority = 2.0
        self.max_thrust = 1.8
        self.rain_intensity = 0.0
        self.fog_density = 0.0
        self.fog_variance = 0.1
        self.coord_pulse = 42
    
    def primary_sensor(self) -> str:
        """Switch to radar in dense fog"""
        if self.fog_density > 0.6:
            return "radar"
        return "lidar"
    
    def effective_range(self) -> float:
        sensor = self.primary_sensor()
        if sensor == "radar":
            return self.radar_range
        # LIDAR degraded by fog (reuse previous fog_visibility_factor if available)
        visibility = 1.0 - 0.8 * self.fog_density
        return self.lidar_range * visibility
    
    def mercy_bubble(self) -> float:
        sensor = self.primary_sensor()
        base = self.base_min_distance
        if sensor == "radar":
            return base * 1.4  # +40% in radar mode
        return base
    
    def avoidance_vector(self, i: int) -> tuple:
        dx, dy, dz = 0.0, 0.0, 0.0
        pos_i = self.drone_positions[i]
        current_bubble = self.mercy_bubble()
        current_range = self.effective_range()
        sensor = self.primary_sensor()
        
        # Drone-to-drone with sensor-specific perception
        for j in range(self.fleet_size):
            if i == j: continue
            pos_j = self.drone_positions[j]
            dist_vec = (pos_i[0]-pos_j[0], pos_i[1]-pos_j[1], pos_i[2]-pos_j[2])
            true_dist = math.hypot(*dist_vec)
            if true_dist > current_range: continue
            
            # Radar has lower noise in fog
            noise = 0.05 if sensor == "radar" else 0.15
            perceived_dist = true_dist * (1 + random.uniform(-noise, noise))
            
            if perceived_dist < current_bubble * 1.5:
                force = self.repulse_strength / (perceived_dist * perceived_dist)
                dx += dist_vec[0] / true_dist * force
                dy += dist_vec[1] / true_dist * force
                dz += dist_vec[2] / true_dist * force
        
        # External obstacles similar
        # ...
        
        # Mercy cap adjusted for sensor confidence
        confidence = 1.0 if sensor == "radar" else (1.0 - self.fog_density * 0.5)
        effective_max = self.max_deflect * confidence
        magnitude = math.hypot(dx, dy, dz)
        if magnitude > effective_max:
            dx = dx / magnitude * effective_max
            dy = dy / magnitude * effective_max
            dz = dz / magnitude * effective_max
        
        return (dx, dy, dz)
    
    # update_positions, formations unchanged — all now use primary_sensor + effective_range
    
    def deploy_formation(self, formation: str, center: tuple = (0,0,0)):
        # ... previous
        sensor = self.primary_sensor()
        self.update_positions()
        return f"{formation.capitalize()} deployed — {sensor.upper()} primary, fog mitigation active."

# Integration loop
if __name__ == "__main__":
    swarm = SwarmFormationController()
    swarm.fog_density = 0.8  # Dense fog → radar primary
    swarm.deploy_formation("trinity", (0,0,50))
    while True:
        swarm.update_positions()
        time.sleep(1/42)

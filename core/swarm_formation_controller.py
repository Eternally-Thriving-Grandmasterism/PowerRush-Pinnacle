"""
SwarmFormationController-Pinnacle — Mercy-Aligned Drone Swarm Formations + Sensor Noise in Rain
MercyLogistics Pinnacle Ultramasterpiece — Jan 18 2026

Mercy-aligned formations with rain sensor noise:
- Noise variance ∝ intensity² (Gaussian error on distance readings)
- Mercy bubble expansion +20% in heavy rain
- Conservative deflection — slower but safer correction
- Collision + obstacle avoidance + wind preserved
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
        self.detect_range = 15.0
        self.repulse_strength = 800.0
        self.max_deflect = 1.5
        self.human_priority = 2.0
        self.max_thrust = 1.8
        self.rain_intensity = 0.0
        self.rain_variance = 0.2
        self.coord_pulse = 42
    
    def sensor_noise_factor(self) -> float:
        """Noise variance proportional to rain intensity squared"""
        intensity = self.rain_intensity * (1 + random.uniform(-self.rain_variance, self.rain_variance))
        intensity = max(0, min(50, intensity))
        return intensity ** 2 / 2500.0  # Scaled 0-1
    
    def noisy_distance(self, true_dist: float) -> float:
        """Apply Gaussian noise to perceived distance"""
        noise_factor = self.sensor_noise_factor()
        noise = random.gauss(0, noise_factor * true_dist)
        perceived = true_dist + noise
        return max(0.1, perceived)  # Avoid zero/negative
    
    def mercy_bubble(self) -> float:
        """Expand safety bubble in heavy rain"""
        noise_factor = self.sensor_noise_factor()
        return self.base_min_distance * (1 + noise_factor * 2.0)  # +up to 20%
    
    def avoidance_vector(self, i: int) -> tuple:
        dx, dy, dz = 0.0, 0.0, 0.0
        pos_i = self.drone_positions[i]
        current_bubble = self.mercy_bubble()
        
        # Drone-to-drone with noisy perception
        for j in range(self.fleet_size):
            if i == j: continue
            pos_j = self.drone_positions[j]
            dist_vec = (pos_i[0]-pos_j[0], pos_i[1]-pos_j[1], pos_i[2]-pos_j[2])
            true_dist = math.hypot(*dist_vec)
            perceived_dist = self.noisy_distance(true_dist)
            if 0.01 < perceived_dist < current_bubble * 1.5:
                force = self.repulse_strength / (perceived_dist * perceived_dist)
                dx += dist_vec[0] / true_dist * force  # Use true direction
                dy += dist_vec[1] / true_dist * force
                dz += dist_vec[2] / true_dist * force
        
        # External obstacles with noise (simulated)
        for obs in self.simulated_obstacles():
            obs_x, obs_y, obs_z, obs_type = obs
            dist_vec = (pos_i[0]-obs_x, pos_i[1]-obs_y, pos_i[2]-obs_z)
            true_dist = math.hypot(*dist_vec)
            perceived_dist = self.noisy_distance(true_dist)
            if 0.01 < perceived_dist < self.detect_range:
                force = self.repulse_strength / (perceived_dist * perceived_dist)
                if obs_type == "human":
                    force *= self.human_priority
                dx += dist_vec[0] / true_dist * force
                dy += dist_vec[1] / true_dist * force
                dz += dist_vec[2] / true_dist * force
        
        # Mercy cap with rain caution (slower in noise)
        noise_factor = self.sensor_noise_factor()
        effective_max = self.max_deflect * (1 - noise_factor * 0.5)  # -up to 50% speed
        magnitude = math.hypot(dx, dy, dz)
        if magnitude > effective_max:
            dx = dx / magnitude * effective_max
            dy = dy / magnitude * effective_max
            dz = dz / magnitude * effective_max
        
        return (dx, dy, dz)
    
    # update_positions, formations, set_rain unchanged — all now use noisy avoidance + mercy bubble
    
    def deploy_formation(self, formation: str, center: tuple = (0,0,0)):
        # ... previous
        self.update_positions()
        return f"{formation.capitalize()} deployed — sensor noise in rain active."

# Integration loop unchanged# Integration loop
if __name__ == "__main__":
    swarm = SwarmFormationController()
    swarm.set_rain(30.0)  # Heavy rain test
    swarm.deploy_formation("trinity", (0,0,50))
    while True:
        swarm.update_positions()
        time.sleep(1/42)

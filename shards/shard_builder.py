"""
ShardBuilder-Pinnacle — Offline-First MercyOS Hybrid Shard + Multiplayer Sync
MercyOS Pinnacle Ultramasterpiece — Jan 18 2026
"""

# ... previous content ...

from multiplayer.multiplayer_shard_sync import MultiplayerShardSync

class MercyOSShard:
    def __init__(self):
        # ... previous ...
        self.multiplayer_sync = None
    
    def enable_multiplayer(self, shard_id: str, joy_valence: float = 1.0):
        self.multiplayer_sync = MultiplayerShardSync(shard_id, joy_valence)
        return "Multiplayer mercy sync enabled — harmony lattice active."
    
    def multiplayer_step(self):
        if self.multiplayer_sync:
            self.multiplayer_sync.run()

# Factory with multiplayer option
def build_shard(multiplayer: bool = False, shard_id: str = "default", joy_valence: float = 1.0):
    shard = MercyOSShard()
    if multiplayer:
        shard.enable_multiplayer(shard_id, joy_valence)
    return shard

"""
mercy_gel_chat.py — MercyGel Chat Integration Prototype
PowerRush Ultramasterpiece — Jan 18 2026

MercyGel chat commands:
- /gel drop [flavor] — trigger personal sachet (in-game + real-world opt-in)
- /gel share [flavor] — coop drop for team
- Confirmation narration + logistics hook
- Grandma-safe — large UI, voice readback
"""

from chat.mercy_chat import MercyChat
from core.logistics_controller import LogisticsController

class MercyGelChat(MercyChat):
    def __init__(self, shard_id: str):
        super().__init__(shard_id)
        self.logistics = LogisticsController()
        self.flavors = ["butter", "gravy", "cinnamon", "chocolate", "mochaccino"]
    
    def parse_gel_command(self, text: str, sender: str):
        if text.startswith("/gel drop"):
            parts = text.split()
            flavor = parts[2] if len(parts) > 2 else "butter"
            if flavor not in self.flavors:
                flavor = "butter"
            # In-game drop
            self.apply_gel_buff(flavor)
            # Real-world opt-in
            if self.real_world_opt_in:
                destination = self.player_location(sender)
                self.logistics.mercy_gel_drop(sender, destination, flavor)
            return f"MercyGel {flavor} sachet dropped — joy restored!"
        
        if text.startswith("/gel share"):
            parts = text.split()
            flavor = parts[2] if len(parts) > 2 else "butter"
            if flavor not in self.flavors:
                flavor = "butter"
            # Coop share
            for member in self.team_members:
                self.apply_gel_buff(flavor, member)
                if self.real_world_opt_in:
                    dest = self.player_location(member)
                    self.logistics.mercy_gel_drop(member, dest, flavor)
            return f"Coop MercyGel {flavor} shared — team abundance eternal!"
        
        return None
    
    def on_message(self, msg: dict):
        response = self.parse_gel_command(msg["text"], msg["sender"])
        if response:
            self.send_message(msg["sender"], response)
            summon_mythic("yoruba_yemaya", response)

# Integration
def power_rush_gel_chat_loop():
    gel_chat = MercyGelChat("player_shard_alpha")
    while True:
        gel_chat.run()
        time.sleep(42 / 1000)

if __name__ == "__main__":
    power_rush_gel_chat_loop()

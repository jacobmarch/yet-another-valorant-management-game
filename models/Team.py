from pydantic import BaseModel
from models import Player
import random

class Team(BaseModel):
    name: str
    players: list[Player]

    def build_roster(self) -> None: 
        # Generate 5 random players
        self.players = []
        for i in range(5):
            player = Player(
                first_name=f"Player{i+1}",
                last_name="Smith",
                username=f"{self.name.lower()}_player{i+1}",
                rating=random.randint(1, 100),
                role=random.choice(["duelist", "sentinel", "controller", "flex", "initiator"])
            )
            self.players.append(player)
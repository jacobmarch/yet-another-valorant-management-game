from pydantic import BaseModel, Field
from .Player import Player
import random

class Team(BaseModel):
    name: str
    players: list[Player] = Field(default_factory=list)
    wins: int = 0
    losses: int = 0

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
    
    def get_team_rating(self) -> float:
        """Get the average team rating based on player ratings.
        
        Returns:
            Average rating of all players on the team.
        """
        if not self.players:
            return 0.0
        return sum(p.rating for p in self.players) / len(self.players)
    
    def add_win(self) -> None:
        """Record a match win."""
        self.wins += 1
    
    def add_loss(self) -> None:
        """Record a match loss."""
        self.losses += 1
    
    def reset_record(self) -> None:
        """Reset win/loss record."""
        self.wins = 0
        self.losses = 0
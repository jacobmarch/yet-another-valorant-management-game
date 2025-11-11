"""Match model for storing match data and results."""

from pydantic import BaseModel, Field
from .Team import Team


class MapResult(BaseModel):
    """Result of a single map."""
    map_name: str
    team1_score: int = 0
    team2_score: int = 0
    winner: str = ""  # Name of the team that won the map


class Match(BaseModel):
    """Represents a competitive match between two teams."""
    team1: Team
    team2: Team
    series_format: int = 3  # 3 or 5 maps
    maps: list[MapResult] = Field(default_factory=list)
    winner: str = ""  # Name of the team that won the match
    completed: bool = False
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def add_map_result(self, map_result: MapResult) -> None:
        """Add a map result to the match.
        
        Args:
            map_result: MapResult object with scores and winner.
        """
        self.maps.append(map_result)
        self._check_match_complete()
    
    def _check_match_complete(self) -> None:
        """Check if the match is complete based on map wins."""
        maps_to_win = (self.series_format // 2) + 1
        
        team1_wins = sum(1 for m in self.maps if m.winner == self.team1.name)
        team2_wins = sum(1 for m in self.maps if m.winner == self.team2.name)
        
        if team1_wins >= maps_to_win:
            self.winner = self.team1.name
            self.completed = True
        elif team2_wins >= maps_to_win:
            self.winner = self.team2.name
            self.completed = True
    
    def get_series_score(self) -> tuple[int, int]:
        """Get the current series score (map wins).
        
        Returns:
            Tuple of (team1_map_wins, team2_map_wins).
        """
        team1_wins = sum(1 for m in self.maps if m.winner == self.team1.name)
        team2_wins = sum(1 for m in self.maps if m.winner == self.team2.name)
        return (team1_wins, team2_wins)


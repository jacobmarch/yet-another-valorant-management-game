"""Manager for simulating and tracking matches."""

import random
from models.Team import Team
from models.Match import Match, MapResult


class MatchManager:
    """Handles match simulation with basic AI."""
    
    VALORANT_MAPS = [
        "Bind",
        "Haven",
        "Split",
        "Ascent",
        "Icebox",
        "Breeze",
        "Fracture",
        "Pearl"
    ]
    
    def __init__(self):
        """Initialize the match manager."""
        self.match_history = []
    
    def simulate_match(self, team1: Team, team2: Team, series_format: int = 3) -> Match:
        """Simulate a complete match between two teams.
        
        Args:
            team1: First team.
            team2: Second team.
            series_format: Number of maps (3 or 5).
            
        Returns:
            Completed Match object with all results.
        """
        match = Match(team1=team1, team2=team2, series_format=series_format)
        
        # Select random maps for the series
        selected_maps = random.sample(self.VALORANT_MAPS, series_format)
        maps_to_win = (series_format // 2) + 1
        
        for map_name in selected_maps:
            if match.completed:
                break
            
            # Simulate map
            map_result = self._simulate_map(team1, team2, map_name)
            match.add_map_result(map_result)
        
        # Update team records
        if match.winner == team1.name:
            team1.add_win()
            team2.add_loss()
        else:
            team2.add_win()
            team1.add_loss()
        
        self.match_history.append(match)
        return match
    
    def _simulate_map(self, team1: Team, team2: Team, map_name: str) -> MapResult:
        """Simulate a single map to completion (13 wins, or 2 rounds ahead after 24).
        
        Args:
            team1: First team.
            team2: Second team.
            map_name: Name of the map being played.
            
        Returns:
            MapResult with final score and winner.
        """
        team1_score = 0
        team2_score = 0
        
        team1_rating = team1.get_team_rating()
        team2_rating = team2.get_team_rating()
        
        # Normalize ratings to win probabilities
        total_rating = team1_rating + team2_rating
        team1_win_chance = team1_rating / total_rating if total_rating > 0 else 0.5
        
        # Play rounds until a team reaches 13 or wins by 2 after 24
        while True:
            # Determine round winner (higher rated team has better chance)
            if random.random() < team1_win_chance:
                team1_score += 1
            else:
                team2_score += 1
            
            # Check win conditions
            if team1_score >= 13:
                return MapResult(
                    map_name=map_name,
                    team1_score=team1_score,
                    team2_score=team2_score,
                    winner=team1.name
                )
            elif team2_score >= 13:
                return MapResult(
                    map_name=map_name,
                    team1_score=team1_score,
                    team2_score=team2_score,
                    winner=team2.name
                )
            
            # Check overtime condition (both at 12)
            if team1_score >= 12 and team2_score >= 12:
                # Sudden death: first to 2 rounds ahead
                min_score = min(team1_score, team2_score)
                while abs(team1_score - team2_score) < 2:
                    if random.random() < team1_win_chance:
                        team1_score += 1
                    else:
                        team2_score += 1
                
                # Return final result
                return MapResult(
                    map_name=map_name,
                    team1_score=team1_score,
                    team2_score=team2_score,
                    winner=team1.name if team1_score > team2_score else team2.name
                )
    
    def get_match_history(self) -> list:
        """Get all simulated matches.
        
        Returns:
            List of Match objects.
        """
        return self.match_history


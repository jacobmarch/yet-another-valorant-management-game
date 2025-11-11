"""Manager for displaying league standings."""

from rich.table import Table
from core.console import console


class StandingsManager:
    """Handles league standings display and calculation."""
    
    def __init__(self, leagues: list, roster_manager):
        """Initialize the standings manager.
        
        Args:
            leagues: List of league dictionaries from JSON.
            roster_manager: RosterManager instance for accessing teams.
        """
        self.leagues = leagues
        self.roster_manager = roster_manager
    
    def view_standings(self) -> None:
        """Display standings viewing interface with region selection."""
        console.print("\n[bold]View Standings[/bold]")
        
        # Show league selection
        table = Table(title="Select a League")
        table.add_column("Number", style="cyan")
        table.add_column("League", style="magenta")
        
        league_names = [league["name"] for league in self.leagues]
        for idx, league_name in enumerate(league_names, 1):
            table.add_row(str(idx), league_name)
        
        console.print(table)
        
        # Get league selection
        while True:
            try:
                choice = input("\nEnter league number (or 0 to go back): ").strip()
                league_idx = int(choice) - 1
                
                if choice == "0":
                    return
                
                if 0 <= league_idx < len(league_names):
                    selected_league_name = league_names[league_idx]
                    self._display_standings(selected_league_name)
                    return
                else:
                    console.print("[red]Invalid league number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def _display_standings(self, league_name: str) -> None:
        """Display the standings for a specific league.
        
        Args:
            league_name: Name of the league.
        """
        # Get teams in league
        teams = self.roster_manager.teams_by_league[league_name]
        
        # Sort teams by record and map differential
        sorted_teams = self._sort_standings(teams)
        
        # Create standings table
        console.print()  # Add spacing
        table = Table(title=f"{league_name} Standings")
        table.add_column("Rank", style="cyan")
        table.add_column("Team", style="green")
        table.add_column("Matches", style="yellow")
        table.add_column("Maps", style="blue")
        table.add_column("Map Diff", style="magenta")
        
        for rank, team in enumerate(sorted_teams, 1):
            matches_record = f"{team.wins}-{team.losses}"
            maps_record = f"{team.maps_won}-{team.maps_lost}"
            map_diff = team.maps_won - team.maps_lost
            map_diff_str = f"{map_diff:+d}" if map_diff != 0 else "0"
            
            table.add_row(
                str(rank),
                team.name,
                matches_record,
                maps_record,
                map_diff_str
            )
        
        console.print(table)
        input("\nPress Enter to continue...")
    
    def _sort_standings(self, teams: list) -> list:
        """Sort teams by wins/losses, then by map differential.
        
        Args:
            teams: List of Team objects.
            
        Returns:
            Sorted list of teams.
        """
        return sorted(
            teams,
            key=lambda t: (
                -t.wins,  # Primary: Most wins (negative for descending)
                -(t.maps_won - t.maps_lost)  # Tiebreaker: Map differential (descending)
            )
        )


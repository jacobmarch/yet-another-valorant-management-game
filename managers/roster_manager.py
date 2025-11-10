"""Manager for displaying team rosters."""

from rich.table import Table
from core.console import console
from models.Team import Team


class RosterManager:
    """Handles team roster display."""
    
    def __init__(self, leagues: list):
        """Initialize the roster manager.
        
        Args:
            leagues: List of league dictionaries from JSON.
        """
        self.leagues = leagues
        self.teams_by_league = self._initialize_teams()
    
    def _initialize_teams(self) -> dict:
        """Initialize all teams with rosters.
        
        Returns:
            Dictionary mapping league names to lists of Team objects.
        """
        teams_by_league = {}
        for league in self.leagues:
            teams = []
            for team_data in league["teams"]:
                team = Team(name=team_data["name"])
                team.build_roster()
                teams.append(team)
            teams_by_league[league["name"]] = teams
        return teams_by_league
    
    def view_roster(self) -> None:
        """Display roster viewing interface with region and team selection."""
        console.print("\n[bold]View Roster[/bold]")
        
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
                    self._select_team_for_roster(selected_league_name)
                    return
                else:
                    console.print("[red]Invalid league number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def _select_team_for_roster(self, league_name: str) -> None:
        """Display teams from a league and let user select one to view roster.
        
        Args:
            league_name: Name of the selected league.
        """
        teams = self.teams_by_league[league_name]
        
        console.print(f"\n[bold]Select a Team from {league_name}[/bold]")
        
        table = Table(title=f"Teams in {league_name}")
        table.add_column("Number", style="cyan")
        table.add_column("Team Name", style="magenta")
        
        for idx, team in enumerate(teams, 1):
            table.add_row(str(idx), team.name)
        
        console.print(table)
        
        while True:
            try:
                choice = input("\nEnter team number (or 0 to go back): ").strip()
                team_idx = int(choice) - 1
                
                if choice == "0":
                    return
                
                if 0 <= team_idx < len(teams):
                    selected_team = teams[team_idx]
                    self._display_roster(selected_team)
                    return
                else:
                    console.print("[red]Invalid team number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def _display_roster(self, team: Team) -> None:
        """Display the roster for a specific team.
        
        Args:
            team: The Team object to display the roster for.
        """
        console.print()  # Add spacing
        table = Table(title=f"{team.name} Roster")
        table.add_column("Number", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Username", style="yellow")
        table.add_column("Role", style="blue")
        table.add_column("Rating", style="magenta")
        
        for idx, player in enumerate(team.players, 1):
            table.add_row(
                str(idx),
                f"{player.first_name} {player.last_name}",
                player.username,
                player.role.capitalize(),
                str(player.rating)
            )
        
        console.print(table)
        input("\nPress Enter to continue...")


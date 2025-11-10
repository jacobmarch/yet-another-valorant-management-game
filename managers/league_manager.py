"""Manager for league and team selection."""

import json
from rich.table import Table
from core.console import console
from models.Team import Team


class LeagueManager:
    """Handles loading and selecting leagues and teams."""
    
    def __init__(self, data_path: str = "data/leagues_and_teams.json"):
        """Initialize the league manager.
        
        Args:
            data_path: Path to the JSON file containing leagues and teams.
        """
        self.data_path = data_path
        self.leagues = self._load_leagues()
    
    def _load_leagues(self) -> list:
        """Load all leagues from the JSON file."""
        with open(self.data_path, "r") as f:
            data = json.load(f)
        return data["leagues"]
    
    def select_region(self) -> dict:
        """Display available regions and let user select one.
        
        Returns:
            The selected league dictionary.
        """
        console.print("\n[bold]Select a Region[/bold]")
        
        table = Table(title="Available Regions")
        table.add_column("Number", style="cyan")
        table.add_column("Region", style="magenta")
        
        for idx, league in enumerate(self.leagues, 1):
            table.add_row(str(idx), league["name"])
        
        console.print(table)
        
        while True:
            try:
                choice = input("\nEnter region number: ").strip()
                region_idx = int(choice) - 1
                if 0 <= region_idx < len(self.leagues):
                    selected_league = self.leagues[region_idx]
                    console.print(f"[green]You selected {selected_league['name']}![/green]")
                    return selected_league
                else:
                    console.print("[red]Invalid region number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def select_team_from_region(self, league: dict) -> Team:
        """Display teams from selected region and let user select one.
        
        Args:
            league: The selected league dictionary.
            
        Returns:
            The selected Team object with roster initialized.
        """
        console.print(f"\n[bold]Select a Team from {league['name']}[/bold]")
        
        table = Table(title=f"Teams in {league['name']}")
        table.add_column("Number", style="cyan")
        table.add_column("Team Name", style="magenta")
        
        teams = []
        for idx, team_data in enumerate(league["teams"], 1):
            team_model = Team(name=team_data["name"])
            team_model.build_roster()
            teams.append(team_model)
            table.add_row(str(idx), team_data["name"])
        
        console.print(table)
        
        while True:
            try:
                choice = input("\nEnter team number: ").strip()
                team_idx = int(choice) - 1
                if 0 <= team_idx < len(teams):
                    selected_team = teams[team_idx]
                    console.print(f"[green]You selected {selected_team.name}![/green]")
                    return selected_team
                else:
                    console.print("[red]Invalid team number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")


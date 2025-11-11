"""Manager for game loop and game state."""

from rich.table import Table
from core.console import console
from models.Team import Team
from .schedule_manager import ScheduleManager
from .roster_manager import RosterManager
from .match_manager import MatchManager


class GameManager:
    """Handles the main game loop and menu logic."""
    
    def __init__(self, user_team: Team, leagues: list):
        """Initialize the game manager.
        
        Args:
            user_team: The Team object the player is managing.
            leagues: List of all leagues (for schedule and roster access).
        """
        self.user_team = user_team
        self.leagues = leagues
        self.schedule_manager = ScheduleManager(leagues)
        self.roster_manager = RosterManager(leagues)
        self.match_manager = MatchManager()
        self.current_week = 0
    
    def run(self) -> None:
        """Run the main game loop."""
        console.print(f"\n[bold]Starting Game with {self.user_team.name}[/bold]")
        while True:
            self._display_menu()
            choice = input("> ").strip()
            
            if not self._handle_menu_choice(choice):
                break
    
    def _display_menu(self) -> None:
        """Display the main menu."""
        console.print("\n[bold]Main Menu[/bold]")
        console.print(f"[cyan]Team: {self.user_team.name}[/cyan]")
        console.print("[1] View Roster")
        console.print("[2] Advance to Match")
        console.print("[3] View Schedule")
        console.print("[4] View Standings")
        console.print("[0] Quit")
    
    def _handle_menu_choice(self, choice: str) -> bool:
        """Handle menu selection.
        
        Args:
            choice: The user's menu selection.
            
        Returns:
            False if the user wants to quit, True otherwise.
        """
        if choice == "0":
            console.print("[red]Goodbye![/red]")
            return False
        elif choice == "1":
            self.view_roster()
        elif choice == "2":
            self.advance_to_match()
        elif choice == "3":
            self.view_schedule()
        elif choice == "4":
            self.view_standings()
        else:
            console.print("[red]Invalid option![/red]")
        
        return True
    
    def view_roster(self) -> None:
        """Display team rosters with region and team selection."""
        self.roster_manager.view_roster()
    
    def advance_to_match(self) -> None:
        """Advance to the next week and simulate all matches."""
        if self.current_week >= 11:
            console.print("[red]Season is over![/red]")
            return
        
        console.print(f"\n[bold yellow]Simulating Week {self.current_week + 1}...[/bold yellow]\n")
        
        # Simulate all matches in all leagues
        all_results = {}
        for league in self.leagues:
            league_name = league["name"]
            all_results[league_name] = self._simulate_week(league_name)
        
        # Display results
        self._display_week_results(all_results)
        
        self.current_week += 1
    
    def _simulate_week(self, league_name: str) -> dict:
        """Simulate all matches for a week in a league.
        
        Args:
            league_name: Name of the league.
            
        Returns:
            Dictionary of match results for the week.
        """
        schedule = self.schedule_manager.schedules[league_name]
        teams_in_league = self.roster_manager.teams_by_league[league_name]
        
        # Create dict for easy team lookup
        teams_dict = {team.name: team for team in teams_in_league}
        
        week_matches = schedule[self.current_week]
        results = {}
        
        for team1_name, team2_name in week_matches:
            team1 = teams_dict[team1_name]
            team2 = teams_dict[team2_name]
            
            # Simulate the match
            match = self.match_manager.simulate_match(team1, team2, series_format=3)
            
            # Store result with series score
            match_key = f"{team1_name}_vs_{team2_name}"
            team1_wins, team2_wins = match.get_series_score()
            results[match_key] = (team1_name, team1_wins, team2_wins, team2_name)
        
        # Store in schedule manager
        self.schedule_manager.store_week_results(league_name, self.current_week, results)
        
        return results
    
    def _display_week_results(self, all_results: dict) -> None:
        """Display the results of all matches for the week.
        
        Args:
            all_results: Dictionary of results by league.
        """
        for league_name, results in all_results.items():
            table = Table(title=f"{league_name} - Week {self.current_week + 1} Results")
            table.add_column("Match", style="cyan")
            table.add_column("Result", style="green")
            
            for idx, (match_key, result) in enumerate(results.items(), 1):
                team1_name, team1_wins, team2_wins, team2_name = result
                result_str = f"{team1_name} {team1_wins} - {team2_wins} {team2_name}"
                table.add_row(str(idx), result_str)
            
            console.print(table)
            console.print()
    
    def view_schedule(self) -> None:
        """Display league schedules."""
        self.schedule_manager.view_schedule()
    
    def view_standings(self) -> None:
        """Display league standings."""
        console.print("[purple]Standings shown here...[/purple]")
        # TODO: Implement view_standings


"""Manager for generating and displaying league schedules."""

from rich.table import Table
from core.console import console
from models.Team import Team


class ScheduleManager:
    """Handles round-robin schedule generation and display."""
    
    def __init__(self, leagues: list):
        """Initialize the schedule manager.
        
        Args:
            leagues: List of league dictionaries from JSON.
        """
        self.leagues = leagues
        self.schedules = self._generate_all_schedules()
    
    def _generate_all_schedules(self) -> dict:
        """Generate round-robin schedules for all leagues.
        
        Returns:
            Dictionary mapping league names to their schedules.
        """
        schedules = {}
        for league in self.leagues:
            schedules[league["name"]] = self._generate_round_robin(league["teams"])
        return schedules
    
    def _generate_round_robin(self, teams_data: list) -> list:
        """Generate a round-robin schedule for a league.
        
        Uses the standard rotation algorithm to create a balanced schedule
        where each team plays every other team exactly once.
        
        Args:
            teams_data: List of team data dictionaries.
            
        Returns:
            List of weeks, where each week is a list of matchups (team_name tuples).
        """
        team_names = [team["name"] for team in teams_data]
        n = len(team_names)
        
        # Ensure even number of teams
        if n % 2 == 1:
            team_names.append("BYE")
            n += 1
        
        schedule = []
        
        # Generate n-1 rounds (weeks)
        for round_num in range(n - 1):
            week_matches = []
            
            for i in range(n // 2):
                # Calculate pairings using rotation algorithm
                if i == 0:
                    # First team vs last team (which rotates)
                    team1 = team_names[0]
                    team2 = team_names[n - 1]
                else:
                    # Other teams rotate around the circle
                    team1 = team_names[i]
                    team2 = team_names[n - 1 - i]
                
                if team1 != "BYE" and team2 != "BYE":
                    week_matches.append((team1, team2))
            
            # Rotate teams for next round (keeping first team fixed)
            if round_num < n - 2:
                team_names = (
                    [team_names[0]] + [team_names[-1]] + team_names[1:-1]
                )
            
            schedule.append(week_matches)
        
        return schedule
    
    def view_schedule(self) -> None:
        """Display schedule viewing interface."""
        console.print("\n[bold]View Schedule[/bold]")
        
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
                    selected_league = league_names[league_idx]
                    self._display_league_schedule(selected_league)
                    return
                else:
                    console.print("[red]Invalid league number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def _display_league_schedule(self, league_name: str) -> None:
        """Display the schedule for a specific league.
        
        Args:
            league_name: Name of the league to display.
        """
        schedule = self.schedules[league_name]
        
        console.print(f"\n[bold]{league_name} Schedule[/bold]")
        console.print(f"[cyan]Total Weeks: {len(schedule)}[/cyan]\n")
        
        while True:
            try:
                week_choice = input(
                    "Enter week number to view (1 to {}, or 0 to go back): ".format(
                        len(schedule)
                    )
                ).strip()
                
                if week_choice == "0":
                    return
                
                week_num = int(week_choice) - 1
                
                if 0 <= week_num < len(schedule):
                    self._display_week(league_name, week_num, schedule[week_num])
                else:
                    console.print(
                        f"[red]Please enter a number between 1 and {len(schedule)}.[/red]"
                    )
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def _display_week(self, league_name: str, week_num: int, matches: list) -> None:
        """Display all matches for a specific week.
        
        Args:
            league_name: Name of the league.
            week_num: Week number (0-indexed).
            matches: List of matchups for the week.
        """
        console.print()  # Add spacing
        table = Table(title=f"{league_name} - Week {week_num + 1}")
        table.add_column("Match", style="cyan")
        table.add_column("Home Team", style="green")
        table.add_column("Away Team", style="yellow")
        
        for match_num, (team1, team2) in enumerate(matches, 1):
            table.add_row(str(match_num), team1, team2)
        
        console.print(table)
        input("\nPress Enter to continue...")


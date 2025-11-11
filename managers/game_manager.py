"""Manager for game loop and game state."""

from rich.table import Table
from core.console import console
from models.Team import Team
from .schedule_manager import ScheduleManager
from .roster_manager import RosterManager
from .match_manager import MatchManager
from .standings_manager import StandingsManager


class GameManager:
    """Handles the main game loop and menu logic."""
    
    def __init__(self, user_team: Team, leagues: list):
        """Initialize the game manager.
        
        Args:
            user_team: The Team object the player is managing.
            leagues: List of all leagues (for schedule and roster access).
        """
        self.leagues = leagues
        self.schedule_manager = ScheduleManager(leagues)
        self.roster_manager = RosterManager(leagues)
        self.match_manager = MatchManager()
        self.standings_manager = StandingsManager(leagues, self.roster_manager)
        
        # Find the actual user team in the roster manager to ensure we reference the same object
        self.user_team = None
        for teams in self.roster_manager.teams_by_league.values():
            for team in teams:
                if team.name == user_team.name:
                    self.user_team = team
                    break
            if self.user_team:
                break
        
        # Fallback (shouldn't happen)
        if self.user_team is None:
            self.user_team = user_team
        
        self.current_week = 0
        self.current_season = 1
        self.season_history = {}  # Track records from completed seasons
    
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
        console.print(f"[yellow]Season {self.current_season} - Week {self.current_week + 1}/11[/yellow]")
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
            self._handle_season_end()
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
            
            # Track maps won/lost
            team1.add_map_win(team1_wins)
            team1.add_map_loss(team2_wins)
            team2.add_map_win(team2_wins)
            team2.add_map_loss(team1_wins)
        
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
        self.standings_manager.view_standings()
    
    def _handle_season_end(self) -> None:
        """Handle the end of season - show summary and offer to continue."""
        console.print("\n[bold cyan]SEASON {} COMPLETE![/bold cyan]\n".format(self.current_season))
        
        # Display final standings for user's league
        user_league = self._find_user_league()
        if user_league:
            self._display_season_summary(user_league)
        
        # Ask if user wants to continue
        while True:
            choice = input("\nContinue to next season? (y/n): ").strip().lower()
            if choice == "y":
                self._advance_to_next_season()
                return
            elif choice == "n":
                console.print("[yellow]Season ended. Returning to main menu...[/yellow]")
                return
            else:
                console.print("[red]Please enter 'y' or 'n'.[/red]")
    
    def _find_user_league(self) -> dict:
        """Find the league that contains the user's team.
        
        Returns:
            League dictionary or None if not found.
        """
        for league in self.leagues:
            for team_data in league["teams"]:
                if team_data["name"] == self.user_team.name:
                    return league
        return None
    
    def _display_season_summary(self, league: dict) -> None:
        """Display season summary for user's league.
        
        Args:
            league: The league dictionary containing the user's team.
        """
        console.print(f"\n[bold]{league['name']} - Final Standings[/bold]\n")
        
        teams = self.roster_manager.teams_by_league[league["name"]]
        sorted_teams = self.standings_manager._sort_standings(teams)
        
        # Show user's team rank and top 5
        user_rank = next((i + 1 for i, t in enumerate(sorted_teams) if t.name == self.user_team.name), None)
        
        table = Table(title="Top 5 Teams")
        table.add_column("Rank", style="cyan")
        table.add_column("Team", style="green")
        table.add_column("Record", style="yellow")
        table.add_column("Maps", style="blue")
        
        for idx, team in enumerate(sorted_teams[:5], 1):
            matches_record = f"{team.wins}-{team.losses}"
            maps_record = f"{team.maps_won}-{team.maps_lost}"
            table.add_row(str(idx), team.name, matches_record, maps_record)
        
        console.print(table)
        
        if user_rank:
            console.print(f"\n[cyan]Your team ({self.user_team.name}) finished: [bold]#{user_rank}[/bold][/cyan]")
    
    def _advance_to_next_season(self) -> None:
        """Advance to the next season."""
        console.print(f"\n[bold yellow]Advancing to Season {self.current_season + 1}...[/bold yellow]\n")
        
        # Save current season record to history
        user_league = self._find_user_league()
        if user_league:
            teams = self.roster_manager.teams_by_league[user_league["name"]]
            user_team_data = next((t for t in teams if t.name == self.user_team.name), None)
            if user_team_data:
                self.season_history[self.current_season] = {
                    "wins": user_team_data.wins,
                    "losses": user_team_data.losses,
                    "maps_won": user_team_data.maps_won,
                    "maps_lost": user_team_data.maps_lost,
                    "rank": self._get_user_team_rank(user_league)
                }
        
        # Display player rating changes before and after
        self._display_player_rating_changes()
        
        # Update player ratings
        self._update_all_player_ratings()
        
        # Reset all team records
        for teams in self.roster_manager.teams_by_league.values():
            for team in teams:
                team.reset_record()
        
        # Regenerate schedule
        self.schedule_manager = ScheduleManager(self.leagues)
        
        # Increment season and reset week
        self.current_season += 1
        self.current_week = 0
        
        # Display season history
        self._display_season_history()
        
        console.print(f"\n[green]Welcome to Season {self.current_season}![/green]")
        console.print("[yellow]New schedules have been generated.[/yellow]\n")
        
        input("Press Enter to continue...")
    
    def _get_user_team_rank(self, league: dict) -> int:
        """Get the user team's rank in their league.
        
        Args:
            league: The league dictionary.
            
        Returns:
            Rank number (1-12).
        """
        teams = self.roster_manager.teams_by_league[league["name"]]
        sorted_teams = self.standings_manager._sort_standings(teams)
        for rank, team in enumerate(sorted_teams, 1):
            if team.name == self.user_team.name:
                return rank
        return 12  # Default to last if not found
    
    def _display_player_rating_changes(self) -> None:
        """Display player rating changes before and after season update."""
        console.print("[bold]Player Rating Changes:[/bold]\n")
        
        table = Table(title=f"{self.user_team.name} - Offseason Updates")
        table.add_column("Player", style="cyan")
        table.add_column("Role", style="yellow")
        table.add_column("Old Rating", style="red")
        table.add_column("New Rating", style="green")
        table.add_column("Change", style="magenta")
        
        # Store old ratings
        old_ratings = [(p.first_name, p.last_name, p.role, p.rating) for p in self.user_team.players]
        
        # Update ratings
        self._update_all_player_ratings()
        
        # Display changes
        for idx, player in enumerate(self.user_team.players):
            old_first, old_last, role, old_rating = old_ratings[idx]
            new_rating = player.rating
            change = new_rating - old_rating
            change_str = f"{change:+d}" if change != 0 else "0"
            change_color = "green" if change > 0 else "red" if change < 0 else "yellow"
            
            table.add_row(
                f"{player.first_name} {player.last_name}",
                role.capitalize(),
                str(old_rating),
                str(new_rating),
                f"[{change_color}]{change_str}[/{change_color}]"
            )
        
        console.print(table)
        input("\nPress Enter to continue...")
    
    def _display_season_history(self) -> None:
        """Display the user team's season history."""
        if not self.season_history:
            return
        
        console.print("\n[bold]Season History[/bold]\n")
        
        table = Table(title=f"{self.user_team.name} - Career Record")
        table.add_column("Season", style="cyan")
        table.add_column("Record", style="yellow")
        table.add_column("Maps", style="blue")
        table.add_column("Rank", style="green")
        
        total_wins = 0
        total_losses = 0
        total_maps_won = 0
        total_maps_lost = 0
        
        for season in sorted(self.season_history.keys()):
            record = self.season_history[season]
            wins = record["wins"]
            losses = record["losses"]
            maps_won = record["maps_won"]
            maps_lost = record["maps_lost"]
            rank = record["rank"]
            
            total_wins += wins
            total_losses += losses
            total_maps_won += maps_won
            total_maps_lost += maps_lost
            
            table.add_row(
                str(season),
                f"{wins}-{losses}",
                f"{maps_won}-{maps_lost}",
                f"#{rank}"
            )
        
        # Add career totals
        table.add_row(
            "[bold]Total[/bold]",
            f"[bold]{total_wins}-{total_losses}[/bold]",
            f"[bold]{total_maps_won}-{total_maps_lost}[/bold]",
            ""
        )
        
        console.print(table)
        input("\nPress Enter to continue...")
    
    def _update_all_player_ratings(self) -> None:
        """Update all player ratings randomly (change by 0-5 points)."""
        import random
        
        for teams in self.roster_manager.teams_by_league.values():
            for team in teams:
                for player in team.players:
                    # Random change from -5 to +5
                    change = random.randint(-5, 5)
                    new_rating = max(1, min(100, player.rating + change))  # Clamp between 1-100
                    player.rating = new_rating


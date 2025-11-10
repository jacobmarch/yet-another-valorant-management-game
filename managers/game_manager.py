"""Manager for game loop and game state."""

from core.console import console
from models.Team import Team
from .schedule_manager import ScheduleManager


class GameManager:
    """Handles the main game loop and menu logic."""
    
    def __init__(self, user_team: Team, leagues: list):
        """Initialize the game manager.
        
        Args:
            user_team: The Team object the player is managing.
            leagues: List of all leagues (for schedule access).
        """
        self.user_team = user_team
        self.schedule_manager = ScheduleManager(leagues)
    
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
        """Display the team roster."""
        console.print("[green]Current Roster:[/green]")
        # TODO: Implement view_roster
    
    def advance_to_match(self) -> None:
        """Advance to the next match."""
        console.print("[yellow]Advancing to match...[/yellow]")
        # TODO: Implement advance_to_match
    
    def view_schedule(self) -> None:
        """Display league schedules."""
        self.schedule_manager.view_schedule()
    
    def view_standings(self) -> None:
        """Display league standings."""
        console.print("[purple]Standings shown here...[/purple]")
        # TODO: Implement view_standings


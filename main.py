"""Main entry point for Valorant Manager Game."""

from core.console import console
from managers import LeagueManager, GameManager


def main_menu() -> bool:
    """Display main menu and handle user choice.
    
    Returns:
        False if user wants to quit, True if they want to start a game.
    """
    console.print("\n[bold]Starting Menu[/bold]")
    console.print("[1] Start Game")
    console.print("[2] Quit")
    
    choice = input("> ").strip()
    if choice == "1":
        return True
    elif choice == "2":
        console.print("[red]Goodbye![/red]")
        return False
    else:
        console.print("[red]Invalid option![/red]")
        return main_menu()


def start_game() -> None:
    """Initialize and start a new game."""
    console.print("[green]Game starting...[/green]")
    console.print("[bold]Initializing Game...[/bold]")
    
    # Select region and team
    league_manager = LeagueManager()
    selected_league = league_manager.select_region()
    user_team = league_manager.select_team_from_region(selected_league)
    
    # Run the game
    game_manager = GameManager(user_team)
    game_manager.run()


def main() -> None:
    """Main entry point."""
    console.print("[bold cyan]Valorant Manager Game[/bold cyan]")
    
    while True:
        if main_menu():
            start_game()
        else:
            break


if __name__ == "__main__":
    main()

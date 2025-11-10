from rich.console import Console
from models.Team import Team

console = Console()

def game_loop():
    console.print("[bold]Starting Game[/bold]")
    initialize_game() # TODO: Implement initialize_game
    while True:
        console.print("\n[bold]Main Menu[/bold]")
        console.print("[1] View Roster")
        console.print("[2] Advance to Match")
        console.print("[3] View Match History")
        console.print("[4] View Standings")
        console.print("[0] Quit")

        choice = input("> ").strip()
        if choice == "0":
            console.print("[red]Goodbye![/red]")
            break
        elif choice == "1":
            console.print("[green]Current Roster:[/green]")
            view_roster() # TODO: Implement view_roster
        elif choice == "2":
            console.print("[yellow]Advancing to match...[/yellow]")
            advance_to_match() # TODO: Implement advance_to_match
        elif choice == "3":
            console.print("[blue]Match history shown here...[/blue]")
            view_match_history() # TODO: Implement view_match_history
        elif choice == "4":
            console.print("[purple]Standings shown here...[/purple]")
            view_standings() # TODO: Implement view_standings
        else:
            console.print("[red]Invalid option![/red]")

    def initialize_game():
        # TODO: Implement initialize_game
        # Create a new game instance
        # This needs to set up four leagues, each with 12 teams. They can be loaded from the JSON file titled leagues_and_teams.json in the data folder.
        from data.leagues_and_teams import leagues_and_teams
        teams: list[Team] = []
        for league in leagues_and_teams:
            for team in league["teams"]:
                team_model = Team(name=team["name"])
                team_model.build_roster()
                teams.append(team_model)

def main():
    console.print("[bold cyan]Valorant Manager Game[/bold cyan]")
    while True:
        console.print("\n[bold]Starting Menu[/bold]")
        console.print("[1] Start Game")
        console.print("[2] Quit")

        choice = input("> ").strip()
        if choice == "1":
            console.print("[green]Game started[/green]")
            game_loop() # TODO: Implement game loop
        elif choice == "2":
            console.print("[red]Goodbye![/red]")
            break


if __name__ == "__main__":
    main()
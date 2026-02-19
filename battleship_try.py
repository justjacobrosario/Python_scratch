
# pyright: strict

from __future__ import annotations

from typing import Protocol
from collections.abc import Sequence
from utils import generate_grid
from random import Random
from enum import Enum
import os
os.system("")

class PlayerType(Enum):
    HUMAN = 0
    BOT = 1

class TurnAction(Enum):
    SHOOT = 0
    MOVE = 1
    SCAN = 2

class Player(Protocol):
    total_players: int
    n: int
    ship_sizes: Sequence[int]
    rng: Random
    player_type: PlayerType
    player_grid: list[list[str]]
    shot_coords: dict[int, list[tuple[int, int]]] | None
    move_ship_chances: int | None
    scan_chances: int | None
    player_dead: bool
        


class HumanPlayer:
    def __init__(self,
        total_players: int = 2,
        n: int = 6,
        ship_sizes: Sequence[int] = (4, 3, 2, 2),
        rng: Random = Random(),
        player_type: PlayerType = PlayerType.HUMAN,
        player_grid: list[list[str]] | None = None,
        shot_coords: dict[int, list[tuple[int, int]]] | None = dict(),
        move_ship_chances: int | None = None,
        scan_chances: int | None = None,
        player_dead: bool = True,
        ):
        self.total_players = total_players
        self.n = n
        self.ship_sizes = ship_sizes
        self.rng = rng
        self.player_type = player_type
        self.player_grid = generate_grid(self.n, self.ship_sizes, self.rng)
        self.shot_coords = shot_coords
        for p in range(self.total_players):
            self.shot_coords.update({p:[]})
        self.move_ship_chances = move_ship_chances
        self.scan_chances = scan_chances
        self.player_dead = player_dead

class BotPlayer:
    def __init__(self,
        total_players: int = 2,
        n: int = 6,
        ship_sizes: Sequence[int] = (4, 3, 2, 2),
        rng: Random = Random(),
        player_type: PlayerType = PlayerType.HUMAN,
        player_grid: list[list[str]] | None = None,
        shot_coords: dict[int, list[tuple[int, int]]] | None = dict(),
        move_ship_chances: int | None = None,
        scan_chances: int | None = None,
        player_dead: bool = True,
        ):
        self.total_players = total_players
        self.n = n
        self.ship_sizes = ship_sizes
        self.rng = rng
        self.player_type = player_type
        self.player_grid = generate_grid(self.n, self.ship_sizes, self.rng)
        self.shot_coords = shot_coords
        for p in range(self.total_players):
            self.shot_coords.update({p:[]})
        self.move_ship_chances = move_ship_chances
        self.scan_chances = scan_chances
        self.player_dead = player_dead
        


class BattleshipModel:
    def __init__(self,
        n: int = 6,
        k: int = 2,
        ship_sizes: Sequence[int] = (4,3,2,2),
        rng: Random = Random(),
        turn: int = 0,
        players: int = 2,
        player_list: list[Player] = [],
        max_powerup_uses: int = 3):
        # constant attributes
        self.n = n
        self.k = k
        self.ship_sizes = ship_sizes
        self.rng = rng
        self.turn = turn
        self.players = players
        # MODIFIED COMBINED PLAYER GRIDS
        self.player_list = player_list
        # max powerups
        self.max_powerup_uses = max_powerup_uses

    def is_game_over(self) -> bool:
        grids = [player.player_grid for player in self.player_list]
        

        for idx, grid in enumerate(grids):
            still_living: bool = False
            for r in range(len(grid)):
                if still_living:
                    break
                for c in range(len(grid[0])):
                    if grid[r][c].isupper():
                        self.player_list[idx].player_dead = False
                        still_living = True
                        break

        return [player.player_dead for player in self.player_list].count(False) <= 1


    def grids(self) -> list[list[str]]:
        # return grids
        # ['A', '.', '.'] to "A . ."
        def strnger(_grid: list[list[str]]) -> list[str]:
            ans: list[str] = []
            for row in _grid:
                ans.append("".join(row))
            return ans

        res: list[list[str]] = []
        for p in range(self.players):
            res.append(strnger(self.player_list[p].player_grid))
        return res

    # NEED TO UPDATE
    def winner(self) -> int:
        # Edge: if winner is called but game is not over
        if not self.is_game_over():
            raise AssertionError("Game is not yet over")

        if self.players == 2:
            g0_alive = False
            g1_alive = False

            for r in range(len(self.grid_0)):
                for c in range(len(self.grid_0[0])):
                    if self.grid_0[r][c].isupper():
                        g0_alive = True
                    if self.grid_1[r][c].isupper():
                        g1_alive = True

            if g0_alive and not g1_alive:
                return 0
            if g1_alive and not g0_alive:
                return 1
            # both dead at same time
            return -1

        elif self.players == 3:
            g0_alive = False
            g1_alive = False
            g2_alive = False

            for r in range(len(self.grid_0)):
                for c in range(len(self.grid_0[0])):
                    if self.grid_0[r][c].isupper():
                        g0_alive = True
                    if self.grid_1[r][c].isupper():
                        g1_alive = True
                    if self.grid_2[r][c].isupper():
                        g2_alive = True

            if g0_alive and not g1_alive and not g2_alive:
                return 0
            if g1_alive and not g0_alive and not g2_alive:
                return 1
            if g2_alive and not g0_alive and not g1_alive:
                return 2
            return -1
        else:
            # edge: all lost
            return -1

    def go_to_next_turn(self) -> None:
        # collect living players manually
        living_players: list[int] = []
        for p in range(self.players):
            if self.players_dead[p] == False:
                living_players.append(p)

        # if no one is alive, do nothing
        if len(living_players) == 0:
            return

        # if current player is dead, move to first living player
        is_turn_alive = False
        for p in living_players:
            if p == self.turn:
                is_turn_alive = True

        if not is_turn_alive:
            self.turn = living_players[0]
            return

        # find current index manually
        current_index = 0
        for i in range(len(living_players)):
            if living_players[i] == self.turn:
                current_index = i

        # go to next player (circular)
        if current_index + 1 == len(living_players):
            self.turn = living_players[0]
        else:
            self.turn = living_players[current_index + 1]


    def get_random_ij(self) -> tuple[int, int]:
        # return random (i, j) as the bot's moves
        return (self.rng.randint(0, self.n - 1), self.rng.randint(0, self.n - 1))

    def get_random_target(self) -> int:
        valid_targets: list[int] = []
        for t in range(self.players):
            if t != self.turn:
                valid_targets.append(t)
        return self.rng.choice(valid_targets)

    def get_random_ship_move(self) -> tuple[str, str]:
        current_grid: list[list[str]] = [self.grid_0, self.grid_1, self.grid_2][self.turn]
        present_ships: set[str] = set()
        
        # check all living ships
        for row in current_grid:
            for char in row:
                if char.isupper():
                    present_ships.add(char)

        # edge: if all ships are dead
        if not present_ships:
            return ("", "")

        def is_move_valid(current_grid: list[list[str]], target_ship: str, move: str) -> bool:
            row_coords: list[int] = []
            col_coords: list[int] = []

            # collect ship coordinates
            for r in range(len(current_grid)):
                for c in range(len(current_grid[0])):
                    if current_grid[r][c] == target_ship:
                        row_coords.append(r)
                        col_coords.append(c)

            # ship not found or too small
            if len(row_coords) < 2:
                return False

            row_coords.sort()
            col_coords.sort()

            # vertical ship
            if col_coords[0] == col_coords[1]:
                col = col_coords[0]
                top = row_coords[0]
                bottom = row_coords[-1]

                if move.lower() == "u" and top > 0:
                    return current_grid[top - 1][col] == "."
                if move.lower() == "d" and bottom < len(current_grid) - 1:
                    return current_grid[bottom + 1][col] == "."

            # horizontal ship
            if row_coords[0] == row_coords[1]:
                row = row_coords[0]
                left = col_coords[0]
                right = col_coords[-1]

                if move.lower() == "l" and left > 0:
                    return current_grid[row][left - 1] == "."
                if move.lower() == "r" and right < len(current_grid) - 1:
                    return current_grid[row][right + 1] == "."

            return False

        # randomly generate input
        target_ship: str = ""
        movement: str = ""

        for _ in range(1000): # for loop instead while loop to prevent infinite  looping
            target_ship = self.rng.choice(list(present_ships))
            movement = self.rng.choice(['u', 'd', 'l', 'r'])
            if is_move_valid(current_grid, target_ship, movement):
                return target_ship, movement

        # fallback if no move is possible
        return ("", "")

    def shoot(self, i: int, j: int, target: int | None = None) -> None:
        # setup the target grid and saved shots for each player
        if target is None:
            target = 1 - self.turn # for edge cases

        # target grids
        target_grid_dic = {0:self.grid_0, 1:self.grid_1, 2:self.grid_2}
        target_grid = target_grid_dic[target]
        player_saved_shots_dic = {0:self.player0_shots, 1:self.player1_shots, 2:self.player2_shots}

        self.shot_grids[target].append((i, j))
        player_saved_shots_dic[self.turn][target].append((i, j))

        if target_grid[i][j].isupper():
            shot_char = target_grid[i][j]
            for r in range(len(target_grid)):
                for c in range(len(target_grid[0])):
                    if target_grid[r][c] == shot_char:
                        target_grid[r][c] = shot_char.lower()

    def scan(self, i: int, j:int, target:int) -> None:
        if self.scan_chances[self.turn] > 0:
            self.scan_chances[self.turn] -= 1
            # setup the target grid and saved shots for each player
            target_grid_dic = {0:self.grid_0, 1:self.grid_1, 2:self.grid_2}
            target_grid = target_grid_dic[target]
            player_saved_shots_dic = {0:self.player0_shots, 1:self.player1_shots, 2:self.player2_shots}

            for r in range(len(target_grid)):
                for c in range(len(target_grid[0])):
                    if i <= r <= i + self.k - 1 and j <= c <= j + self.k - 1:
                        player_saved_shots_dic[self.turn][target].append((r, c))
        
    def move_ship(self, ship_movement_pair: tuple[str, str]) -> None:
        if self.move_ship_chances[self.turn] > 0:
            self.move_ship_chances[self.turn] -= 1
            target_ship, movement = ship_movement_pair
            current_grid = [self.grid_0, self.grid_1, self.grid_2][self.turn]

            n = len(current_grid)
            updated_grid = [['.' for _ in range(n)] for _ in range(n)]

            # copy everything exceptt the moving ship
            for r in range(n):
                for c in range(n):
                    if current_grid[r][c] != target_ship:
                        updated_grid[r][c] = current_grid[r][c]

            # move the ship
            for r in range(n):
                for c in range(n):
                    if current_grid[r][c] == target_ship:
                        if movement == 'u':
                            updated_grid[r-1][c] = target_ship
                        elif movement == 'd':
                            updated_grid[r+1][c] = target_ship
                        elif movement == 'l':
                            updated_grid[r][c-1] = target_ship
                        elif movement == 'r':
                            updated_grid[r][c+1] = target_ship

            # save grid back
            if self.turn == 0:
                self.grid_0 = updated_grid
            elif self.turn == 1:
                self.grid_1 = updated_grid
            else:
                self.grid_2 = updated_grid

    def get_random_action(self) -> str:
        choices: list[str] = ['a', 'b', 'c']
        valid: list[str] = ["a"]
        if self.move_ship_chances[self.turn] > 0:
            valid.append("b")
        if self.scan_chances[self.turn] > 0:
            valid.append("c")
        return self.rng.choice(valid)

class BattleshipView:

    def ask_what_action(self, player_type: PlayerType, turn: int ) -> str:
        ans = ""
        while ans not in ["a", "b", "c"]:
            try:
                ans = str(input("▶️ Pick action (Shoot [a] | Move [b] | Scan [c]): ")).lower()
                if ans not in ['a', 'b', 'c']:
                    print('Input a valid action')
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Input a valid action")
        print()
        options_dic: dict[str, str] = {'a':'shoot a ship', 'b':'move a ship', 'c':'scan a grid'}
        print(f"Player {turn} chose to {options_dic[ans]}")
        return ans



    def ask_what_to_move(self, player_type: PlayerType, turn: int, grids: Sequence[list[list[str]]]) -> tuple[str, str]:
        current_grid: list[list[str]] = grids[turn]
        present_ships: set[str] = set()
        
        # check all living ships
        for row in current_grid:
            for char in row:
                if char.isupper():
                    present_ships.add(char)
        

        def is_move_valid(current_grid: list[list[str]], target_ship: str, move: str) -> bool:
            row_coords: list[int] = []
            col_coords: list[int] = []

            # collect ship coordinates
            for r in range(len(current_grid)):
                for c in range(len(current_grid[0])):
                    if current_grid[r][c] == target_ship:
                        row_coords.append(r)
                        col_coords.append(c)

            # ship not found or too small
            if len(row_coords) < 2:
                return False

            row_coords.sort()
            col_coords.sort()

            # vertical ship
            if col_coords[0] == col_coords[1]:
                col = col_coords[0]
                top = row_coords[0]
                bottom = row_coords[-1]

                if move.lower() == "u" and top > 0:
                    return current_grid[top - 1][col] == "."
                if move.lower() == "d" and bottom < len(current_grid) - 1:
                    return current_grid[bottom + 1][col] == "."

            # horizontal ship
            if row_coords[0] == row_coords[1]:
                row = row_coords[0]
                left = col_coords[0]
                right = col_coords[-1]

                if move.lower() == "l" and left > 0:
                    return current_grid[row][left - 1] == "."
                if move.lower() == "r" and right < len(current_grid) - 1:
                    return current_grid[row][right + 1] == "."

            return False

                            
        # ask valid input
        target_ship: str = ""
        movement: str = ""
        while not target_ship in present_ships or not is_move_valid(current_grid, target_ship, movement):
            try:
                target_ship = str(input(f"▶️ Which functioning ship do u want to move: ")).upper()
                movement = str(input(f"▶️ How to move [u/d for vertical ships][l/r for horizontal ships]: "))
                if target_ship not in present_ships:
                    print(f"Please input one of your valid ships [{present_ships}]")
                if not is_move_valid(current_grid, target_ship, movement):
                    print(f"Please input a valid move [u, l, d, r]")
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print(f"Please input one of your valid ships [{present_ships}]")
        return (target_ship, movement)


    def show_grids(self, grids: Sequence[Sequence[str]], turn: int, saved_grids: Sequence[dict[int, list[tuple[int,int]]]], n: int) -> None:
        for l in range(n):
            line: str = ""
            for g in range(len(grids)):
                for c in range(len(grids[g][l])):
                    reveal = False
                    if g == turn:
                        reveal = True
                    else:
                        # check if the current cell was scanned by the current player
                        if g in saved_grids[turn] and (l, c) in saved_grids[turn][g]:
                            reveal = True

                    if reveal:
                        if grids[g][l][c] == ".":
                            line += f'\033[34m{grids[g][l][c]}\033[0m'
                        else:
                            line += f'\033[33m{grids[g][l][c]}\033[0m'
                    else:
                        line += "?"
                line += "  " # separator
            print(line)
        print()

    def show_final_grids(self, grids: Sequence[Sequence[str]], turn: int, saved_grids: Sequence[dict[int, list[tuple[int,int]]]], n: int) -> None:
        for l in range(n):
            line: str = ""
            for g in range(len(grids)):
                for c in range(len(grids[g][l])):
                    if grids[g][l][c] == ".":
                        line += f'\033[34m{grids[g][l][c]}\033[0m'
                    else:
                        line += f'\033[33m{grids[g][l][c]}\033[0m'
                line += "  " # separator
            print(line)
        print()


    def ask_for_location(self, n: int) -> tuple[int, int]:
        i, j = -1, -1

        while not 0 <= i < n:
            try:
                i = int(input(f"▶️ Choose a row    [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...

        while not 0 <= j < n:
            try:
                j = int(input(f"▶️ Choose a column [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...

        print()
        return i, j

    def ask_for_top_left_scan_point(self, n: int) -> tuple[int, int]:
        i, j = -1, -1

        while not 0 <= i < n:
            try:
                i = int(input(f"▶️ Choose a row of top-leftmost cell to scan [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...

        while not 0 <= j < n:
            try:
                j = int(input(f"▶️ Choose a column of top-leftmost cell to scan [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...

        print()
        return i, j

    def ask_num_players(self) -> int:
        player_count = -1
        while not 2 <= player_count <= 3:
            try:
                player_count = int(input(f"▶️ How many players will be playing this match [2-3 players]: "))
                
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...
        print()
        return player_count

    def ask_who_to_shoot(self, players: int, turn: int) -> int:
        target = -1
        
        while target not in (0, 1, 2) or turn == target:
            try:
                print(f'You are player {turn}')
                target = int(input(f"▶️ What Player No. should you shoot [0 / 1 / 2]: "))
                if target == turn:
                    print("You can't damage yourself!! (Chill!)")
                if target not in (0, 1, 2):
                    print("Please enter a valid player number.")
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please enter a valid player number.")
        print()
        return target

    def ask_who_to_scan(self, players: int, turn: int) -> int:
        target = -1
        
        while target not in (0, 1, 2) or turn == target:
            try:
                print(f'You are player {turn}')
                target = int(input(f"▶️ What Player No. should you scan [0 / 1 / 2]: "))
                if target == turn:
                    print("You can't scan yourself!! (Chill!)")
                if target not in (0, 1, 2):
                    print("Please enter a valid player number.")
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please enter a valid player number.")
        print()
        return target

    def is_human_or_bot(self, player_num: int) -> PlayerType:
        player_type: str = 'ee'
        while not player_type in {'h', 'b'}:
            try:
                player_type = str(input(f"▶️ Is Player {player_num} a Human or a Bot [h / b]: ")).lower()
            except KeyboardInterrupt:
                exit()
            except Exception:
                ...
        print()
        return PlayerType.HUMAN if player_type == 'h' else PlayerType.BOT

    def whos_turn_is_it(self, turn: int, move_ship_chances: Sequence[int], scan_chances:Sequence[int]) -> None:
        print(f"It's Player {turn}'s turn. {move_ship_chances[turn]} move ship chances left & {scan_chances[turn]} scan chances left.")
        print()

    def show_shot(self, i: int, j: int, turn: int) -> None:
        print(f"({i},{j}) was shot by Player {turn}!")
        print()

    def show_end_message(self, winner: int) -> None:
        if winner == -1:
            print("It's a draw! No one wins.")
        elif winner == 0:
            print("You win!")
        else:
            print(f"Player {winner} wins!")
        print()

    def ask_n_size(self) -> int:
        n: int = -1
        while n < 1:
            try:
                n = int(input(f"▶️ Set n size of the grids' sides: "))
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please input a valid value")
        return n

    def ask_k_size(self) -> int:
        k: int = -1
        while k < 1:
            try:
                k = int(input(f"▶️ Set k size of the scan area (k x k sides wide): "))
            except KeyboardInterrupt:
                exit()
            except ValueError:
                print("Please input a valid value")
        return k

class BattleshipController:
    def __init__(self, model: BattleshipModel, view: BattleshipView):
        self._model = model
        self._view = view

    def run(self) -> None:
        model = self._model
        view = self._view

        # Setup: Set n size of grid, and k size of scans
        model.n = view.ask_n_size()
        model.k = view.ask_k_size()

        model.grid_0 = generate_grid(model.n, model.ship_sizes, model.rng)
        model.grid_1 = generate_grid(model.n, model.ship_sizes, model.rng)
        model.grid_2 = generate_grid(model.n, model.ship_sizes, model.rng)

        # Setup: Set no. of players, and if humans or bots
        # initialize for pyright
        player_1: PlayerType = PlayerType.BOT
        player_2: PlayerType = PlayerType.BOT
        i: int = 0
        j: int = 0
        target: int = 1
        decision: str = 'a'
        target_ship: str = ""
        movement: str = ""

        model.players = view.ask_num_players()
        # MODIFIED PLAYER GRIDS
        for _ in range(model.players):
            model.player_grids.append(generate_grid(model.n, model.ship_sizes, model.rng))

        model.move_ship_chances = [model.max_powerup_uses] * model.players
        model.scan_chances = [model.max_powerup_uses] * model.players
        model.players_dead = [False] * model.players

        player_0 = PlayerType.HUMAN
        if model.players == 2:
            player_1 = view.is_human_or_bot(1)
        elif model.players == 3:
            player_1 = view.is_human_or_bot(1)
            player_2 = view.is_human_or_bot(2)


        # Game loop
        while not model.is_game_over():
            view.whos_turn_is_it(model.turn, model.move_ship_chances, model.scan_chances)
            # [2 players mode]
            if model.players == 2:
                # Player 0
                if model.turn == 0:
                    view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)
                    target = 1
                    # decide action
                    decision = view.ask_what_action(PlayerType.HUMAN, model.turn)
                    if decision == 'a':
                        i, j = view.ask_for_location(model.n)
                    elif decision == 'b':
                        target_ship, movement = view.ask_what_to_move(PlayerType.HUMAN, model.turn, [model.grid_0, model.grid_1, model.grid_2])
                        model.move_ship((target_ship, movement))
                    elif decision == 'c':
                        i, j = view.ask_for_top_left_scan_point(model.n)
                        model.scan(i, j, target)
                # Player 1
                else:
                    # Human P1
                    if player_1 == PlayerType.HUMAN:
                        view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)
                        target = 0
                        # decide action
                        decision = view.ask_what_action(PlayerType.HUMAN, model.turn)
                        if decision == 'a':
                            i, j = view.ask_for_location(model.n)
                        elif decision == 'b':
                            target_ship, movement = view.ask_what_to_move(PlayerType.HUMAN, model.turn, [model.grid_0, model.grid_1, model.grid_2])
                            model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            i, j = view.ask_for_top_left_scan_point(model.n)
                            model.scan(i, j, target)
                    # Bot P1
                    else:
                        # decide action
                        decision = view.ask_what_action(PlayerType.BOT, model.turn)
                        if decision == 'a':
                            target = 0
                            i, j = model.get_random_ij()
                            view.show_shot(i, j, model.turn)
                        elif decision == 'b':
                            target_ship, movement = model.get_random_ship_move()
                            if target_ship and movement:
                                model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            target = model.get_random_target()
                            i, j = model.get_random_ij()
                            model.scan(i, j, target)

            # [3 players mode]
            else:
                # Player 0
                if model.turn == 0:
                    view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)

                    # decide action

                    decision = view.ask_what_action(PlayerType.HUMAN, model.turn)
                    if decision == 'a':
                        target = view.ask_who_to_shoot(model.players, model.turn)
                        i, j = view.ask_for_location(model.n)
                    elif decision == 'b':
                        target_ship, movement = view.ask_what_to_move(PlayerType.HUMAN, model.turn, [model.grid_0, model.grid_1, model.grid_2])
                        model.move_ship((target_ship, movement))
                    elif decision == 'c':
                        target = view.ask_who_to_scan(model.players, model.turn)
                        i, j = view.ask_for_top_left_scan_point(model.n)
                        model.scan(i, j, target)
                # PLayer 1
                elif model.turn == 1:
                    # Human P1
                    if player_1 == PlayerType.HUMAN:
                        view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)
                        
                        # decide action
                        decision = view.ask_what_action(PlayerType.HUMAN, model.turn)
                        if decision == 'a':
                            target = view.ask_who_to_shoot(model.players, model.turn)
                            i, j = view.ask_for_location(model.n)
                        elif decision == 'b':
                            target_ship, movement = view.ask_what_to_move(PlayerType.HUMAN, model.turn, [model.grid_0, model.grid_1, model.grid_2])
                            model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            target = view.ask_who_to_scan(model.players, model.turn)
                            i, j = view.ask_for_top_left_scan_point(model.n)
                            model.scan(i, j, target)
                    # Bot P1
                    else:
                        # decide action
                        decision = view.ask_what_action(PlayerType.BOT, model.turn)
                        if decision == 'a':
                            target = model.get_random_target()
                            i, j = model.get_random_ij()
                            view.show_shot(i, j, model.turn)
                        elif decision == 'b':
                            target_ship, movement = model.get_random_ship_move()
                            if target_ship and movement:
                                model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            target = model.get_random_target()
                            i, j = model.get_random_ij()
                            model.scan(i, j, target)
                # Player 2
                else:
                    # Human P2
                    if player_2 == PlayerType.HUMAN:
                        view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)
                        
                        # decide action
                        decision = view.ask_what_action(PlayerType.HUMAN, model.turn)
                        if decision == 'a':
                            target = view.ask_who_to_shoot(model.players, model.turn)
                            i, j = view.ask_for_location(model.n)
                        elif decision == 'b':
                            target_ship, movement = view.ask_what_to_move(PlayerType.HUMAN, model.turn, [model.grid_0, model.grid_1, model.grid_2])
                            model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            target = view.ask_who_to_scan(model.players, model.turn)
                            i, j = view.ask_for_top_left_scan_point(model.n)
                            model.scan(i, j, target)
                    # Bot P2
                    else:
                        # decide action
                        decision = view.ask_what_action(PlayerType.BOT, model.turn)
                        if decision == 'a':
                            target = model.get_random_target()
                            i, j = model.get_random_ij()
                            view.show_shot(i, j, model.turn)
                        elif decision == 'b':
                            target_ship, movement = model.get_random_ship_move()
                            if target_ship and movement:
                                model.move_ship((target_ship, movement))
                        elif decision == 'c':
                            target = model.get_random_target()
                            i, j = model.get_random_ij()
                            model.scan(i, j, target)
            view.show_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)

            if decision == 'a':            
                model.shoot(i, j, target)
            model.go_to_next_turn()

        
        view.show_final_grids(model.grids(), model.turn, [model.player0_shots, model.player1_shots, model.player2_shots], model.n)
        view.show_end_message(model.winner())


my_model = BattleshipModel()
my_view = BattleshipView()
my_controller = BattleshipController(my_model, my_view)
my_controller.run()


# DRAFT 1

'''class BattleshipModel:
    def __init__(self, 
        n: int = 6, 
        ship_sizes: Sequence[int] = (4, 3, 2, 2), 
        rng: Random = Random(), 
        turn: int = 0,
        grid_pair: Sequence[list[str], list[str]] = [[], []],
        shot_grids: Sequence[Sequence] = []
        ):

        self.n = n # row num
        self.ship_sizes = ship_sizes # the ships
        self.rng = rng # just Random()
        self.turn = turn # stay on 0 if single player
        # [MODIFIED] added grid_pair, shot_grids
        self.grid_pair = [generate_grid(self.n, self.ship_sizes, self.rng), generate_grid(self.n, self.ship_sizes, self.rng)]
        self.shot_grids = shot_grids

    def is_game_over(self) -> bool:
        grid1_alive = False
        grid2_alive = False

        for r, row in enumerate(self.grid_pair[0]):
            for c, col in enumerate(row):
                if (self.grid_pair[0][r][c]).isupper():
                    grid1_alive = True
                if (self.grid_pair[1][r][c]).isupper():
                    grid2_alive = True
        game_over = ((grid1_alive) == False) or ((grid2_alive) == False)
        return game_over

    # [NOTEE] grids is a method in the instructions, but is treated as an attribute in the provided controller
    # [Solution via sir Kevin] make grids() as a
    # your grid and opp grid
    def grids(self) -> Sequence[list[str], list[str]]:
        return [generate_grid(self.n, self.ship_sizes, self.rng), generate_grid(self.n, self.ship_sizes, self.rng)]

    #return 0 if user won
    def winner(self) -> int:
        for r, row in enumerate(self.grid_pair[0]):
            for c, col in enumerate(row):
                if (self.grid_pair[0][r][c]).isupper():
                    return 0
        return 1


    # advance to the next turn of the game
    # refer which grid will be shot 
    def go_to_next_turn(self):
        if self.turn == 0:
            self.turn = 1
        elif self.turn == 1:
            self.turn = 0
    # row-column pair for the bot
    def get_random_ij(self) -> Sequence[int, int]:
        return (self.rng.randint(0, self.n-1), self.rng.randint(0, self.n-1))
    # uses i,j, and go_to_next_turn() on which to be shot
    def shoot(self, i: int, j: int):
        if self.turn == 0: # shoot opp
            if self.grid_pair[1][i][j] == ".":
                self.shot_grids.append((i, j))
            else:
                self.shot_grids.append((i, j))
                target = self.grid_pair[1][i][j]
                for r, row in enumerate(self.grid_pair[1]):
                    for c, col in enumerate(row):
                        if self.grid_pair[1][r][c] == target:
                            self.grid_pair[1][r][c] = target.lower()
        elif self.turn == 1: # opp shoots user
            if self.grid_pair[0][i][j] != ".":
                target = self.grid_pair[0][i][j]
                for r, row in enumerate(self.grid_pair[0]):
                    for c, col in enumerate(row):
                        if self.grid_pair[0][r][c] == target:
                            self.grid_pair[0][r][c] = target.lower()


# UPDATE show_grids() TO ONLY REVEAL IN MODEL.SHOT_GRIDS 
   
class BattleshipView:
    # [MODIFIED] Modified show when shot 
    def show_grids(self, grids: Sequence[Sequence[str]], reveal_opp: bool = False):
        def strnger(row:list[str]):
            return "".join(row)

        for rows in zip(*grids, strict=True):
            line = ""
            for kth_grid, r_part in enumerate([*rows]):
                for char in r_part:
                    if reveal_opp == False and kth_grid != 0: # reveal switch
                        line += '?'
                    else:
                        line += char
                line += "  " #separator
            print(line)
        print()

    def ask_for_location(self, n: int) -> tuple[int, int]:
        i, j = -1, -1

        while not 0 <= i < n:
            try:
                i = int(input(f"Choose a row    [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except:
                ...

        while not 0 <= j < n:
            try:
                j = int(input(f"Choose a column [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except:
                ...

        print()
        return i, j

    def show_shot(self, i: int, j: int):
        print(f"({i},{j}) was shot!")
        print()

    def show_end_message(self, winner: int):
        if winner == 0:
            print("You win!")
        else:
            print("You lose...")
        print()


class BattleshipController:
    def __init__(self, model: BattleshipModel, view: BattleshipView):
        self._model = model
        self._view = view

    def run(self):
        model = self._model
        view = self._view

        while model.is_game_over() == False:
            if model.turn == 0:
                #[MODIFIED] updated view.show_grids(model.grid_pair instead of model.grids())
                
                view.show_grids(model.grid_pair, True) # CHEATTT FOR PROTOTYPINGG, RETURN TO FALSE AFTER
                i, j = view.ask_for_location(model.n)
            else:
                i, j = model.get_random_ij()
                view.show_shot(i, j)

            model.shoot(i, j)
            model.go_to_next_turn()
            
        # [MODIFIED] updated view.show_grids(model.grid_pair, True instead of model.grids())
        view.show_grids(model.grid_pair, True) 
        view.show_end_message(model.winner())

model = BattleshipModel()
view = BattleshipView()
controller = BattleshipController(model, view)
controller.run()
'''

# Original Code

"""# pyright: strict

from __future__ import annotations

from collections.abc import Sequence


class BattleshipView:
    def show_grids(self, grids: Sequence[Sequence[str]]):
        for rows in zip(*grids, strict=True):
            print(*rows, sep="\t")
        print()

    def ask_for_location(self, n: int) -> tuple[int, int]:
        i, j = -1, -1

        while not 0 <= i < n:
            try:
                i = int(input(f"Choose a row    [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except:
                ...

        while not 0 <= j < n:
            try:
                j = int(input(f"Choose a column [0-{n-1}]: "))
            except KeyboardInterrupt:
                exit()
            except:
                ...

        print()
        return i, j

    def show_shot(self, i: int, j: int):
        print(f"({i},{j}) was shot!")
        print()

    def show_end_message(self, winner: int):
        if winner == 0:
            print("You win!")
        else:
            print("You lose...")
        print()


class BattleshipController:
    def __init__(self, model: BattleshipModel, view: BattleshipView):
        self._model = model
        self._view = view

    def run(self):
        model = self._model
        view = self._view

        while not model.is_game_over:
            if model.turn == 0:
                view.show_grids(model.grids)
                i, j = view.ask_for_location(model.n)
            else:
                i, j = model.get_random_ij()
                view.show_shot(i, j)

            model.shoot(i, j)
            model.go_to_next_turn()

        view.show_grids(model.grids)
        view.show_end_message(model.winner)
"""
# pyright: strict

from __future__ import annotations

from collections.abc import Sequence


from collections.abc import Sequence
from random import Random
from string import ascii_uppercase


def generate_grid(n: int, ship_sizes: Sequence[int], rng: Random) -> list[list[str]]:
    grid = [["."] * n for _ in range(n)]

    for ship_index, ship_size in enumerate(ship_sizes):
        orie = rng.choice("VH")

        def poss_gen():
            def good(i: int, j: int, k: int) -> bool:
                _i = i + (k if orie == "V" else 0)
                _j = j + (k if orie == "H" else 0)
                return 0 <= _i < n and 0 <= _j < n and grid[_i][_j] == "."

            for i in range(n):
                for j in range(n):
                    if all(good(i, j, k) for k in range(ship_size)):
                        yield (i, j)

        poss = [*poss_gen()]
        i, j = rng.choice(poss)

        for k in range(ship_size):
            _i = i + (k if orie == "V" else 0)
            _j = j + (k if orie == "H" else 0)
            grid[_i][_j] = ascii_uppercase[ship_index]

    return grid

#
'''
1. who to scan
2. give i, j

def scan(self, i: int, j:int, target:int) -> None:
        # setup the target grid and saved shots for each player
        target_grid_dic: dict[int, Sequence[Sequence[int]]] = {0:self.grid_0, 1:self.grid_1, 2:self.grid_2}
        player_saved_shots_dic: dict[int, Sequence[Sequence[int]]] = {0:self.player0_shots, 1:self.player1_shots, 2:self.player2_shots}
        target_grid: Sequence[Sequence[int]] = target_grid_dic[target]

        for r in range(len(target_grid)):
            for c in range(len(target_grid[0])):
                if i <= r <= i + k - 1 and j <= c <= j + k - 1:
                    player_saved_shots_dic[self.turn].append((i, j))

'''

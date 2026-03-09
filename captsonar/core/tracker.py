import numpy as np

from .update import BombUpdate, Direction, DroneUpdate, SonarUpdate


def sonar_intersection(a: set, b: set, all: set) -> set:
    not_a = all - a
    not_b = all - b
    return a.intersection(not_b).union(b.intersection(not_a))


class Track(object):
    def __init__(self, weight=1):
        self.pos_list: list[tuple[int, int]] = []
        self.weight = weight

    def set_weight(self, new_weight):
        self.weight = new_weight

    def is_visited(self, coord):
        return coord in self.pos_list

    def visit(self, coord: tuple[int, int]):
        self.pos_list.append(coord)

    def head(self):
        return self.pos_list[-1]

    def copy(self):
        result = self.__class__(weight=self.weight)
        result.pos_list.extend(self.pos_list)
        return result

    def trim_to_head(self):
        result = self.__class__(weight=self.weight)
        result.pos_list.append(self.head())
        return result

    def __repr__(self):
        return f"Track({self.pos_list})"


class Tracker(object):
    def __init__(self, grid):
        self.grid = grid
        self.tracks: list[Track] = []

        for i, j in np.ndindex(grid.shape):
            if not grid[(i, j)]:
                track = Track()
                track.visit((i, j))
                self.tracks.append(track)

    def in_grid(self, pos):
        return 0 <= pos[0] < self.grid.shape[0] and 0 <= pos[1] < self.grid.shape[1]

    def pos_add(self, pos_1, pos_2):
        return (pos_1[0] + pos_2[0], pos_1[1] + pos_2[1])

    def mul_pos(self, pos, mul):
        return (pos[0] * mul, pos[1] * mul)

    def pos_sector(self, pos):
        return 1 + ((pos[0] // 5) + (2 - (pos[1] // 5)) * 3)

    def pos_sub(self, pos_1, pos_2):
        return (pos_1[0] - pos_2[0], pos_1[1] - pos_2[1])

    def bomb_dist(self, pos_1, pos_2):
        return max(abs(x) for x in self.pos_sub(pos_1, pos_2))

    def update_with_dir(self, direction: Direction):
        offset = direction.to_offset()
        new_tracks = []
        for track in self.tracks:
            old_track_head = track.head()
            new_track_head = self.pos_add(old_track_head, offset)
            if not self.in_grid(new_track_head):
                continue
            if self.grid[new_track_head]:
                continue
            if track.is_visited(new_track_head):
                continue
            else:
                track.visit(new_track_head)
                new_tracks.append(track)

        self.tracks = new_tracks

    def update_with_silence(self):
        new_tracks = []
        for track in self.tracks:
            old_track_head = track.head()
            for dir in Direction:
                offset = dir.to_offset()
                last_dir_track = track
                for distance in range(1, 5):
                    new_track_head = self.pos_add(
                        old_track_head, self.mul_pos(offset, distance)
                    )
                    if not self.in_grid(new_track_head):
                        break
                    if self.grid[new_track_head]:
                        break
                    if track.is_visited(new_track_head):
                        break
                    else:
                        new_track = last_dir_track.copy()
                        new_track.visit(new_track_head)
                        new_tracks.append(new_track)
                        last_dir_track = new_track

        self.tracks = new_tracks

    def update_with_drone(self, update: DroneUpdate):
        new_tracks = []
        if update.positive:
            for track in self.tracks:
                if self.pos_sector(track.head()) == update.sector:
                    new_tracks.append(track)
        else:
            for track in self.tracks:
                if self.pos_sector(track.head()) != update.sector:
                    new_tracks.append(track)
        self.tracks = new_tracks

    def update_with_surface(self):
        head_tracks = {}
        head_weights = {}
        for track in self.tracks:
            head = track.head()
            if head not in head_tracks:
                head_tracks[head] = track.trim_to_head()
                head_weights[head] = track.weight
            else:
                head_weights[head] += track.weight

        new_tracks = []
        for head, track in head_tracks.items():
            track.set_weight(head_weights[head])
            new_tracks.append(track)

        self.tracks = new_tracks

    def track_indices_with_x(self, x):
        return set(i for (i, track) in enumerate(self.tracks) if track.head()[0] == x)

    def track_indices_with_y(self, y):
        return set(i for (i, track) in enumerate(self.tracks) if track.head()[1] == y)

    def track_indices_with_sector(self, sector):
        return set(
            i
            for (i, track) in enumerate(self.tracks)
            if self.pos_sector(track.head()) == sector
        )

    def update_with_sonar(self, update: SonarUpdate):
        all = set(range(len(self.tracks)))

        x = update.x
        y = update.y
        sector = update.sector

        if sector is None:
            assert x is not None
            assert y is not None

            with_x = self.track_indices_with_x(x)
            with_y = self.track_indices_with_y(y)

            selected = sonar_intersection(with_x, with_y, all)
        elif x is None:
            assert y is not None
            assert sector is not None

            with_y = self.track_indices_with_y(y)
            with_sector = self.track_indices_with_sector(sector)

            selected = sonar_intersection(with_y, with_sector, all)
        else:
            assert x is not None
            assert sector is not None

            with_x = self.track_indices_with_x(x)
            with_sector = self.track_indices_with_sector(sector)

            selected = sonar_intersection(with_x, with_sector, all)

        new_tracks = []
        for i, track in enumerate(self.tracks):
            if i in selected:
                new_tracks.append(track)
        self.tracks = new_tracks

    def update_with_bomb(self, update: BombUpdate):
        assert update.damage <= 2

        new_tracks = []
        if update.damage == 0:
            for track in self.tracks:
                if self.bomb_dist(track.head(), update.pos) >= 2:
                    new_tracks.append(track)
        else:
            expected_dist = 2 - update.damage
            for track in self.tracks:
                if self.bomb_dist(track.head(), update.pos) == expected_dist:
                    new_tracks.append(track)

        self.tracks = new_tracks

    def cell_probs(self):
        result = np.zeros(self.grid.shape, dtype=np.float32)

        if not self.tracks:
            return result

        total = 0
        for track in self.tracks:
            result[track.head()] += track.weight
            total += track.weight

        result /= total
        return result

import sys
from typing import List, Optional, Tuple
from functools import cache
import logging

LOG = logging.getLogger(__name__)

SHOW_SOLUTIONS = False
STORE_SOLUTIONS = False

class SlitherlinkSolver:
    xsize: int
    ysize: int
    current: List[Tuple[Tuple[int, int], ...]]

    def __init__(self, xsize: int, ysize: int):
        self.xsize = xsize
        self.ysize = ysize
        self.current = []

    @cache
    def merge_comp(self, vertical: Tuple[Tuple[int, int], ...], horizontal: Tuple[Tuple[int, int], ...]) -> Tuple[Tuple[Tuple[int, int], ...], int]:
        # Returns a tuple of
        #  - new set of vertical pairs
        #  - number of loops closed

        vdict = {}
        hdict = {}
        for c, (h1, h2) in enumerate(vertical):
            vdict[h1] = c
            vdict[h2] = c
        for (h1, h2) in horizontal:
            hdict[h1] = h2
            hdict[h2] = h1

        used_horizontal = set()
        used_vertical = set()

        def follow(x: int) -> Optional[int]:
            while x in vdict:
                h1, h2 = vertical[vdict[x]]
                assert (h1, h2) not in used_vertical
                used_vertical.add((h1,h2))
                assert h1 < h2
                x = h1 + h2 - x
                if x not in hdict:
                    return x
                nx = hdict[x]
                h = ordered(x, nx)
                if h in used_horizontal:
                    return None
                used_horizontal.add(h)
                x = nx

            return x


        def ordered(h1: int, h2: int) -> Tuple[int, int]:
            return (h1, h2) if h1 < h2 else (h2, h1)

        num_closed = 0
        res: List[Tuple[int, int]] = []
        for h1, h2 in horizontal:
            assert h1 < h2
            if (h1, h2) in used_horizontal:
                continue
            used_horizontal.add((h1, h2))
            nh1 = follow(h1)
            if nh1 is not None:
                nh2 = follow(h2)
                assert nh2 is not None
                res.append(ordered(nh1, nh2))
            else:
                num_closed += 1

        for h1, h2 in vertical:
            assert h1 < h2
            if (h1,h2) not in used_vertical:
                res.append((h1, h2))

        return tuple(sorted(res)), num_closed

    @cache
    def generate_horizontal_segments(self, verticals: Tuple[Tuple[int, int], ...]) -> List[Tuple[Tuple[int, int], ...]]:
        vset = set()
        for h1, h2 in verticals:
            vset.add(h1)
            vset.add(h2)

        res = []
        cur = []

        def rec(x):
            if x >= self.xsize:
                res.append(tuple(cur))
                return

            rec(x+1)

            nx = x+1
            cur.append((x, nx))
            rec(nx + 1)
            while nx not in vset and nx < self.xsize:
                cur.pop()
                nx += 1
                cur.append((x, nx))
                rec(nx + 1)
            cur.pop()


        rec(0)
        return sorted(res)

    def show_current(self):
        def show_row(horz: Tuple[Tuple[int, int], ...]):
            s = [" "] * self.xsize
            for h1, h2 in horz:
                for x in range(h1, h2):
                    s[x] = '-'
            print(f"+{'+'.join(s)}+")

        is_active = [False] * (self.xsize + 1)
        for y in range(self.ysize + 1):
            cur_horz = self.current[y] if y < len(self.current) else ()
            for h1, h2 in cur_horz:
                is_active[h1] = not is_active[h1]
                is_active[h2] = not is_active[h2]
            show_row(cur_horz)
            if y < self.ysize:
                s = ["|" if a else " " for a in is_active]
                print(" ".join(s))
        print()
        print("==" * (self.xsize+1))
        print()


    @cache
    def count_loops_rec(self, verticals: Tuple[Tuple[int, int], ...], row_num: int) -> int:
        if row_num > self.ysize:
            return 0

        num_solutions = 0
        started = len(verticals) > 0

        for horz_segments in self.generate_horizontal_segments(verticals):
            try:
                if SHOW_SOLUTIONS or STORE_SOLUTIONS:
                    self.current.append(horz_segments)
                new_verticals, closed_loops = self.merge_comp(verticals, horz_segments)
                if closed_loops == 1:
                    if len(new_verticals) == 0 and started:
                        if SHOW_SOLUTIONS:
                            self.show_current()
                        num_solutions += 1
                elif closed_loops == 0:
                    num_solutions += self.count_loops_rec(new_verticals, row_num+1)
            finally:
                if SHOW_SOLUTIONS or STORE_SOLUTIONS:
                    self.current.pop()

        return num_solutions

    def count_loops(self) -> int:
        LOG.debug(f"Counting loops in grid of size {self.xsize}x{self.ysize}")
        num_solutions = self.count_loops_rec((), 0)
        LOG.debug(f"Number of solutions: {num_solutions}")
        try:
            LOG.debug("Cache info:")
            LOG.debug("------------")
            LOG.debug(f"count_loops_rec {self.count_loops_rec.cache_info()}")
            LOG.debug(f"merge_comp {self.merge_comp.cache_info()}")
            LOG.debug(f"generate_row_patterns {self.generate_horizontal_segments.cache_info()}")
        except:
            pass
        return num_solutions


logging.basicConfig(level=logging.DEBUG)
solver = SlitherlinkSolver(int(sys.argv[1]), int(sys.argv[2]))
solver.count_loops()

# for ysize in range(1, 8):
#     s = ""
#     for xsize in range(1, 8):
#         solver = SlitherlinkSolver(xsize, ysize)
#         s += f"{solver.count_loops():12d} "
#     print(s)

from puzzles.slitherlink import generate_horizontal_segments, merge_comp


def test_merge_comp_simple():
    assert merge_comp([(1, 13)], [(1, 2), (13, 15)]) == ([(2, 15)], 0)


def test_merge_comp_multiple():
    assert merge_comp(
        [(1, 13), (3, 11), (6, 8)], [(1, 2), (3, 6), (9, 11), (13, 15)]
    ) == ([(2, 15), (8, 9)], 0)


def test_merge_no_horz():
    assert merge_comp([(5, 8)], []) == ([(5, 8)], 0)


def test_merge_no_vert():
    assert merge_comp([], [(3, 6), (7, 8), (15, 20)]) == ([(3, 6), (7, 8), (15, 20)], 0)


def test_close_single_loop():
    assert merge_comp([(1, 4)], [(1, 4)]) == ([], 1)


def test_close_complex_loops():
    assert merge_comp(
        [(1, 16), (4, 9), (7, 8), (12, 14)], [(1, 4), (5, 7), (9, 12), (14, 16)]
    ) == ([(5, 8)], 1)


def test_no_vert_or_horz():
    assert merge_comp([], []) == ([], 0)


def test_generate_horizontal_simple():
    assert generate_horizontal_segments([], 2) == [
        (),
        ((0, 1),),
        ((0, 2),),
        ((1, 2),),
    ]

def test_generate_horizontal_larger():
    assert generate_horizontal_segments([], 4) == [
        (),
        ((0, 1),),
        ((0, 1), (2, 3)),
        ((0, 1), (2, 4)),
        ((0, 1), (3, 4)),
        ((0, 2),),
        ((0, 2), (3, 4)),
        ((0, 3),),
        ((0, 4),),
        ((1, 2),),
        ((1, 2), (3, 4)),
        ((1, 3),),
        ((1, 4),),
        ((2, 3),),
        ((2, 4),),
        ((3, 4),),
    ]


def test_generate_horizontal_with_verticals():
    assert generate_horizontal_segments([(1, 3)], 4) == [
        (),
        ((0, 1),),
        ((0, 1), (2, 3)),
        ((0, 1), (3, 4)),
        ((1, 2),),
        ((1, 2), (3, 4)),
        ((1, 3),),
        ((2, 3),),
        ((3, 4),),
    ]
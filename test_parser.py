import parser
#TESTS


def run_all_tests():
    tests = [test_within_braces, test_find_right_most_colon]
    for t in tests:
        t()
    return


def test_within_braces():
    assert parser.within_braces('(b!+c):(b:B)', 9)
    assert parser.within_braces('(b!+c):(b:B)', 3)
    assert parser.not_within_braces('(b!+c):(b:B)', 6)
    assert parser.not_within_braces('(b!+c):(b:B)', 5)
    return


def test_find_right_most_colon():
    assert parser.find_right_most_colon('(b!+c):(b:B)') == 6
    assert parser.find_right_most_colon('bla') is None
    return


run_all_tests()
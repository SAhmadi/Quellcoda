import unittest


class TestRouteRun(unittest.TestCase):
    """ """

    def test_route_run(self):
        self.assertEqual('run example'.upper(), 'RUN EXAMPLE')


if __name__ == '__main__':
    unittest.main()
from spconfigreader import configreader

import unittest


class Test:
    val1: str
    val2: str

    def __str__(self):
        return "\tTest:\n\t\tval1: {}\n\t\tval2: {}\n".format(self.val1, self.val2)

    def __eq__(self, value):
        if not isinstance(value, Test):
            return False
        return self.val1 == value.val1 and self.val2 == value.val2


class Datasource:
    __path__: str = "datasource"

    server: str
    port: int = 1433
    protocol: str = "tcp"
    test = Test()

    def __str__(self):
        return "Datasource:\n\tserver: {}\n\tport: {}\n\tprotocol: {}\n{}".format(self.server, self.port, self.protocol, self.test)

    def __eq__(self, value) -> bool:
        if not isinstance(value, Datasource):
            return False
        return self.server == value.server and self.port == value.port and self.protocol == value.protocol and self.test == value.test

    def function(self):
        pass


class TestSum(unittest.TestCase):
    def test_getObject(self):
        match = Datasource()
        match.server = "mssql.server"
        match.port = 1433
        match.protocol = "tcp"

        match.test.val1 = "foo"
        match.test.val2 = "bar"

        result = configreader.getObject(Datasource())

        self.assertEqual(result, match)


if __name__ == '__main__':
    unittest.main()

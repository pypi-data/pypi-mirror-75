import unittest


from .stopwords import Stopwords


class StopwordsTest(unittest.TestCase):

    def testDefaultStopwords(self):
        sw = Stopwords()
        print(sw.size())
        print(sw.contains('的'))


if __name__ == "__main__":
    unittest.main()

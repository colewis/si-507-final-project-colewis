import unittest
from fetch_dogs import *

class TestDatabase(unittest.TestCase):

    def test_breed_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT BreedName FROM Breeds'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Appenzeller Sennenhund',), result_list) #1
        self.assertEqual(len(result_list), 15) #2

        sql = '''
            SELECT BreedName, Group_Id, ActivityLevel_Id
            FROM Breeds
            WHERE Size_Id=5
            ORDER BY ActivityLevel_Id DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 2) #3
        self.assertEqual(result_list[0][2], 4) #4
        self.assertIn(('Anatolian Shepherd Dog', 2, 1),  result_list) #5


        sql = '''
            SELECT COUNT(*)
            FROM Breeds
            WHERE Size_Id = 5
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 2) #6


        conn.close()

    def test_shedding_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Description
            FROM Shedding
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Seasonal',), result_list) #7
        self.assertEqual(len(result_list), 6) #8
        self.assertFalse('Infrequent' in result_list) #9
        self.assertTrue(('Infrequent',) in result_list) #10

        sql = '''
            SELECT COUNT(*)
            FROM Shedding
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 6) #11

        conn.close()

    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT BreedName
            FROM Breeds
                JOIN Coat_Type
                ON Breeds.CoatType_Id=Coat_Type.Id
            WHERE BarkingLevel_Id=2
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('American Water Spaniel',), result_list) #12
        self.assertTrue(len(result_list), 9) #13

        sql = '''
            SELECT BreedName
            FROM Breeds
                JOIN Trainability
                ON Breeds.Trainability_Id=Trainability.Id
            WHERE BarkingLevel_Id=1
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 0) #14
        self.assertFalse('Akita' in result_list) #15

        conn.close()

unittest.main()

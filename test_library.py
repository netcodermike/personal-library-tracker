import unittest,tempfile,csv
from pathlib import Path
from library import Library
class Tests(unittest.TestCase):
    def test_reading_and_lending(self):
        l=Library(':memory:')
        try:
            book=l.add('Dune','Frank Herbert');l.status(book,'reading');l.lend(book,'Ada','2030-01-10')
            self.assertEqual(l.get(book)['status'],'reading');self.assertEqual(l.books('herbert')[0]['borrower'],'Ada')
            with self.assertRaises(ValueError):l.lend(book,'Ben','2030-01-20')
            l.returned(book);self.assertEqual(l.get(book)['borrower'],'')
            with self.assertRaises(ValueError):l.lend(book,'Ada','invalid')
        finally:l.close()
    def test_persistence_literal_search_and_csv(self):
        with tempfile.TemporaryDirectory()as tmp:
            db=Path(tmp)/'books.sqlite3';l=Library(db);l.add('100% Python','=Author');l.add('Other','Someone');l.close();l=Library(db)
            try:
                self.assertEqual(len(l.books('%')),1);path=Path(tmp)/'export.csv';l.export(path)
                with path.open(newline='',encoding='utf-8')as f:rows=list(csv.reader(f))
                self.assertEqual(rows[1][2],"'=Author")
            finally:l.close()
if __name__=='__main__':unittest.main()

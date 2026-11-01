"""Проверка отношений и запросов для всех шести вариантов."""
import unittest
from main import build_relations, computers, drives, drive_computers, run_queries


class TestRubezhnyControl(unittest.TestCase):
    def test_foreign_keys(self):
        computer_ids = {computer.id for computer in computers}
        drive_ids = {drive.id for drive in drives}
        self.assertTrue(all(drive.computer_id in computer_ids for drive in drives))
        self.assertTrue(all(link.computer_id in computer_ids and link.drive_id in drive_ids
                            for link in drive_computers))

    def test_relationship_sizes(self):
        one, many = build_relations()
        self.assertEqual(len(one), len(drives))
        self.assertEqual(len(many), len(drive_computers))

    def test_variant_a(self):
        result1, result2, result3 = run_queries("А")
        self.assertEqual([r[2] for r in result1], sorted(r[2] for r in result1))
        self.assertIn(("Архивный компьютер", 1536), result2)
        self.assertEqual(result3["Архивный компьютер"], ["Альфа", "Атласов", "Астра"])

    def test_all_variants(self):
        for letter in "АБВГДЕ":
            with self.subTest(letter=letter):
                answers = run_queries(letter)
                self.assertEqual(len(answers), 3)
                self.assertTrue(all(answer for answer in answers))

    def test_invalid_variant(self):
        with self.assertRaises(ValueError):
            run_queries("Ж")


if __name__ == "__main__":
    unittest.main()

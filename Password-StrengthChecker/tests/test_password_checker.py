"""Unit testing suite verifying assertions across extreme bounds and requirements."""

import unittest
import password_checker
import utils

class TestPasswordChecker(unittest.TestCase):

    def test_empty_password(self):
        """Validates behavior when handling missing parameters gracefully."""
        res = password_checker.analyze_password("")
        self.assertEqual(res["score"], 0)
        self.assertEqual(res["category"], "Very Weak")
        self.assertEqual(res["entropy"], 0.0)

    def test_weak_passwords(self):
        """Verifies classic blacklisted dictionary vectors are heavily down-voted."""
        res = password_checker.analyze_password("123456")
        self.assertTrue(res["metrics"]["highly_common"])
        self.assertEqual(res["category"], "Very Weak")

    def test_strong_passwords(self):
        """Checks high score evaluation for complex inputs."""
        res = password_checker.analyze_password("C0mpl3x#Str0ng!P@ss")
        self.assertTrue(res["metrics"]["length_ok"])
        self.assertTrue(res["metrics"]["has_upper"])
        self.assertTrue(res["metrics"]["has_special"])
        self.assertGreaterEqual(res["score"], 80)

    def test_entropy_logic(self):
        """Validates that text variety matches bit calculations."""
        low_ent = password_checker.calculate_entropy("aaaa")
        high_ent = password_checker.calculate_entropy("aA1!")
        self.assertGreater(high_ent, low_ent)

    def test_generator_output(self):
        """Ensures the secure factory meets minimum validation conditions."""
        generated = utils.generate_password(12)
        self.assertEqual(len(generated), 12)
        res = password_checker.analyze_password(generated)
        self.assertTrue(res["metrics"]["has_upper"])
        self.assertTrue(res["metrics"]["has_lower"])
        self.assertTrue(res["metrics"]["has_digits"])

if __name__ == "__main__":
    unittest.main()
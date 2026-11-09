import unittest
from agents.policies import SpendPolicy

class TestSpendPolicy(unittest.TestCase):
    def test_allowlist_success(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=["0x123"], denylist=[])
        # Should not raise
        policy.check("0x123", 500)

    def test_allowlist_failure(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=["0x123"], denylist=[])
        with self.assertRaisesRegex(ValueError, "Destination not in allowlist"):
            policy.check("0x456", 500)

    def test_denylist_failure(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=[], denylist=["0x123"])
        with self.assertRaisesRegex(ValueError, "Destination is denylisted"):
            policy.check("0x123", 500)

    def test_denylist_overrides_allowlist(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=["0x123"], denylist=["0x123"])
        with self.assertRaisesRegex(ValueError, "Destination is denylisted"):
            policy.check("0x123", 500)

    def test_max_value_wei_success(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=[], denylist=[])
        policy.check("0x123", 1000)
        policy.check("0x123", 500)
        policy.check("0x123", 0)

    def test_max_value_wei_failure(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=[], denylist=[])
        with self.assertRaisesRegex(ValueError, "Transfer exceeds policy max value"):
            policy.check("0x123", 1001)

    def test_case_insensitivity(self):
        policy = SpendPolicy(max_value_wei=1000, allowlist=["0xAbC"], denylist=["0xDeF"])
        policy.check("0xabc", 500)
        policy.check("0xABC", 500)

        with self.assertRaisesRegex(ValueError, "Destination is denylisted"):
            policy.check("0xdef", 500)

        with self.assertRaisesRegex(ValueError, "Destination is denylisted"):
            policy.check("0xDEF", 500)

if __name__ == '__main__':
    unittest.main()

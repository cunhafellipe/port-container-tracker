import unittest
from demo import domain


class ContainerTests(unittest.TestCase):
    def test_checksum_known_example_and_invalid_check_digit(self):
        self.assertTrue(domain.valid_container_id("CSQU3054383"))
        self.assertFalse(domain.valid_container_id("CSQU3054384"))
        self.assertFalse(domain.valid_container_id("CSQX3054383"))
        self.assertTrue(all(domain.valid_container_id(r["id"]) for r in domain.seed()))

    def test_hold_prevents_release_then_clearance_allows_it(self):
        r = next(r for r in domain.seed() if r["hold"] and r["state"] == "yard")
        with self.assertRaises(ValueError):
            domain.execute([r], dict(id=r["id"], action="advance"))
        with self.assertRaises(ValueError):
            domain.execute([r], dict(id=r["id"], action="clear_hold", note=""))
        r = domain.execute(
            [r], dict(id=r["id"], action="clear_hold", note="Demo customs clearance")
        )
        r = domain.execute([r], dict(id=r["id"], action="advance"))
        self.assertEqual(r["state"], "released")
        r = domain.execute([r], dict(id=r["id"], action="advance"))
        self.assertEqual(r["state"], "gate_out")
        with self.assertRaises(ValueError):
            domain.execute([r], dict(id=r["id"], action="advance"))

    def test_departed_container_dwell_uses_exit_timestamp(self):
        r = next(r for r in domain.seed() if r["state"] == "gate_out")
        self.assertEqual(domain.dwell(r), 2)

    def test_dwell_target_is_strict(self):
        r = domain.seed()[0]
        r["arrived"] = "2026-06-11T08:00:00+00:00"
        self.assertFalse(domain.present([r])[0]["exception"])

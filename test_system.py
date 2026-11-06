import unittest
from api import validate_member
from database import next_member_id,membership_status

SAMPLE={"full_name":"Juan Dela Cruz","age":"25","gender":"Male","contact_number":"09123456789","address":"Talavera, Nueva Ecija","membership_type":"Monthly","start_date":"2026-11-01","expiration_date":"2026-11-30"}
class TestGymSystem(unittest.TestCase):
    def test_valid_member(self): self.assertIsNone(validate_member(SAMPLE))
    def test_required_name(self):
        d=dict(SAMPLE); d["full_name"]=""
        self.assertIn("Full Name",validate_member(d))
    def test_age_validation(self):
        d=dict(SAMPLE); d["age"]="0"
        self.assertIn("Age",validate_member(d))
    def test_contact_validation(self):
        d=dict(SAMPLE); d["contact_number"]="12345"
        self.assertIn("Contact number",validate_member(d))
    def test_date_validation(self):
        d=dict(SAMPLE); d["expiration_date"]="2026-10-01"
        self.assertIn("Expiration date",validate_member(d))
    def test_next_id(self):
        self.assertEqual(next_member_id([{"member_id":"PG-0001"},{"member_id":"PG-0003"}]),"PG-0004")
    def test_upcoming_status(self): self.assertEqual(membership_status("2099-01-01","2099-01-30"),"Upcoming")
if __name__=="__main__": unittest.main(verbosity=2)

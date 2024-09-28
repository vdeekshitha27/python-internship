class Seat:
    def __init__(self, row, number, is_occupied=False):
        self.row = row
        self.number = number
        self.is_occupied = is_occupied
    def __repr__(self):
        return f"{self.row}-{self.number}{'*' if self.is_occupied else ''}"
class SeatingSection:
    def __init__(self, section_id, rows, seats_per_row):
        self.section_id = section_id
        self.rows = {row: [Seat(row, i) for i in range(1, seats_per_row + 1)] for row in range(1, rows + 1)}
    def get_seat(self, row, number):
        return self.rows[row][number - 1]
    def update_seat(self, row, number, is_occupied):
        self.rows[row][number - 1].is_occupied = is_occupied
    def __repr__(self):
        return f"Section {self.section_id}: "+", ".join([str(seat) for sublist in self.rows.values() for seat in sublist])
class Stadium:
    def __init__(self):
        self.sections = {}
    def add_section(self, section_id, rows, seats_per_row):
        self.sections[section_id] = SeatingSection(section_id, rows, seats_per_row)
    def remove_section(self, section_id):
        if section_id in self.sections:
            del self.sections[section_id]
    def update_seating(self, section_id, row, number, is_occupied):
        if section_id in self.sections:
            self.sections[section_id].update_seat(row, number, is_occupied)           
    def get_section(self, section_id):
        return self.sections.get(section_id, None)
    def __repr__(self):
        return "\n".join([str(section) for section in self.sections.values()])
def optimize_stadium_seating(stadium):
    # Example simple optimization: fill seats from front rows to back
    for section in stadium.sections.values():
        for row in sorted(section.rows):
            for seat in section.rows[row]:
                if not seat.is_occupied:
                    seat.is_occupied = True
def manage_seat_allocations(stadium, allocations):
    for allocation in allocations:
        section_id, row, seat_num = allocation
        if section_id in stadium.sections:
            stadium.update_seating(section_id, row, seat_num, True)
import unittest
class TestStadiumSeating(unittest.TestCase):
    def setUp(self):
        self.stadium = Stadium()
        self.stadium.add_section(101, 10, 10)
        self.stadium.add_section(102, 5, 20)
    def test_crud_seats(self):
        # Test Create/Read
        section = self.stadium.get_section(101)
        self.assertFalse(section.get_seat(1, 1).is_occupied)
        # Test Update
        self.stadium.update_seating(101, 1, 1, True)
        self.assertTrue(section.get_seat(1, 1).is_occupied)
        # Test Delete
        self.stadium.remove_section(102)
        self.assertIsNone(self.stadium.get_section(102))
    def test_optimization(self):
        optimize_stadium_seating(self.stadium)
        section = self.stadium.get_section(101)
        self.assertTrue(all(seat.is_occupied for row in section.rows.values() for seat in row))
if __name__ == "__main__":
    unittest.main()

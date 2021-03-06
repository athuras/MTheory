import unittest

from note import Note, validate


class NoteTest(unittest.TestCase):

  def test_validate(self):
    valid_notes = ['A4', 'G#-4', 'Bb2']
    invalid_notes = ['AB#2', 'A--5', 'J15', 'C3P0', 'G##4', '']
    for bad in invalid_notes:
      self.assertFalse(validate(bad))
    for good in valid_notes:
      self.assertTrue(validate(good))

  def test_frequency(self):
    # Handles some cases where the math is easy.
    self.assertEqual(Note(0), Note.from_frequency(440))
    self.assertEqual(Note(12), Note.from_frequency(880))
    self.assertEqual(Note(-24), Note.from_frequency(110))

  def test_midi(self):
    self.assertEqual(Note.from_midi(69), Note.from_frequency(440))
    self.assertAlmostEqual(Note.from_midi(60), Note.from_frequency(261.6))

  def test_parsing(self):
    self.assertIsNone(Note.parse("BB2"))
    self.assertEqual(Note(0), Note.parse('A4'))
    self.assertEqual(Note(59), Note.parse('G#8'))
    self.assertEqual(Note(-18), Note.parse('Eb2'))

if __name__ == '__main__':
    unittest.main()

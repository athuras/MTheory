from collections import namedtuple
import math
import re

_VALIDATION_REGEX = r"[A-G]([#b])?-?[0-9]+$"
_SID_TO_NAME = {
  0: 'A', 1: 'A#',
  2: 'B',
  3: 'C', 4: 'C#',
  5: 'D', 6: 'D#',
  7: 'E',
  8: 'F', 9: 'F#',
  10: 'G', 11: 'G#',
}
_NAME_TO_SID = {v: k for k, v in _SID_TO_NAME.iteritems()}

def validate(note_string):
  '''
  Validates that a note string takes the following form:
  Note Name (A-G), optionally followed by exactly one accidental, and an octave
  '''
  match = re.match(_VALIDATION_REGEX, note_string)
  return True if match else False


class Note(object):
  '''
  A data structure for identifying a note in an equal temperment scale.

  Preferred initialization using `Note.parse`.
  '''
  __slots__ = ['_semitone_id', 'octave']

  def __init__(self, semitone_id, octave):
    self._semitone_id = semitone_id
    self.octave = octave

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return (self._semitone_id == other._semitone_id and
              self.octave == other.octave)
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return '%s(%s)' % (self.__class__.__name__, self.name)

  @property
  def name(self):
    '''i.e. A#3'''
    return _SID_TO_NAME[self._semitone_id] + str(self.octave)

  @property
  def frequency(self, reference=440.0):
    '''
    :reference [hz] is used to define the frequency of A4.
    '''
    semitone_offset = 12 * (self.octave - 4) + self._semitone_id
    return reference * math.pow(2.0, semitone_offset  / 12.0)

  @property
  def midi(self):
    return ((12 * self.octave - 4) + self._semitone_id) + 69

  @classmethod
  def from_midi(cls, midi_value):
    octave, semi = divmod(midi_value - 69, 12)
    return cls(semi, octave + 4)

  @classmethod
  def from_frequency(cls, frequency, reference=440.0):
    '''
    Find the closest note to the provided frequency.
    :reference [hz] is used to define the frequency of A4.
    '''
    n = 12 * (math.log(frequency) - math.log(reference)) / math.log(2)
    low, high = math.floor(n), math.ceil(n)
    low_err = n - low
    high_err = high - n
    i = math.trunc(low) if low_err < high_err else math.trunc(high)
    octave, si = divmod(i, 12)
    return cls(si, octave + 4)

  @classmethod
  def parse(cls, note_string):
    '''
    Parse the provided note string,
    returns a `Note` instance if parsing is successful, otherwise `None`.

    EXAMPLE:
      Note.parse("A#3") # => Note(A#, 3)

    Naive implementation uses string 'in' operator, so deal with it.
    '''
    if not validate(note_string): return None
    note = re.match(r"([A-Z]).+", note_string)
    semitone_id = _NAME_TO_SID.get(note.groups()[0], None) if note else None
    modifier = 0
    if '#' in note_string:
      modifier += 1
    elif 'b' in note_string:
      modifier -= 1

    sign = -1 if '-' in note_string else 1

    octave = re.match(r"[A-Z][#b]?-?(\d+)", note_string)
    octave = int(octave.groups()[0]) * sign if octave else None

    if semitone_id is None or octave is None:
      return None
    else:
      return cls(semitone_id + modifier, octave)

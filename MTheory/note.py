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
  Internal note representation is an integer, with 0 corresponding to the reference pitch A4.

  Preferred initialization using the class-methods
    Note.parse
    Note.from_midi
    Note.from_frequency
  '''
  __slots__ = ['_semitone']

  def __init__(self, semitone):
    self._semitone = semitone

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self._semitone == other._semitone
    else:
      return False

  def __ne__(self, other):
    return not self.__eq__(other)

  def __repr__(self):
    return '%s(%s)' % (self.__class__.__name__, self.name)

  @property
  def midi_value(self):
    return self._semitone + 69

  @classmethod
  def from_midi_value(cls, midi_value):
    # note: 69 = A4 = Note(0)
    return cls(midi_value - 69)

  def frequency(self, reference=440.0):
    '''
    :reference [hz] is used to define the frequency of A4.
    '''
    return reference * math.pow(2.0, self._semitone  / 12.0)

  @classmethod
  def from_frequency(cls, frequency, reference=440.0):
    '''
    Find the closest note to the provided frequency.
    :reference [hz] is used to define the frequency of A4.

    EXAMPLE:
    >>> Note.from_frequency(440)
    Note(A4)
    >>> Note.from_frequency(450)
    Note(A4)
    '''
    n = 12 * math.log(frequency / reference, 2)
    low, high = math.floor(n), math.ceil(n)
    low_err = n - low
    high_err = high - n
    i = math.trunc(low) if low_err < high_err else math.trunc(high)
    return cls(i)

  @property
  def name(self):
    '''Canonical note name, i.e. "A4", "G#-2".'''
    octave, root = divmod(self._semitone, 12)
    return _SID_TO_NAME[root] + str(octave + 4)

  @classmethod
  def from_name(cls, note_string):
    '''
    Parse the provided canonical note string.
    returns a `Note` instance if parsing is successful, otherwise `None`.

    EXAMPLE:
    >>> Note.parse("A#3")
    Note(A#3)
    >>> print(Note.parse("INVALID"))
    None
    '''
    if not validate(note_string): return None
    note = re.match(r"([A-Z]).+", note_string)
    root = _NAME_TO_SID.get(note.groups()[0], None) if note else None
    modifier = 0
    if '#' in note_string:
      modifier += 1
    elif 'b' in note_string:
      modifier -= 1

    sign = -1 if '-' in note_string else 1

    octave = re.match(r"[A-Z][#b]?-?(\d+)", note_string)
    octave = int(octave.groups()[0]) * sign if octave else None

    if root is None or octave is None:
      return None
    else:
      return cls((octave - 4) * 12 + root + modifier)

import itertools
from datetime import datetime, timezone


def parse8601(s):
  '''Parse ISO8601 date string.'''

  if not s:
    return None

  formats = '%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ'
  for f in formats:
    try:
      return datetime.strptime(s, f).replace(tzinfo = timezone.utc)
    except ValueError:
      pass
  else:
    raise ValueError("time data '{}' is not supported".format(s)) from None


def chunk(iterable, k):
  '''Split iterable by chunk of k elements, see
  https://docs.python.org/3/library/itertools.html#itertools-recipes'''
  return ((i for i in c if i is not None) for c in itertools.zip_longest(*[iter(iterable)] * k))


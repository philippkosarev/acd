# Imports
from pathlib import Path
import io
import os
import tempfile

# Going into the module directory
script_file = Path(__file__)
script_dir = script_file.parent
os.chdir(script_dir)

# Checking the environment
assert Path.cwd().name.lower() == 'acd'
assert (Path.cwd() / 'acd').is_dir()

# Importing the library
import acd

# Example data
example_encryption_key = b'192-45-0-55-66-241-55-117'
example_data = {'example-file': b'example file contents'}
example_data_encrypted = b'\x0c\x00\x00\x00example-file\x15\x00\x00\x00\x96\x00\x00\x00\xb1\x00\x00\x00\x93\x00\x00\x00\x9a\x00\x00\x00\xa4\x00\x00\x00\xa1\x00\x00\x00\x92\x00\x00\x00P\x00\x00\x00\x93\x00\x00\x00\x9e\x00\x00\x00\xa1\x00\x00\x00\x92\x00\x00\x00V\x00\x00\x00\x99\x00\x00\x00\x9c\x00\x00\x00\xa0\x00\x00\x00\xa8\x00\x00\x00\x96\x00\x00\x00\x9b\x00\x00\x00\xa9\x00\x00\x00\xa8\x00\x00\x00'
example_file_to_key = {
  'testing': b'254-7-113-249-206-21-55-104',
  'test': b'192-45-0-55-66-241-55-117',
  't': b'116-0-0-131-66-101-171-171',
  '': b'0-0-0-131-66-101-171-171',
  'data': b'40-157-0-188-66-4-74-101',
  'data.acd': b'40-157-0-188-66-4-74-101',
  'DAtAbaNAnA$': b'40-157-0-188-66-4-74-101',
}

# Tests
def test_get_encryption_key():
  for (file, key) in example_file_to_key.items():
    assert key == acd.get_encryption_key(file)
    if not file:
      continue
    assert key == acd.get_encryption_key(Path(file))
    assert key == acd.get_encryption_key(Path.cwd() / file)


def test_read():
  with tempfile.TemporaryFile('rb+') as fp:
    fp.write(example_data_encrypted)
    fp.seek(0)
    data = acd.read(fp, example_encryption_key)
    assert data == example_data
    assert not fp.closed
  with io.BytesIO(example_data_encrypted) as fp:
    data = acd.read(fp, example_encryption_key)
    assert data == example_data
    assert not fp.closed


def test_write():
  with tempfile.TemporaryFile('rb+') as fp:
    fp.write(example_data_encrypted)
    fp.seek(0)
    data = acd.read(fp, example_encryption_key)
    assert data == example_data
    assert not fp.closed
  with io.BytesIO() as fp:
    acd.write(example_data, fp, example_encryption_key)
    data = fp.getvalue()
    assert data == example_data_encrypted
    assert not fp.closed


def test_read_bytes():
  data = acd.read_bytes(example_data_encrypted, example_encryption_key)
  assert data == example_data
  encrypted_bytearray = bytearray(example_data_encrypted)
  data = acd.read_bytes(encrypted_bytearray, example_encryption_key)
  assert data == example_data


def test_write_bytes():
  data = acd.write_bytes(example_data, example_encryption_key)
  assert data == example_data_encrypted


def test_read_file():
  with tempfile.TemporaryDirectory() as tmp:
    file = Path(tmp) / 'test'
    with open(file, 'wb') as fp:
      fp.write(example_data_encrypted)
    data = acd.read_file(file)
  assert data == example_data


def test_write_file():
  with tempfile.TemporaryDirectory() as tmp:
    file = Path(tmp) / 'test'
    acd.write_file(example_data, file)
    data = acd.read_file(file)
  assert data == example_data

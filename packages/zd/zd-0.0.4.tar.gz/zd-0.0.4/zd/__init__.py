#!/usr/bin/env python

from zstandard import ZstdCompressor as compressor
from zstandard import ZstdDecompressor as decompressor
from io import TextIOWrapper, RawIOBase

_open = open


class Write:
  def __init__(self, file, encoding, level=10):
    self.encoding = encoding
    self.file = _open(file, "wb")
    self.ctx = compressor(level=level).stream_writer(self.file)

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.close()

  def write(self, text):
    encoding = self.encoding
    if encoding:
      if isinstance(text, str):
        text = text.encode(encoding)
    self.ctx.write(text)

  def close(self):
    self.ctx.close()
    self.file.close()


class ByteIOWrapper:
  def __init__(self, file):
    self.file = file
    self.iter = iter(self)

  def __next__(self):
    return next(self.iter)

  def __iter__(self):
    pre = b""
    while True:
      buf = self.file.read(16384)
      if not buf:
        return pre
      li = (pre + buf).split(b"\n")
      pre = li.pop()
      for i in li:
        yield i


class Read:
  def __init__(self, file, wrap):
    self.file = _open(file, "rb")
    self.ctx = decompressor().stream_reader(self.file)
    self.wrap = wrap

  def __iter__(self):
    return self.wrap(self.ctx)

  def __enter__(self):
    return self

  def __exit__(self, *args):
    self.ctx.close()
    self.file.close()


def open(file, mode='r', encoding="utf-8", level=10):
  if "w" in mode:
    return Write(file, encoding, level)
  if "b" in mode:
    wrap = ByteIOWrapper
  else:
    wrap = lambda ctx: TextIOWrapper(ctx, encoding=encoding)
  return Read(file, wrap)

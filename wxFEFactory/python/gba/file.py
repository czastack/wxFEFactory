class FileRW:
	__slots__ = ('_file', 'addrmask')

	MODE = 'rb'

	def __init__(self, path, addrmask=-1, mode=None):
		self._file = open(path, mode or self.MODE)
		self.addrmask = addrmask

	def close(self):
		self._file.close()

	__del__ = close

	def __getattr__(self, name):
		try:
			return getattr(self._file, name)
		except AttributeError:
			raise

	def pos(self, offset):
		if self.addrmask != -1:
			offset &= self.addrmask
		self._file.seek(offset)
		return self

	def rawRead(self, size):
		return self._file.read(size)

	def read(self, addr, type, size=1):
		return self.pos(addr).rawRead(size)

	def readInt(self, pos, size):
		if pos is not None:
			self.pos(pos)
		return int.from_bytes(self._file.read(size), byteorder='little')

	def read8(self, pos=None):
		return self.readInt(pos, 1)

	def read16(self, pos=None):
		return self.readInt(pos, 2)

	def read32(self, pos=None):
		return self.readInt(pos, 4)

	def rawWrite(self, data):
		return self._file.write(data)

	def write(self, addr, data, size=0):
		if size:
			data = data[:size]
		return self.pos(addr).rawWrite(data)

	def writeInt(self, pos, val, size):
		if val is None:
			val = pos
		elif pos is not None:
			self.pos(pos)
		return self._file.write(val.to_bytes(size, byteorder='little'))

	def write8(self, pos, val=None):
		return self.writeInt(pos, val, 1)

	def write16(self, pos, val=None):
		return self.writeInt(pos, val, 2)

	def write32(self, pos, val=None):
		return self.writeInt(pos, val, 4)

	def patchFile(self, addr, file, offset=0, size=-1):
		with open(file, 'rb') as f:
			if offset:
				f.seek(offset)
			self.write(addr, f.read(size))
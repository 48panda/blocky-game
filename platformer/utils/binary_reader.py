class binaryReader():
    def __init__(self, file):
        self.file = file
    def __open__(self):
        self.fileObj = open(self.file, "rb")
    def read_byte(self):
        return int.from_bytes(self.fileObj.read(1), byteorder='big', signed=True)
    def read_bytes(self, length):
        return int.from_bytes(self.fileObj.read(length), byteorder='big', signed=True)
    def __close__(self):
        self.fileObj.close()
class binaryWriter():
    def __init__(self, file):
        self.file = file
    def __open__(self):
        self.fileObj = open(self.file, "wb")
    def write_byte(self, to_encode):
        self.fileObj.write(to_encode.to_bytes(1, byteorder='big', signed=True))
    def write_bytes(self, to_encode, length):
        self.fileObj.write(to_encode.to_bytes(length, byteorder='big', signed=True))
    def __close__(self):
        self.fileObj.close()
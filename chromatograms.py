from pathlib import Path
import struct


class Chrom:
    def __init__(self, path: Path):
        with open(path / 'AcqData\\MSScan.bin', 'rb') as file:
            self.data = self._decode(file.read())

    def _decode(self, buff: bytes):
        magic_number = 186
        offset = struct.unpack('I', buff[88:92])[0]
        n = len(buff)
        data = []

        if (n - offset) % magic_number == 0:
            nrows = (n - offset) // magic_number
            for i in range(nrows):
                start = offset + magic_number * i
                data.append(self._entry(buff[start:start + magic_number]))

        return data

    def _entry(self, blist: bytes) -> dict:
        d = {'time': struct.unpack('d', blist[12:20])[0],
             'tic': struct.unpack('d', blist[26:34])[0],
             'fragment': struct.unpack('d', blist[34:42])[0],
             'fragmentor': struct.unpack('f', blist[72:76])[0],
             'collision energy': struct.unpack('f', blist[76:80])[0],
             'parent': struct.unpack('d', blist[80:88])[0]}

        return d

    def get_points(self, parent: float, fragment: float, fragmentor: float, ce: float):
        tol = 0.01

        filt = [i for i in self.data if parent - tol <= float(i['parent']) <= parent + tol]
        filt = [i for i in filt if fragment - tol <= float(i['fragment']) <= fragment + tol]
        filt = [i for i in filt if fragmentor == float(i['fragmentor'])]
        filt = [i for i in filt if ce == float(i['collision energy'])]
        filt = [[float(i['time']), float(i['tic'])] for i in filt]

        return filt

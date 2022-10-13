from xml.etree.ElementTree import parse
from pathlib import Path
import struct
from points import Points


class Transition:
    def __init__(self):
        self.name = ''
        self.parent_mass = 0
        self.child_mass = 0
        self.fragmentor = 0
        self.collision_energy = 0
        self.chromatogram = Points()


def main(file: Path):
    vals = {}
    chromatograms = Chromatograms(file)
    path = None
    # Find XML Method file
    method_files = file / 'AcqData'
    for method_file in method_files.iterdir():
        xpath = file / method_file / '192_1.xml'
        if xpath.is_file():
            path = xpath

    # Parse xml data to dictionary 'vals'
    if path:
        x = parse(path)
        root = x.getroot()
        for child in root[10][0][5]:
            for el in child:
                if el.tag == 'scanElements':
                    drug = get_drug_info(el[0])
                    drug.chromatogram = chromatograms.get_points(drug)
                    vals[drug.name, drug.child_mass] = drug

    return vals


def get_drug_info(xml_element):
    drug = Transition()
    for grandchild in xml_element:
        if grandchild.tag == 'compoundName':
            drug.name = grandchild.text

        elif grandchild.tag == 'ms1LowMz':
            drug.parent_mass = float(grandchild.text)

        elif grandchild.tag == 'ms2LowMz':
            drug.child_mass = float(grandchild.text)

        elif grandchild.tag == 'fragmentor':
            drug.fragmentor = float(grandchild.text)

        elif grandchild.tag == 'collisionEnergy':
            drug.collision_energy = float(grandchild.text)

    return drug


class Chromatograms:
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

    def get_points(self, drug: Transition):
        tol = 0.01

        filt = [i for i in self.data if drug.parent_mass - tol <= float(i['parent']) <= drug.parent_mass + tol]
        filt = [i for i in filt if drug.child_mass - tol <= float(i['fragment']) <= drug.child_mass + tol]
        filt = [i for i in filt if drug.fragmentor == float(i['fragmentor'])]
        filt = [i for i in filt if drug.collision_energy == float(i['collision energy'])]
        filt = [[float(i['time']), float(i['tic'])] for i in filt]

        return filt

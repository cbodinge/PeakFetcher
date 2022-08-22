from xml.etree.ElementTree import parse
from pathlib import Path
import points


def get_acq_method(file: Path):
    vals = []
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
                    vals.append(drug)

    return vals


def get_drug_info(xml_element):
    drug = Drug()
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


class Drug:
    def __init__(self):
        self.name = ''
        self.parent_mass = 0
        self.child_mass = 0
        self.fragmentor = 0
        self.collision_energy = 0
        self.chromatogram = points.Points()

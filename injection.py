from pathlib import Path
import method
import chromatograms


class Injection:
    """
    Data Object that organizes the relevant information from a .d file.
    path is a pathlib.Path object that points to the .d Agilent file.
    """

    def __init__(self, path: Path):
        self.path = Path(path)
        self.drugs = method.get_acq_method(path)
        self._set_data()

    def _set_data(self):
        data = chromatograms.Chrom(self.path)
        for drug in self.drugs:
            drug.chromatogram.points = data.get_points(drug.parent_mass,
                                                       drug.child_mass,
                                                       drug.fragmentor,
                                                       drug.collision_energy)

    def get_data(self, drug=None, parent_mass=None, child_mass=None, fragmentor=None, collision_energy=None):
        filt = self.drugs[:]

        if drug is not None:
            filt = [i for i in filt if i.name == drug]

        if parent_mass is not None:
            filt = [i for i in filt if i.parent_mass == parent_mass]

        if child_mass is not None:
            filt = [i for i in filt if i.child_mass == child_mass]

        if fragmentor is not None:
            filt = [i for i in filt if i.fragmentor == fragmentor]

        if collision_energy is not None:
            filt = [i for i in filt if i.collision_energy == collision_energy]

        return filt

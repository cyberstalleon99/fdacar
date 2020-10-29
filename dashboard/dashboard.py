from .myhelpers import Center, Province, Pendings


class MasterlistSummary:

    class Centers(Center):
        pass

    class Provinces:
        Abra = Province('Abra')
        Apayao = Province('Apayao')
        Baguio_City = Province('Baguio City')
        Benguet = Province('Benguet')
        Ifugao = Province('Ifugao')
        Kalinga = Province('Kalinga')
        Mountain_Province = Province('Mountain Province')

    class Pendings(Pendings):
        pass

from .models import Establishment

class EstInstance:
    establishment = ''

    def __init__(self, est):
        self.establishment = est

    def lto_number(self):
        return self.establishment.lto_number
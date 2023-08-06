from docassemble.base.util import Individual

class TRParty(Individual):
    def init(self, *pargs, **kwargs):
        self.initializeAttribute('witness', Individual)
        super().init(*pargs, **kwargs)
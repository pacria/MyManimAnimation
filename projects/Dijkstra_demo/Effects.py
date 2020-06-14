from manimlib.imports import *

class ShowCreationThenFadeOut(Succession):
    CONFIG = {
        "remover": True,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(
            ShowCreation(mobject),
            FadeOut(mobject),
            **kwargs
        )


class SizeOutAndSizeIn(Succession):
    CONFIG = {
        "amp":1.3,
        "during_time":1,
        "ratio":.35
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs)
        super().__init__(
            ApplyMethod(mobject.scale, self.amp, run_time=self.during_time*self.ratio),
            ApplyMethod(mobject.scale, 1/self.amp, run_time=self.during_time*(1-self.ratio)),
            **kwargs
        )
class SchedTalks(object):
    def __init__(self, **kwargs):
        """Load settings"""

        self.settings = {
            'output_dir': 'files',
            **kwargs,
        }

        self.talks = []
    pass
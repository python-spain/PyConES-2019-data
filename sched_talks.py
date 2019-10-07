import os
class SchedTalks(object):
    def __init__(self, **kwargs):
        """Load settings and prepare paths"""

        self.settings = {
            'output_dir': 'files',
            **kwargs,
        }

        self.talks = []
        
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            pass



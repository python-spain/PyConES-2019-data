import os
class SchedTalks(object):
    def __init__(self, **kwargs):
        """Load settings, prepare paths and get talks"""

        self.settings = {
            'output_dir': 'files',
            **kwargs,
        }

        self.talks = []
        
        try:
            os.mkdir(self.output_dir)
        except FileExistsError:
            pass

        self._get_talks()

    def _get_talks(self):
        """Load talks file and process it downloading associated files"""
        with open('talks.json') as f:
            self.json = json.load(f)

        for talk in tqdm(self.json, desc='Processing talks'):
            self.talks.append(talk)

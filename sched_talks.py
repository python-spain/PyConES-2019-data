import os
import json
import requests
from tqdm import tqdm

class SchedTalks(object):
    __slots__ = ['json', 'talks', 'settings']

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

    @property
    def as_md(self):
        """
        Render talks as a MD string

        It skips non real talks i.e Coffe breaks, lunchs and other similar entries 
        based on the speaker definition.
        """

        talks_content = ''
        for talk in tqdm(self.talks, desc='Converting to MD'):
            speakers = [speaker.get('name', 'Unknown')
                        for speaker in talk.get('speakers', [])]

            # Skip unnamed talks (coffee break, lunch, ...)
            if not speakers:
                continue

            speakers_formated = ", ".join(speakers)
            talk_md = f"\n- **'{talk.get('name')}'** by _{speakers_formated}_"

            attachments = talk.get('attachments')
            if attachments:
                talk_md += ''.join([
                    f'\n  - [{attachment.get("file_name")}]({attachment.get("file_path")})'
                    for attachment in attachments
                ])
            
            talks_content += talk_md

        return talks_content
     
    @property
    def output_dir(self):
        return self.settings.get('output_dir')

    def _get_talks(self):
        """Load talks file and process it downloading associated files"""
        with open('talks.json') as f:
            self.json = json.load(f)

        for talk in tqdm(self.json, desc='Processing talks'):
            # Process attachments
            attachments = talk.get('files', [])
            if attachments:
                attachments_resolved = self._download_attachments(
                    attachments
                )
                talk['attachments'] = attachments_resolved

            self.talks.append(talk)

    def _download_attachments(self, attachments, destination_path=None):
        """Helper to download and save files"""

        result = []
        for attachment in attachments:
            file_url = attachment.get('path')
            file_name = attachment.get('name')

            if not file_name:
                import pudb; pu.db

            file_path_local = os.path.join(
                destination_path or self.output_dir,
                file_name
            )
            get_response = requests.get(file_url, stream=True)
            with open(file_path_local, 'wb') as f:
                for chunk in get_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            result.append({
                'file_url': file_url,
                'file_path': file_path_local,
                'file_name': file_name,
            })

        return result

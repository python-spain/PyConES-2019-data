import os
import json
import requests
from tqdm import tqdm
from slugify import slugify

def _mkdir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError:
        pass

class SchedTalks(object):
    __slots__ = ['json', 'talks', 'settings']

    def __init__(self, **kwargs):
        """Load settings, prepare paths and get talks"""

        self.settings = {
            'output_dir': 'files',
            'api_key': os.environ.get('SCHED_API_KEY', os.environ.get('SCHED_KEY')),
            **kwargs,
        }

        self.talks = []
        
        _mkdir(self.output_dir)

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

    @property
    def api_key(self):
        return self.settings.get('api_key')

    def _get_talks(self):
        """Load talks file and process it downloading associated files"""

        talks_response = requests.get(
            f'https://pycones19.sched.com/api/session/export?api_key={self.api_key}&format=json&strip_html=Y&fields=id,files,name,speakers,event_start'
        )

        if talks_response:
            try:
                self.json = json.loads(talks_response.content)
            except:
                raise Exception(f"Sched Talks can't be correctly retrieved: '{talks_response.content}")

        for talk in tqdm(self.json, desc='Processing talks'):
            # Process attachments
            attachments = talk.get('files', [])
            if attachments:
                # Prepare isolated talk paths
                talk_path = os.path.join(
                    self.output_dir,
                    slugify(talk.get('name'))
                )
                _mkdir(talk_path)

                attachments_resolved = self._download_attachments(
                    attachments,
                    destination_path=talk_path,
                )
                talk['attachments'] = attachments_resolved

            self.talks.append(talk)

    def _download_attachments(self, attachments, destination_path=None):
        """Helper to download and save files"""

        result = []
        for attachment in attachments:
            file_url = attachment.get('path')
            file_name = attachment.get('name')

            # Clean file name with slugify strategy
            cleaned_file_name, file_extension = os.path.splitext(file_name)
            file_path_local = os.path.join(
                destination_path or self.output_dir,
                f'{slugify(cleaned_file_name)}{file_extension}',
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

    def export_md(self, file_name="README.md"):
        """Export as md file"""

        with open(file_name, "w") as readme:
            readme.write(self.as_md)


if __name__ == "__main__":
    talks = SchedTalks(output_dir='files')
    talks.export_md(file_name='README.md')

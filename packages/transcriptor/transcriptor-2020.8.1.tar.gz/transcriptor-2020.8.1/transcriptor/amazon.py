from .job import Job
from .markers import Marker
from .speakers import Speaker
from .alternatives import Alternative

from datetime import timedelta
from pathlib import Path
from slugify import slugify

import boto3
import more_itertools
import requests
import logging
import os
import typing

storage = boto3.client('s3')
transcribe = boto3.client('transcribe')

class Amazon(Job):
    def __init__(
            self,
            key: typing.Optional[str] = '',
            bucket = os.environ.get('BUCKET_NAME', None),
            status = typing.Optional['None'],
            ):

        self.bucket = bucket

        if key:
            self.key = self.set_key(key)
            self.filename = Path(key)

        else:
            self.key = ''

        if status:
            self._status = status

        else:
            self._status = 'NOT STARTED'


    def set_key(self, path_name:str):
        valid_keytypes = ['.mp3', '.mp4', '.wav', '.flac']
        path = Path(path_name)
        path_suffix =  path.suffix

        if path_suffix.lower() not in valid_keytypes:
            msg = "The file that you entered is not a valid filetype. You \
may experience issues with submitting a transcription."
            logging.warning(msg)

        slug_path = slugify(str(path).split(path_suffix)[0])
        return slug_path + path_suffix

    @property
    def status(self):
        if self._status:
            return self._status

        job = transcribe.get_transcription_job(TranscriptionJobName=self.key)
        status = job['TranscriptionJob']['TranscriptionJobStatus']

        if status != 'IN_PROGESS':
            self._status = status

        return status

    def upload_audio_file(self, filename):
        """Loads file to amazon s3 location"""
        return storage.upload_file(str(self.filename), Bucket=self.bucket,
                Key=self.key)

    def start(self,
        language: str='en-US',
        speakers: int=0,
        storage=storage,
        transcribe=transcribe,
        ):

        audio_file = self.upload_audio_file(self.filename)

        transcribe_job_uri = f"{storage.meta.endpoint_url}/{self.bucket}/{self.key}"
        print(transcribe_job_uri)

        if speakers:
            settings = {
                "ShowSpeakerLabels": True,
                "MaxSpeakerLabels": speakers,
                }
        else:
            settings = {}

        transcribe.start_transcription_job(
            TranscriptionJobName=self.key,
            Media={"MediaFileUri": transcribe_job_uri},
            MediaFormat=Path(self.filename).suffix[1:],
            LanguageCode=language,
            Settings=settings,
        )

        # reset status so that it will check for it
        self._status = ''
        return self.status

## Download Jobs
def text_in_range(segments, start_time, end_time):
    content = ''
    in_range = False

    for index, segment in enumerate(segments):
        if segment['type'] == 'punctuation':

            if in_range == True:
                content += segment['alternatives'][0]['content']

            else:
                continue

        elif float(segment['end_time']) <= float(end_time):

            if float(segment['start_time']) >= float(start_time):
                in_range = True
                content += " " + segment['alternatives'][0]['content']

        else:
            return content.strip()


def add_speaker(speaker_index: int) -> Speaker:
    """Create a speaker object from one of the labels in results['speaker_labels']"""
    return Speaker(
            base_name=f'spk_{speaker_index}',
            )


def from_job(job_name: str) -> Job:
    """Create a Job Object based on the TranscriptiobJobName"""
    job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    return from_uri(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])


def from_uri(uri) -> Job:
    """Create a Job Object based on the TranscriptFileUri"""
    response = requests.get(uri)
    response.raise_for_status()

    return from_json(response.json())


def from_json(transcription) -> Job:
    """Create a Job Object when given an Amazon JSON Object"""
    markers = []
    segments = transcription['results']['items']

    if 'speaker_labels' in transcription['results']:
        labels = transcription['results']['speaker_labels']
        speakers = [add_speaker(x) for x in range(labels['speakers'])]

        for segment in labels['segments']:
            start_time=segment['start_time']
            end_time=segment['end_time']
            speaker=[x for x in speakers if x.base_name == segment['speaker_label']][0]
            content = text_in_range(
                    segments,
                    start_time=start_time,
                    end_time=end_time,
                    )
            marker = Marker(
                    start_time = timedelta(seconds=float(start_time)),
                    end_time = timedelta(seconds=float(end_time)),
                    content = content,
                    speaker = speaker
                    )
            markers.append(marker)

    else:
        speakers = []

        items_segments = more_itertools.split_when(
            segments, lambda x,y: x['alternatives'][0]['content'] in ['.', '?', '!'],
        )

        for index, item in enumerate(items_segments):
            start_time = timedelta(seconds=float(item[0]['start_time']))
            end_time = timedelta(seconds=float(item[-2]['end_time']))
            content = ''

            for word_block in item:
                if word_block['type'] == 'punctuation':
                    content += word_block['alternatives'][0]['content']
                else:
                    content += " " + word_block['alternatives'][0]['content']

            marker = Marker(start_time=start_time, end_time=end_time,
                    content=content)
            markers.append(marker)

    # add alternatives
    alternatives = []
    for item in segments:

        if item['type'] == 'pronunciation':

            for alt in item['alternatives']:
                alternatives.append(Alternative(
                    start_time = item['start_time'],
                    content = alt['content'],
                    confidence = alt['confidence'],
                    tag = 'orignal',
                    _type = 'pronunciation',
                    ))

    return Job.from_amazon(
            base_text = transcription['results']['transcripts'][0]['transcript'],
            name = transcription['jobName'],
            transcription=transcription,
            speakers = speakers,
            markers = markers,
            alternatives = alternatives,
            )

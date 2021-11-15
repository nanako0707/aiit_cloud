import contextlib
import pprint
import time
import uuid

import boto3
from playsound import playsound

txt_ja = '前期はボロボロだったので、後期は頑張ります！！'


def translateFnc():
    t_obj = boto3.client('translate')

    t_out = t_obj.translate_text(
        Text=txt_ja,
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )

    global txt_en
    txt_en = t_out['TranslatedText']


def pollyFnc():
    p_obj = boto3.client('polly')

    p_out = p_obj.synthesize_speech(
        Text=txt_en,
        OutputFormat='mp3',
        VoiceId='Ivy'
    )

    f_out = 's_out.mp3'
    with contextlib.closing(p_out['AudioStream']) as a_stream:
        with open(f_out, 'wb') as f:
            f.write(a_stream.read())

    playsound(f_out)


def transcribeFnc():
    f_name = 's_out.mp3'
    k_name = 's_out.mp3'
    b_name = 'data.nanako21745113.com'

    s3_obj = boto3.resource('s3')
    b_obj = s3_obj.Bucket(b_name)
    b_obj.upload_file(f_name, k_name)

    t_obj = boto3.client('transcribe', 'ap-northeast-1')

    jobID = str(uuid.uuid1())
    t_out = t_obj.start_transcription_job(
        TranscriptionJobName=jobID,
        Media={'MediaFileUri': 's3://' + b_name + '/' + f_name},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    pprint.pprint(t_out)

    while True:
        t_out = t_obj.get_transcription_job(TranscriptionJobName=jobID)
        status = t_out['TranscriptionJob']['TranscriptionJobStatus']
        if status != 'IN_PROGRESS':
            break
        time.sleep(5)
    print(status)
    pprint.pprint(t_out)


if __name__ == "__main__":
    translateFnc()
    pollyFnc()
    transcribeFnc()

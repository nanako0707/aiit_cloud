import boto3
import contextlib
from playsound import playsound

t_obj = boto3.client('translate')
p_obj = boto3.client('polly')

txt_ja = '産技大の授業は非常にためになる。'
t_out = t_obj.translate_text(
  Text=txt_ja,
  SourceLanguageCode='ja',
  TargetLanguageCode='en'
)

txt_en = t_out['TranslatedText']

p_out = p_obj.synthesize_speech(
  Text=txt_en,
  OutputFormat='mp3',
  VoiceId='Matthew'
)

f_out = 's_out2.mp3'
with contextlib.closing(p_out['AudioStream']) as a_stream:
  with open(f_out, 'wb') as f:
    f.write(a_stream.read())

playsound(f_out)

import boto3
import contextlib
from playsound import playsound

text = '音声合成のテストです。うまくいきましたか？'
f_out = 's_out.mp3'

p_obj = boto3.client('polly')
p_out = p_obj.synthesize_speech(
	Text=text,
	OutputFormat='mp3',
	# VoiceId='Takumi'
	VoiceId='Mizuki'
)

with contextlib.closing(p_out['AudioStream']) as a_stream:
	with open(f_out, 'wb') as file:
		file.write(a_stream.read())

playsound(f_out)

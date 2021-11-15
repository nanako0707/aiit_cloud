import boto3
import json
from PIL import Image
from PIL import ImageDraw

f_img = 'test.jpg'
in_img = Image.open(f_img)
w, h = in_img.size
textcolor = 'lime'

r_obj = boto3.client('rekognition')
with open(f_img, 'rb') as file:
  r_out = r_obj.detect_faces(
    Image={'Bytes': file.read()},
    Attributes=['ALL']
  )
  print(json.dumps(r_out, indent=2))

draw = ImageDraw.Draw(in_img)

out_img = Image.new('RGB', (w, h), (256, 256, 256))
for face in r_out['FaceDetails']:
    box = face['BoundingBox']
    left = int(box['Left']*w)
    top = int(box['Top']*h)
    width = int(box['Width']*w)
    height = int(box['Height']*h)
    text_place = (left, top - 14)
    emotions = face['Emotions'][0]
    type = str(emotions['Type'])
    confidence = int(emotions['Confidence'])
    text = type + ':' + str(confidence)
    landmarks = face['Landmarks']

    for landmark in landmarks:
        x = int(landmark['X'] * w)
        y = int(landmark['Y'] * h)
        draw.ellipse((x, y, x + 2, y + 2), fill='white', outline='white')

    draw.rectangle([(left, top), (left+width, top+height)], outline='lime', width=2)
    draw.text(text_place, text, textcolor)

in_img.save('show_' + f_img)
in_img.show()

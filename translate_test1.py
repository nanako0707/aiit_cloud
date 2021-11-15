import boto3

txt_ja = '前期はボロボロだったので、後期は頑張ります！！'

def translateFnc():
  t_obj = boto3.client('translate')

  t_out = t_obj.translate_text(
    Text=txt_ja,
    SourceLanguageCode='ja',
    TargetLanguageCode='en'
  )

  print(t_out)
  print(t_out['TranslatedText'])

if __name__ == "__main__":
  translateFnc()


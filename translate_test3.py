import boto3

t_obj = boto3.client('translate')

with open('f_input.txt', 'r', encoding='utf-8') as f_in:
	with open('f_output.txt', 'w', encoding='utf-8') as f_out:
		for txt in f_in:
			if txt != '\n':
				t_out = t_obj.translate_text(
					Text=txt,
					SourceLanguageCode='ja',
					TargetLanguageCode='en'
				)
			f_out.write(t_out['TranslatedText'])
			f_out.write('\n')

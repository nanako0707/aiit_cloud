import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.resource('s3')
sns_obj = boto3.resource('sns')
b_output = 'output.nanako21745113.com'


def lambda_handler(event, context):
    b_input = event['Records'][0]['s3']['bucket']['name']
    f_input = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        bucket = s3.Bucket(b_input)
        b_obj = bucket.Object(f_input)

        response = b_obj.get()
        txt_input = response['Body'].read().decode('utf-8')
        txt_list = txt_input.split()

        # Translate を使用し、日本語を英語に翻訳する
        t_obj = boto3.client('translate')
        txt_list_output = []
        for txt_ja in txt_list:
            t_out = t_obj.translate_text(
                Text=txt_ja,
                SourceLanguageCode='ja',
                TargetLanguageCode='en',
            )
            txt_list_output.append(t_out['TranslatedText'])

        f_output = 'translate_' + f_input
        bucket_out = s3.Bucket(b_output)
        b_out_obj = bucket_out.Object(f_output)

        txt_out = '\n'.join(txt_list_output)

        # 英語に翻訳されたテキストを出力用のバケットに格納
        b_out_obj.put(Body=txt_out)

        # SNS を使用し、メールでメッセージを送信
        sns_obj.Topic('arn:aws:sns:ap-northeast-1:601230306569:SNS_Test_21745113').publish(
            Message=f"Translation complete. input file name: {f_input}, output file name: {f_output}.",
            Subject='Lambda_s3_21745113 Execution result'
        )

        return print('Translation complete. input file name: {}, output file name: {}. '.format(f_input, f_output))
    except Exception as e:
        print(e)
        print('Translation failed')
        raise e

import json
import os
import boto3
import logging
from datetime import date

def _get_ses_client():
    return boto3.client('ses')

def _calculate_pnl(data):
    try:
        chg = [d.get('PNL', 0) for d in data]
        return sum(chg)
    except Exception as e:
        raise Exception(f'Exceptioni n calculate pnl. got:\n{data}')

def generate_email(body):
    receiver  = os.environ.get('RECIPIENT')
    logging.info(f'---- sending ot {receiver}')
    
    try:
        jsondict = json.loads(body['body'])
        alldata = jsondict['data']
        diffs = _calculate_pnl(alldata)
    except Exception as e:
        raise Exception(f'eException in genearte email:{str(e)}\n {body}')
    body_html = f"""<html>
        <head></head>
        <body>
         <p> Portfolio Summary for Today . Changes: {diffs}</p>
         <hr>
         
         <table>
        """
    body_html += "<tr><th>TICKER</th><th>QTY</th><th>CLOSE</th><th>POSITION</th><th>PNL</th></tr>"
    template = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>"
    for data in alldata:
        if alldata.get('QTY', 0) > 1:
            formatted = template.format(data['TICKER'], data['QTY'], data['CLOSE'], data['POSITION'], data['PNL'])        
            body_html += formatted
     
    body_html += "</table></body></html>" 
     
    email_message = {
        'Body': {
            'Html': {
                'Charset': 'utf-8',
                'Data': body_html,
            },
        },
        'Subject': {
            'Charset': 'utf-8',
            'Data': f"Portfolio Change for {date.today().strftime('%Y-%m-%d')} = {diffs}",
        },
    }

    logging.info(f'Bodyhtml:{body_html}')

    client = _get_ses_client()

    ses_response = client.send_email(
        Destination={
            'ToAddresses': ['mmistroni@gmail.com'],
        },
        Message=email_message,
        Source="mmistroni@gmail.com"
    )

    print(f"ses response id received: {ses_response['MessageId']}.")
    return ses_response['MessageId']

    
def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    logging.info(f'Got body:{event}')
    result = ''
    try :
        result = generate_email(event)
    except Exception as e:
        result = f'Exception in generating data:{str(e)}'


    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": result,
            }
        ),
    }

import json
import logging

import requests
import os

def get_fmpkey():
    logging.info(os.environ)
    return os.environ.get('FMPREPKEY', ' ')

def get_quote_for_ticker(ticker:str)-> dict:
    key = get_fmpkey()
    stat_url = f'https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={key}'
    return requests.get(stat_url).json()[0]
    
def populate_with_prices(ticker_dict:dict) -> dict :
    res_dict = ticker_dict.copy()
        
    try:
        data = get_quote_for_ticker(res_dict['TICKER'])    
        res_dict['CLOSE'] = data['price']
        res_dict['ORIGINAL_POSITION'] = res_dict['QTY'] * res_dict['PRICE']
        res_dict['POSITION'] = res_dict['QTY'] * res_dict['CLOSE']
        res_dict['PNL'] = res_dict['POSITION'] - res_dict['ORIGINAL_POSITION']
        return res_dict
    except Exception as e:
        logging.info(f'Error in fetching {ticker_dict}:{str(e)}')
        return res_dict

def _filter_valid_shares(rqst):
    logging.info('---- inputs---')
    if 'body' in rqst:
        rqst = rqst['body']
    return [d for d in rqst if d['QTY'] > 1]

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
    #https://www.youtube.com/watch?v=mhdX4znMd2Q&ab_channel=JonathanDavies
    #https://codeolives.com/2020/01/02/vs-code-with-python-aws-lambda-a-complete-tutorial-to-develop-and-deploy-python-lambda-functions-using-vs-code-part-2/

    
    logging.info(f'Received:{event}')
    
    
    valid_shares = _filter_valid_shares(event)
    
    
    
    ptfchanges = [populate_with_prices(d) for d in valid_shares]
    
    changes = sum([d.get('PNL', -1) for d in ptfchanges])
    
    result = dict(data=ptfchanges, ptfchange=changes, statusCode=200)
    
    
    return {
        "statusCode": 200,
        "body": json.dumps(
            result
        )
    }

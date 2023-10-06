import json


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

    valid_shares = ['AMZN', 'AAPL', 'MSFT', 'NFLX']


    return {
        "statusCode": 200,
        "body": json.dumps(
            valid_shares
        ),
    }

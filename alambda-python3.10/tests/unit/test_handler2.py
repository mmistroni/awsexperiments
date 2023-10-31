import json

import pytest

from hello_world import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "body": '{ "ptfchange": 100}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_lambda_handler(apigw_event, mocker):
    retmsg = 'success11'
    mocker.patch('hello_world.app.generate_email', return_value=retmsg)
    
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == retmsg

def test_generate_email(mocker):
    stub = mocker.Mock(name='ses client')
    stub.send_email.return_value = {'MessageId'  :1}

    mocker.patch('hello_world.app._get_ses_client', return_value=stub)
    
    input_data = {
  "statusCode": 200,
  "body": "{\"data\": [{\"TICKER\": \"AAPL\", \"NAME\": \"Apple Inc\", \"QTY\": 64, \"PRICE\": 66.33, \"CLOSE\": 170.29, \"ORIGINAL_POSITION\": 4245.12, \"POSITION\": 10898.56, \"PNL\": 6653.44}, {\"TICKER\": \"ACBFF\", \"NAME\": \"Aurora Cannabis\", \"QTY\": 200, \"PRICE\": 6.28}, {\"TICKER\": \"ADAC \", \"NAME\": \"ADAMA TECHNOLOGIES\", \"QTY\": 62000, \"PRICE\": 0.0025}, {\"TICKER\": \"AGEEF\", \"NAME\": \"HALO LABS INC\", \"QTY\": 4000, \"PRICE\": 0.5, \"CLOSE\": 15.2, \"ORIGINAL_POSITION\": 2000.0, \"POSITION\": 60800.0, \"PNL\": 58800.0}, {\"TICKER\": \"AMBS\", \"NAME\": \"AMARANTUS BIOSCIENCE\", \"QTY\": 4000, \"PRICE\": 0.0490375, \"CLOSE\": 0.0007, \"ORIGINAL_POSITION\": 196.14999999999998, \"POSITION\": 2.8, \"PNL\": -193.34999999999997}, {\"TICKER\": \"AMZN\", \"NAME\": \"Amazon\", \"QTY\": 8, \"PRICE\": 1384.27, \"CLOSE\": 132.71, \"ORIGINAL_POSITION\": 11074.16, \"POSITION\": 1061.68, \"PNL\": -10012.48}, {\"TICKER\": \"APTY\", \"NAME\": \"APTSYSTEMINC\", \"QTY\": 70000, \"PRICE\": 0.0004, \"CLOSE\": 0.00085, \"ORIGINAL_POSITION\": 28.0, \"POSITION\": 59.5, \"PNL\": 31.5}, {\"TICKER\": \"ARSC\", \"NAME\": \"AmericanSec Res\", \"QTY\": 600, \"PRICE\": 1.24825, \"CLOSE\": 0.0001, \"ORIGINAL_POSITION\": 748.95, \"POSITION\": 0.060000000000000005, \"PNL\": -748.8900000000001}, {\"TICKER\": \"AZFL\", \"NAME\": \"AMAZONAS FLORESTAL\", \"QTY\": 999999, \"PRICE\": 0.0001, \"CLOSE\": 1e-06, \"ORIGINAL_POSITION\": 99.99990000000001, \"POSITION\": 0.999999, \"PNL\": -98.99990100000001}, {\"TICKER\": \"BAC\", \"NAME\": \"Bank of america\", \"QTY\": 100, \"PRICE\": 30.94, \"CLOSE\": 25.69, \"ORIGINAL_POSITION\": 3094.0, \"POSITION\": 2569.0, \"PNL\": -525.0}, {\"TICKER\": \"BRK.B\", \"NAME\": \"BERKSHIRE HATAWAY\", \"QTY\": 45, \"PRICE\": 64.108}, {\"TICKER\": \"BTCS\", \"NAME\": \"BT CS\", \"QTY\": 278, \"PRICE\": 0.117, \"CLOSE\": 0.91, \"ORIGINAL_POSITION\": 32.526, \"POSITION\": 252.98000000000002, \"PNL\": 220.454}, {\"TICKER\": \"CRNT\", \"NAME\": \"CERAGON NETWORKS\", \"QTY\": 1000, \"PRICE\": 2.9, \"CLOSE\": 1.67, \"ORIGINAL_POSITION\": 2900.0, \"POSITION\": 1670.0, \"PNL\": -1230.0}, {\"TICKER\": \"DGP\", \"NAME\": \"DB Gold Double LOng\", \"QTY\": 50, \"PRICE\": 27.68, \"CLOSE\": 41.4996, \"ORIGINAL_POSITION\": 1384.0, \"POSITION\": 2074.98, \"PNL\": 690.98}, {\"TICKER\": \"ENPH\", \"NAME\": \"ENphase Energy\", \"QTY\": 200, \"PRICE\": 7.014, \"CLOSE\": 78.66, \"ORIGINAL_POSITION\": 1402.8, \"POSITION\": 15732.0, \"PNL\": 14329.2}, {\"TICKER\": \"HAON\", \"NAME\": \"Halitron Inc\", \"QTY\": 999999, \"PRICE\": 0.000104950105, \"CLOSE\": 1e-06, \"ORIGINAL_POSITION\": 104.95000004989501, \"POSITION\": 0.999999, \"PNL\": -103.95000104989501}, {\"TICKER\": \"HMNY\", \"NAME\": \"HELIOS  MATHESON\", \"QTY\": 4, \"PRICE\": 0.0025, \"CLOSE\": 1e-06, \"ORIGINAL_POSITION\": 0.01, \"POSITION\": 4e-06, \"PNL\": -0.009996}, {\"TICKER\": \"INDOY \", \"NAME\": \"INDOY \", \"QTY\": 150, \"PRICE\": 18.08, \"CLOSE\": 6.635, \"ORIGINAL_POSITION\": 2711.9999999999995, \"POSITION\": 995.25, \"PNL\": -1716.7499999999995}, {\"TICKER\": \"JNJ\", \"NAME\": \"JohnsonJohnson\", \"QTY\": 40, \"PRICE\": 129.12375, \"CLOSE\": 147.03, \"ORIGINAL_POSITION\": 5164.95, \"POSITION\": 5881.2, \"PNL\": 716.25}, {\"TICKER\": \"LEMIF\", \"NAME\": \"LEADING EDGE MAT\", \"QTY\": 2000, \"PRICE\": 0.1297, \"CLOSE\": 0.11, \"ORIGINAL_POSITION\": 259.40000000000003, \"POSITION\": 220.0, \"PNL\": -39.400000000000034}, {\"TICKER\": \"MCD\", \"NAME\": \"MCDONALDS CORP\", \"QTY\": 42, \"PRICE\": 88.016, \"CLOSE\": 260.15, \"ORIGINAL_POSITION\": 3696.672, \"POSITION\": 10926.3, \"PNL\": 7229.627999999999}, {\"TICKER\": \"NFLX\", \"NAME\": \"Netflix\", \"QTY\": 51, \"PRICE\": 58.594, \"CLOSE\": 410.08, \"ORIGINAL_POSITION\": 2988.294, \"POSITION\": 20914.079999999998, \"PNL\": 17925.786}, {\"TICKER\": \"NVCN\", \"NAME\": \"NEOVAS INC\", \"QTY\": 200, \"PRICE\": 3.0, \"CLOSE\": 30.03, \"ORIGINAL_POSITION\": 600.0, \"POSITION\": 6006.0, \"PNL\": 5406.0}, {\"TICKER\": \"NXTTF\", \"NAME\": \"NAMASTE TECHNOLOGIES\", \"QTY\": 900, \"PRICE\": 0.6449, \"CLOSE\": 0.0371, \"ORIGINAL_POSITION\": 580.4100000000001, \"POSITION\": 33.39, \"PNL\": -547.0200000000001}, {\"TICKER\": \"PTNR\", \"NAME\": \"PARTNER COMMUNICATION\", \"QTY\": 300, \"PRICE\": 3.89, \"CLOSE\": 6.61, \"ORIGINAL_POSITION\": 1167.0, \"POSITION\": 1983.0, \"PNL\": 816.0}, {\"TICKER\": \"REMX\", \"NAME\": \"RARE EARTH\", \"QTY\": 200, \"PRICE\": 14.84, \"CLOSE\": 57.52, \"ORIGINAL_POSITION\": 2968.0, \"POSITION\": 11504.0, \"PNL\": 8536.0}, {\"TICKER\": \"RNVA\", \"NAME\": \"RENNOVA HEALTH\", \"QTY\": 50060, \"PRICE\": 0.00389, \"CLOSE\": 1e-06, \"ORIGINAL_POSITION\": 194.7334, \"POSITION\": 0.05006, \"PNL\": -194.68334}, {\"TICKER\": \"TORC\", \"NAME\": \"RESTORBIO INC\", \"QTY\": 400, \"PRICE\": 7.5}, {\"TICKER\": \"TVIX\", \"NAME\": \"TVIX\", \"QTY\": 8, \"PRICE\": 971.394, \"CLOSE\": 112.36, \"ORIGINAL_POSITION\": 7771.152, \"POSITION\": 898.88, \"PNL\": -6872.272}, {\"TICKER\": \"VALE\", \"NAME\": \"COMPANHIA VALE DO RIO DOCE\", \"QTY\": 2, \"PRICE\": 20.774, \"CLOSE\": 13.52, \"ORIGINAL_POSITION\": 41.548, \"POSITION\": 27.04, \"PNL\": -14.508000000000003}, {\"TICKER\": \"VZ\", \"NAME\": \"VERIZON COMM.\", \"QTY\": 135, \"PRICE\": 58.07, \"CLOSE\": 34.62, \"ORIGINAL_POSITION\": 7839.45, \"POSITION\": 4673.7, \"PNL\": -3165.75}], \"ptfchange\": 95888.17476195013}",
  "request": [
    {
      "TICKER": "000001.SS",
      "NAME": "Shanghai Composite",
      "QTY": 1,
      "PRICE": 2059.15
    },
    {
      "TICKER": "2836.HK",
      "NAME": "SENSEX ETF",
      "QTY": 1,
      "PRICE": 14.4
    },
    {
      "TICKER": "AAPL",
      "NAME": "Apple Inc",
      "QTY": 64,
      "PRICE": 66.33
    },
    {
      "TICKER": "ACBFF",
      "NAME": "Aurora Cannabis",
      "QTY": 200,
      "PRICE": 6.28
    },
    {
      "TICKER": "ADAC ",
      "NAME": "ADAMA TECHNOLOGIES",
      "QTY": 62000,
      "PRICE": 0.0025
    },
    {
      "TICKER": "AGEEF",
      "NAME": "HALO LABS INC",
      "QTY": 4000,
      "PRICE": 0.5
    },
    {
      "TICKER": "AMBS",
      "NAME": "AMARANTUS BIOSCIENCE",
      "QTY": 4000,
      "PRICE": 0.0490375
    },
    {
      "TICKER": "AMZN",
      "NAME": "Amazon",
      "QTY": 8,
      "PRICE": 1384.27
    },
    {
      "TICKER": "APTY",
      "NAME": "APTSYSTEMINC",
      "QTY": 70000,
      "PRICE": 0.0004
    },
    {
      "TICKER": "ARSC",
      "NAME": "AmericanSec Res",
      "QTY": 600,
      "PRICE": 1.24825
    },
    {
      "TICKER": "AUDEUR=X",
      "NAME": "AUDEUR",
      "QTY": 1,
      "PRICE": 0.7221
    },
    {
      "TICKER": "AUDGBP=X",
      "NAME": "AUDGBP",
      "QTY": 1,
      "PRICE": 0.6204
    },
    {
      "TICKER": "AUDUSD=X",
      "NAME": "AUDUSD",
      "QTY": 1,
      "PRICE": 0.9671
    },
    {
      "TICKER": "AZFL",
      "NAME": "AMAZONAS FLORESTAL",
      "QTY": 999999,
      "PRICE": 0.0001
    },
    {
      "TICKER": "BAC",
      "NAME": "Bank of america",
      "QTY": 100,
      "PRICE": 30.94
    },
    {
      "TICKER": "BRK.B",
      "NAME": "BERKSHIRE HATAWAY",
      "QTY": 45,
      "PRICE": 64.108
    },
    {
      "TICKER": "BTCS",
      "NAME": "BT CS",
      "QTY": 278,
      "PRICE": 0.117
    },
    {
      "TICKER": "CHFEUR=X",
      "NAME": "CHFEUR",
      "QTY": 1,
      "PRICE": 0.8326
    },
    {
      "TICKER": "CRBQ",
      "NAME": "Jefferies Global Comm.",
      "QTY": 1,
      "PRICE": 49.3
    },
    {
      "TICKER": "CRNT",
      "NAME": "CERAGON NETWORKS",
      "QTY": 1000,
      "PRICE": 2.9
    },
    {
      "TICKER": "DGP",
      "NAME": "DB Gold Double LOng",
      "QTY": 50,
      "PRICE": 27.68
    },
    {
      "TICKER": "DIA",
      "NAME": "SPDR DJ Ind Avg",
      "QTY": 1,
      "PRICE": 124.11
    },
    {
      "TICKER": "DJP",
      "NAME": "DJ UBS Commodity",
      "QTY": 1,
      "PRICE": 43.16
    },
    {
      "TICKER": "DZZ",
      "NAME": "Gold Double Short",
      "QTY": 1,
      "PRICE": 4.65
    },
    {
      "TICKER": "EE0003M:IND",
      "NAME": "LIBOR",
      "QTY": 1,
      "PRICE": 1.42
    },
    {
      "TICKER": "EEM",
      "NAME": "Em. Markets ETF",
      "QTY": 1,
      "PRICE": 39.65
    },
    {
      "TICKER": "ENPH",
      "NAME": "ENphase Energy",
      "QTY": 200,
      "PRICE": 7.014
    },
    {
      "TICKER": "EUR003M:IND",
      "NAME": "EURIBOR",
      "QTY": 1,
      "PRICE": 1.46
    },
    {
      "TICKER": "EURCHF=X",
      "NAME": "EURCHF",
      "QTY": 1,
      "PRICE": 1.2148
    },
    {
      "TICKER": "EURUSD=X",
      "NAME": "EURUSD",
      "QTY": 1,
      "PRICE": 1.2466
    },
    {
      "TICKER": "FXA",
      "NAME": "AUD Trust",
      "QTY": 1,
      "PRICE": 105.21
    },
    {
      "TICKER": "GBPCHF=X",
      "NAME": "GBPCHF",
      "QTY": 1,
      "PRICE": 1.4136
    },
    {
      "TICKER": "GBPEUR=X",
      "NAME": "GBPEUR",
      "QTY": 1,
      "PRICE": 1.1636
    },
    {
      "TICKER": "GBPUSD=X",
      "NAME": "GBPUSD",
      "QTY": 1,
      "PRICE": 1.5588
    },
    {
      "TICKER": "GLD",
      "NAME": "Gold Spot Price",
      "QTY": 1,
      "PRICE": 164.08
    },
    {
      "TICKER": "GLL",
      "NAME": "ProShares UltraShort Gold ",
      "QTY": 1,
      "PRICE": 60
    },
    {
      "TICKER": "HAON",
      "NAME": "Halitron Inc",
      "QTY": 999999,
      "PRICE": 0.000104950105
    },
    {
      "TICKER": "HMNY",
      "NAME": "HELIOS  MATHESON",
      "QTY": 4,
      "PRICE": 0.0025
    },
    {
      "TICKER": "INDOY ",
      "NAME": "INDOY ",
      "QTY": 150,
      "PRICE": 18.08
    },
    {
      "TICKER": "JJC",
      "NAME": "Copper Long",
      "QTY": 1,
      "PRICE": 44.09
    },
    {
      "TICKER": "JNJ",
      "NAME": "JohnsonJohnson",
      "QTY": 40,
      "PRICE": 129.12375
    },
    {
      "TICKER": "KOLD",
      "NAME": "SHort Gas",
      "QTY": 1,
      "PRICE": 27.5
    },
    {
      "TICKER": "LEMIF",
      "NAME": "LEADING EDGE MAT",
      "QTY": 2000,
      "PRICE": 0.1297
    },
    {
      "TICKER": "MCD",
      "NAME": "MCDONALDS CORP",
      "QTY": 42,
      "PRICE": 88.016
    },
    {
      "TICKER": "NFLX",
      "NAME": "Netflix",
      "QTY": 51,
      "PRICE": 58.594
    },
    {
      "TICKER": "NVCN",
      "NAME": "NEOVAS INC",
      "QTY": 200,
      "PRICE": 3
    },
    {
      "TICKER": "NXTTF",
      "NAME": "NAMASTE TECHNOLOGIES",
      "QTY": 900,
      "PRICE": 0.6449
    },
    {
      "TICKER": "NZDUSD=X",
      "NAME": "NZDUSD",
      "QTY": 1,
      "PRICE": 0.8105
    },
    {
      "TICKER": "PIN",
      "NAME": "PowerShars India",
      "QTY": 1,
      "PRICE": 17.14
    },
    {
      "TICKER": "PTD",
      "NAME": "Platinum Short",
      "QTY": 1,
      "PRICE": 27.43
    },
    {
      "TICKER": "PTM",
      "NAME": "Platinum Long",
      "QTY": 1,
      "PRICE": 17.6
    },
    {
      "TICKER": "PTNR",
      "NAME": "PARTNER COMMUNICATION",
      "QTY": 300,
      "PRICE": 3.89
    },
    {
      "TICKER": "REMX",
      "NAME": "RARE EARTH",
      "QTY": 200,
      "PRICE": 14.84
    },
    {
      "TICKER": "RNVA",
      "NAME": "RENNOVA HEALTH",
      "QTY": 50060,
      "PRICE": 0.00389
    },
    {
      "TICKER": "SCO",
      "NAME": "UltraShort Oil",
      "QTY": 1,
      "PRICE": 36.65
    },
    {
      "TICKER": "SMN",
      "NAME": "ProShares Short Basic Material",
      "QTY": 1,
      "PRICE": 15.85
    },
    {
      "TICKER": "TESTER",
      "NAME": "TESTER_SHARE",
      "QTY": 1,
      "PRICE": 1
    },
    {
      "TICKER": "TESTER2",
      "NAME": "TESTER_SHARE2",
      "QTY": 1,
      "PRICE": 1
    },
    {
      "TICKER": "TORC",
      "NAME": "RESTORBIO INC",
      "QTY": 400,
      "PRICE": 7.5
    },
    {
      "TICKER": "TVIX",
      "NAME": "TVIX",
      "QTY": 8,
      "PRICE": 971.394
    },
    {
      "TICKER": "UNG",
      "NAME": "Long Natural Gas",
      "QTY": 1,
      "PRICE": 19.42
    },
    {
      "TICKER": "US0003M:IND",
      "NAME": "LIBOR USD 3 month",
      "QTY": 1,
      "PRICE": 0.455
    },
    {
      "TICKER": "USDCAD=X",
      "NAME": "USDCAD",
      "QTY": 1,
      "PRICE": 0.9894
    },
    {
      "TICKER": "USDCHF=X",
      "NAME": "USDCHF",
      "QTY": 1,
      "PRICE": 0.9633
    },
    {
      "TICKER": "USDJPY=X",
      "NAME": "USD / JPY",
      "QTY": 1,
      "PRICE": 76.81
    },
    {
      "TICKER": "USO",
      "NAME": "Long Oil",
      "QTY": 1,
      "PRICE": 36.21
    },
    {
      "TICKER": "USSOC:IND",
      "NAME": "OIS Swap Rate",
      "QTY": 1,
      "PRICE": 0.16
    },
    {
      "TICKER": "VALE",
      "NAME": "COMPANHIA VALE DO RIO DOCE",
      "QTY": 2,
      "PRICE": 20.774
    },
    {
      "TICKER": "VZ",
      "NAME": "VERIZON COMM.",
      "QTY": 135,
      "PRICE": 58.07
    },
    {
      "TICKER": "^GSPC",
      "NAME": "S&P500",
      "QTY": 1,
      "PRICE": 1165.15
    },
    {
      "TICKER": "^HSI",
      "NAME": "Hang Seng",
      "QTY": 1,
      "PRICE": 19209.3
    },
    {
      "TICKER": "^IRX",
      "NAME": "13mth Treasury Bills",
      "QTY": 1,
      "PRICE": 0.13
    },
    {
      "TICKER": "^IXIC",
      "NAME": "NASDAQ",
      "QTY": 1,
      "PRICE": 2637.54
    },
    {
      "TICKER": "^KS11",
      "NAME": "KOSPI (S.KOREA)",
      "QTY": 1,
      "PRICE": 1881.24
    },
    {
      "TICKER": "^N225",
      "NAME": "Nikkei",
      "QTY": 1,
      "PRICE": 8881.16
    },
    {
      "TICKER": "^RUT",
      "NAME": "Russell 2000",
      "QTY": 1,
      "PRICE": 767.24
    },
    {
      "TICKER": "^TNX",
      "NAME": "1O yr bond",
      "QTY": 1,
      "PRICE": 3.296
    },
    {
      "TICKER": "^VIX",
      "NAME": "VOLATILITY INDEX",
      "QTY": 1,
      "PRICE": 21.31
    },
    {
      "TICKER": "^VXEWZ",
      "NAME": "Em. Market Vol Index",
      "QTY": 1,
      "PRICE": 28.2
    }
  ]
}
    import json
    app.generate_email(input_data)
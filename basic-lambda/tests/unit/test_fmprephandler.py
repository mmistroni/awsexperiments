import pytest
from hello_world import app

def test_get_quote_for_ticker(mocker):
    mocker.patch('hello_world.app.get_quote_for_ticker', return_value=11)
    assert app.get_quote_for_ticker() == 11

def test_poulate_with_prices(mocker):
    mocker.patch('hello_world.app.get_quote_for_ticker', return_value={'price' : 11})
    test_dict = dict(TICKER='AAPL', QTY=10, PRICE=1 )
    res = app.populate_with_prices(test_dict)
    assert res['CLOSE'] == 11
    assert res['ORIGINAL_POSITION'] == test_dict['QTY'] * test_dict['PRICE']
    assert res['POSITION'] == test_dict['QTY'] * res['CLOSE']
    
def test_getfmp_key(monkeypatch):
    test_key = 'abc'
    monkeypatch.setenv("fmp_key", test_key)
    assert app.get_fmpkey() != test_key
    
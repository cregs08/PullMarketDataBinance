import pandas as pd
from ClientInfo import client


default_market_data_indices = {0: 'time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}

print('Gathering ', default_market_data_indices.values())

def pull_market_data(input_dict):
    print('Pulling Market Data...')
    pulled_data = {}

    for current_symbol in input_dict['symbol_list']:
        current_klines_df = pd.DataFrame(client.get_historical_klines(current_symbol,
                                                                      input_dict['interval'],
                                                                      input_dict['start_str'],
                                                                      input_dict['end_str']))

        pulled_data[current_symbol] = create_subset_of_and_rename_kline_df(current_klines_df)
        print(current_symbol, ' Pulled')

    return pulled_data


def create_subset_of_and_rename_kline_df(current_klines_df):

    data_to_be_pulled_from_klines = default_market_data_indices.keys()

    current_asset_data = pd.DataFrame(current_klines_df[data_to_be_pulled_from_klines].rename
                                          (columns=default_market_data_indices))

    current_asset_data = format_time_and_set_cast_as_float(current_asset_data)

    return current_asset_data


def format_time_and_set_cast_as_float(data_df):
    data_df = data_df.astype('float64')
    data_df['time'] = pd.to_datetime(data_df['time']/1000, unit='s')
    return data_df

if __name__ == '__main__':

    input_dict = {'symbol_list': ['BTCUSDT'],
                  'interval': '4h',
                  'start_str':'30 days ago',
                  'end_str':'1-25-2021'
                  }
    print('Sample Code')
    print('Getting input for:\n', input_dict)

    BTCUSDT_market_data = pull_market_data(input_dict)['BTCUSDT']
    print(BTCUSDT_market_data.head())


    input_dict = {'symbol_list': ['BTCUSDT', 'ETHBTC'],
                  'interval': '4h',
                  'start_str': '12-25-2020',
                  'end_str': '1-25-2021'
                  }
    print('Getting input for:\n', input_dict)

    market_data = pull_market_data(input_dict)
    for symbol in market_data:
        print('\n', symbol, '\n', market_data[symbol].head())


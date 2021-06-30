import gspread
import os
import json


def game_config():

    google_api_json = os.environ.get('GOOGLE_API_JSON')
    if google_api_json:
        print('reading google api info from env variable')
        params = json.loads(google_api_json)
        gc = gspread.service_account_from_dict(params)
    else:
        print('did not find GOOGLE_API_JSON, reading secret from config then...')
        gc = gspread.service_account()

    sheet = gc.open('trader_options')

    general_options = sheet.worksheet('general').get_all_records()
    round_specific = sheet.worksheet('round_specific').get_all_records()

    # view the data
    print(general_options)
    print(round_specific)


if __name__ == '__main__':
    game_config()

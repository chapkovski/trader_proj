import gspread

from oauth2client.service_account import ServiceAccountCredentials

def game_config():

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('trader-317212-ec72a67b17eb.json', scope)
    # ServiceAccountCredentials.from_json_keyfile_dict()
    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('trader_options')

    general_options= sheet.worksheet('general').get_all_records()
    round_specific = sheet.worksheet('round_specific').get_all_records()



    # view the data
    print(general_options)
    print(round_specific)
if __name__ == '__main__':
    game_config()
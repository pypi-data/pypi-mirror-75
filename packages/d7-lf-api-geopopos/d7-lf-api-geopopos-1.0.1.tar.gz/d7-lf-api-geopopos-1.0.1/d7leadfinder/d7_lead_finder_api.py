import requests
import json
import csv
import time
import logging

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class D7LeadFinderAPI():
    '''
    A class to integrate with the D7 Lead Finder API

    Attributes
    __________
    base_uri : str
        the url for the API
    api_key : str
        the API key used to authenticate with the api

    Methods
    _______
    history()
        returns a dictionary objest with all historical searches for the users account



    '''

    base_uri = "https://app.d7leadfinder.com/app/api"

    def __init__(self, api_key):
        self.api_key = api_key
        account_info = self.account()
        if 'error' in account_info:
            raise Exception(f'Failed to authenticate with D7 Lead Finder API endpoint. Reason: {account_info["response_body"]}')
        self.daily_limit = account_info['daily_limit']
        self.today_remaining = account_info['today_remaining']
        self.reset_time = int(time.time()) + int(account_info['seconds_to_reset'])

    def account(self):
        '''
        calls Account endpoint
        :returns: a dict containing account relevant information or and error if the request was not successful
        :rtype: dict
        '''
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500,402, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        search_params = {'key': self.api_key}
        #define exception handling here (have a block around the try/except block to rerun the reques X times before actually throwing an error.)
        r = http.get(f'{self.base_uri}/account', params=search_params)

        exception_count = 0
        max_tries = 3
        while(True):
            try:
                response_body = json.loads(r.text)
                break
            except json.decoder.JSONDecodeError as e:
                logging.error(f'error: {e}')
                exception_count += 1
                if (exception_count == max_tries):
                    raise Exception(f'failed to access account data due to {r.text}')

        
        return response_body


    def history(self):
        '''
        returns a dictionary objest with all historical searches for the users accoun

        :returns: a list of historical searches
        :rtype: list
        '''
        search_params = {'key': self.api_key}
        #define exception handling here (have a block around the try/except block to rerun the reques X times before actually throwing an error.)
        r = requests.get(f'{self.base_uri}/history', params=search_params)

        exception_count = 0
        max_tries = 3
        while(True):
            try:
                response_body = json.loads(r.text)
                break
            except json.decoder.JSONDecodeError as e:
               logging.error(f'error: {e}')
               exception_count += 1
               if (exception_count == max_tries):
                   raise Exception(f'failed to access account data due to {r.text}')
        # if response_body.has_key("error"):
        #     raise ValueError(response_body["error"])
        return response_body


    def keywords(self):
        '''
        Returns all available keywords from D7 Api Endpoint.

        :returns: a dict containing available keywords on the platform
        :rtype: dict
        '''
        search_params = {'key': self.api_key}

        r = requests.get(f'{self.base_uri}/keywords', params=search_params)

        exception_count = 0
        max_tries = 3
        while(True):
            try:
                response_body = json.loads(r.text)
                break
            except json.decoder.JSONDecodeError as e:
               logging.error(f'error: {e}')
               exception_count += 1
               if (exception_count == max_tries):
                   raise Exception(f'failed to access account data due to {r.text}')

        response_body = json.loads(r.text)

        return response_body

    def search_in_history(self, keyword, city, state):
        '''
        A utility function to see if a search has already been made using the city, state, and keyword

        :returns: a dict of info on a search that matches the provided search parameters
        :rtype: dict
        '''
        historical_search = self.history()
        matched_searches = [search_item for search_item in historical_search if search_item['city'].lower() == city.lower() and search_item['state'].lower() == state.lower() and search_item['keyword'].lower() == keyword.lower()]
        if matched_searches:
            return matched_searches[0]
        else:
            return False


    def search(self, keyword, city, state, country_code):
        '''
        create a new search task

        :param keyword: the keyword to search for leads
        :type keyword: str
        :param city: the city to search for leads
        :type city: str
        :param state: the state to search for leads
        :type state: str
        :param country_code: the country_code to search for leads
        :type country_code: str
        :returns: a dictionary containing search relevant values
        :rtype: dict
        '''
        # check if search has previously been made, if it has return said searches searchid to prevent hitting our rate limit
        search_values = self.search_in_history(keyword, city, state)
        if search_values:
            return {'wait_seconds': '0', 'searchid': search_values['searchid'], 'ready_time': -1}

        # if the search has not been created before
        search_params = {'key': self.api_key, 'keyword': keyword, 'location': f'{city} {state}', 'country': country_code}
        #define exception handling here (have a block around the try/except block to rerun the reques X times before actually throwing an error.)
        r = requests.get(f'{self.base_uri}/search', params=search_params)

        exception_count = 0
        max_tries = 3
        while(True):
            try:
                response_body = json.loads(r.text)
                break
            except json.decoder.JSONDecodeError as e:
               logging.error(f'error: {e}')
               exception_count += 1
               if (exception_count == max_tries):
                   raise Exception(f'failed to access account data due to {r.text}')
        # if response_body.has_key("error"):
        #     raise ValueError(response_body["error"])
        return response_body


    def download_leads(self, lead_sheet_meta, keys_to_select, write_to_csv=True, write_location='.'):
        search_id = lead_sheet_meta['searchid']
        city = lead_sheet_meta['city']
        state = lead_sheet_meta['state']
        keyword = lead_sheet_meta['keyword']
        count = 0
        csv_file = f'{write_location}/lead_sheet_{search_id}_{city}_{state}_{keyword}.csv'
        data_file = open(csv_file, 'w')
        csv_writer = csv.writer(data_file)
        # download data for each lead sheet in history
        object_to_append = {key:value for key, value in lead_sheet_meta.items() if key in keys_to_select}
        lead_sheet_params = {'key': self.api_key, 'id': search_id}
        r = requests.get(f'{self.base_uri}/results', params=lead_sheet_params)
        exception_count = 0
        max_tries = 3
        while(True):
            try:
                lead_sheet = json.loads(r.text)
                break
            except json.decoder.JSONDecodeError as e:
               logging.error(f'error: {e}')
               exception_count += 1
               if (exception_count == max_tries):
                   raise Exception(f'failed to access account data due to {r.text}')
        for lead in lead_sheet:
            lead.update(object_to_append)
            if 'position' in lead.keys():
                del lead['position']
            if count == 0:
                header = lead.keys()
                csv_writer.writerow(header)
                count += 1
            csv_writer.writerow(lead.values())
            count += 1
        data_file.close()
        return {'row_count': count, 'filename': csv_file}

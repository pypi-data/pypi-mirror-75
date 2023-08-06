import requests
import rauth
from rauth import OAuth2Service
import json

import numpy as np
import pandas as pd

from humailib.cloud_tools import GoogleBigQuery

import humailib.utils as hu
import humailib.hasher as hh


class CopernicaREST:
    
    def __init__(self, access_token = 'a4b898dfeeb9e67e55136004c2889ba7675a71e0ebbbbc44afa1dcb593220231eb9d20f31261dc0fa214a515b444628f50c51e53e30a235e129d0f452877b2a8'):
        
        self.access_token = access_token
        self.base_url = 'https://api.copernica.com/v2/'
        # Just a random string
        self.state = 'sjDIEj39fkDSUo40'
        
    def get_auth_url(self, client_id = '352576017e08e77410efc978040b7e7d', client_secret = 'dc0ac7e6d01998f78a92850835004d3d'):
        
        copernica = OAuth2Service(
            client_id=client_id,
            client_secret=client_secret,
            name='Copernica',
            authorize_url='https://www.copernica.com/nl/authorize',
            access_token_url='https://api.copernica.com/v2/token',
            base_url='https://www.copernica.com/nl/')

        redirect_uri = 'https://www.copernica.com/nl/'
        params = {'state': self.state,
                  'response_type': 'code',
                  'redirect_uri': redirect_uri}

        url = copernica.get_authorize_url(**params)
        return url
        
    def post(self, endpoint, params=None, data=None, verbose=False):

        url = self.base_url + endpoint + '?access_token={}'.format(self.access_token)
        response = requests.post(url, params=params, data=data)
        if verbose:
            print("REST URI: {}".format(url))
            print("Response code: {0}".format(response.status_code))
            print("Response: " + response.text)

        return response
    
    def delete(self, endpoint, verbose=False):
        
        url = self.base_url + endpoint + '?access_token={}'.format(self.access_token)
        response = requests.delete(url)
        if verbose:
            print("REST URI: {}".format(url))
            print("Response code: {0}".format(response.status_code))
            print("Response: " + response.text)

        return response
    
    def put(self, endpoint, params=None, data=None, verbose=False):
        
        url = self.base_url + endpoint + '?access_token={}'.format(self.access_token)
        response = requests.put(url, params=params, data=data)
        if verbose:
            print("REST URI: {}".format(url))
            print("Response code: {0}".format(response.status_code))
            print("Response: " + response.text)

        return response
    
    def get(self, endpoint, params=None, verbose=False):
        
        url = self.base_url + endpoint + '?access_token={}'.format(self.access_token)
        response = requests.get(url, params=params)
        if verbose:
            print("REST URI: {}".format(url))
            print("Response code: {0}".format(response.status_code))
            print("Response: " + response.text)

        return response, response.json()
        

class CopernicaEmailExtract:
    
    def __init__(self, access_token = 'a4b898dfeeb9e67e55136004c2889ba7675a71e0ebbbbc44afa1dcb593220231eb9d20f31261dc0fa214a515b444628f50c51e53e30a235e129d0f452877b2a8'):
        
        self.api = CopernicaREST(access_token)
        
    def extract(
        self, from_date, to_date, 
        min_destinations = 3, page_size = 1000, verbose=False
    ):
        """
        Get all email events for the date range in the halt-open interval [from_date, to_date).
        """
        
        total = 1
        offset = 0

        mailings = []
        events = []
        
        ii = 1

        while offset < total:

            response, mm = self.api.get(
                'publisher/emailings', params={
                    'type': 'mass', 
                    'start': offset, 'count': page_size,
                    'fromdate': from_date.strftime('%Y-%m-%d'), 'todate': to_date.strftime('%Y-%m-%d')
                }, 
                verbose=False
            )
            total = mm['total']

            for m in mm['data']:
                mailing_id = m['id']
                mailing_datetime = m['timestamp']
                ndestinations = int(m['destinations'])
                if ndestinations >= min_destinations:

                    _, stats = self.api.get('publisher/emailing/{}'.format(mailing_id), verbose=False)
                    #print(stats)
                    print("{}/{} emailing {} at {}, subject '{}', destinations: {:,}, clicks: {:,}, opens: {:,}".format(
                        ii, total,
                        stats['id'], 
                        stats['timestamp'], 
                        stats['subject'], 
                        int(stats['destinations']),
                        int(stats['clicks']), 
                        int(stats['impressions'])
                    ))

                    mailings.append((stats['id'], stats['timestamp'], stats['document'], 
                                     stats['subject'], int(stats['destinations']), 
                                     int(stats['impressions']), int(stats['clicks'])))

                    ## events
                    dd = self._get_events_by_type(
                        mailing_id, mailing_datetime, type='deliveries', event_name='DELIVERY', verbose=verbose
                    )
                    events.extend(dd)

                    ## OPENS ("impressions")
                    oo = self._get_events_by_type(
                        mailing_id, mailing_datetime, type='impressions', event_name='OPEN', verbose=verbose
                    )
                    events.extend(oo)

                    ## CLICKS
                    cc = self._get_events_by_type(
                        mailing_id, mailing_datetime, type='clicks', event_name='CLICK', verbose=verbose
                    )
                    events.extend(cc)

                    ## UNSUBSCRIBES 
                    uu = self._get_events_by_type(
                        mailing_id, mailing_datetime, type='unsubscribes', event_name='UNSUBSCRIBE', verbose=verbose
                    )
                    events.extend(uu)

                ii = 1 + ii
                
            offset = mm['count'] + offset

        df_mailings = pd.DataFrame(mailings, columns=['Broadcast_ID', 'Send_Datetime', 'Campaign_ID', 
                                                      'Campaign_Name', 'Num_Customers', 'Num_Opens', 'Num_Clicks'])
        df_mailings = df_mailings.sort_values(by=['Send_Datetime'])
        
        df_mailings_events = pd.DataFrame(events, columns=['Broadcast_ID', 'Copernica_ID', 'Send_Datetime', 
                                                          'Activity', 'Activity_Datetime', 'Description'])
        df_mailings_events = df_mailings_events.sort_values(by=['Activity_Datetime'])
        
        hu.columns_as_datetime(df_mailings, columns=['Send_Datetime'])
        hu.columns_as_datetime(df_mailings_events, columns=['Send_Datetime','Activity_Datetime'])

        return df_mailings, df_mailings_events
        
    
    def _get_events_by_type(self, mailing_id, mailing_datetime, type='events', event_name='DELIVERY', verbose=False):
        
        events = []
        
        if verbose:
            print("[CopernicaEmailExtract_get_events_by_type]... retrieving {} for {}".format(event_name, mailing_id))

        start = 0
        count = 1000
        total = 1
        while start < total:
            response, dd = self.api.get(
                'publisher/emailing/{}/{}'.format(mailing_id, type), 
                params={'start': start, 'count':count},
                verbose=False
            )
            
            if 200 <= response.status_code <= 299:
                
                total = dd['total']

                if verbose:
                    print("  Emailing: {}, found {} [{},{}) total {}".format(mailing_id, event_name, dd['start'], dd['start']+dd['count'], total))

                for d in dd['data']:

                    if d['emailing'] != mailing_id:
                        print("{} {}".format(d['emailing'], mailing_id))
                    events.append((
                        mailing_id, d['profile'], mailing_datetime, event_name, d['timestamp'], ''
                    ))

                start = dd['count'] + start
            else:
                print("[CopernicaEmailExtract_get_events_by_type] {}".format(response.text))

        print("  Emailing {}, found {:,} events of type {}".format(mailing_id, len(events), event_name))

        return events     
    

class CopernicaProfileLink:
    
    def __init__(self, access_token = 'a4b898dfeeb9e67e55136004c2889ba7675a71e0ebbbbc44afa1dcb593220231eb9d20f31261dc0fa214a515b444628f50c51e53e30a235e129d0f452877b2a8'):
        
        self.api = CopernicaREST(access_token)
        
    def _extract_string(self, record, field_name):
        
        return record[field_name].strip().upper() if field_name in record else ''
    
    def _extract_int(self, record, field_name):
        
        return int(record[field_name]) if field_name in record else np.nan
    
    def link_profiles(self, df, database='', page_size=1000, verbose=True):

        database_id = get_database_id(self.api, database)
        if database_id < 0:
            if verbose:
                print("[link_and_add_to_customers] Failed to find database {}".format(database))
            return None
        
        df_customers = df.copy()

        if 'Copernica_ID' not in df_customers:
            df_customers.loc[:,'Copernica_ID'] = [-1] * len(df_customers)

        if 'Copernica_Unsubscribed' not in df_customers:
            df_customers.loc[:,'Copernica_Unsubscribed'] = [''] * len(df_customers)
                    
        email_to_cid = {e:c for e,c in zip(df_customers.Email.values, df_customers.Customer_ID.values)}
        cop_to_email = {c:e for c,e in zip(df_customers.Copernica_ID.values, df_customers.Email.values)}

        df_customers.set_index('Customer_ID', inplace=True)

        cur_profile = 0
        total_profiles = 1
        n_found = 0
        n_linked = 0
        n_new = 0
        while cur_profile < total_profiles:

            parameters = {
                'start' : cur_profile,
                'limit' : page_size
            }
            response, data = self.api.get('database/{}/profiles'.format(database_id), params=parameters, verbose=False)
            if response.status_code == 200:

                total_profiles = data['total']

                for profile in data['data']:

                    if cur_profile % 1000 == 0:
                        print("{:,}/{:,} ({:.2f}%). Found {:,}. Linked {:,} ({:.2f}%). New {:,}.".format(
                            cur_profile, total_profiles, 
                            100.0*cur_profile / total_profiles, 
                            n_found, n_linked, 
                            100.0*float(n_linked)/np.max([1,n_found]),
                            n_new
                        ))

                    copernica_id = np.nan
                    if 'fields' in profile:
                        fields = profile['fields']
                        cfirstname = self._extract_string(fields, 'MFirstName')
                        clastname = self._extract_string(fields, 'MLastName')
                        cemail = self._extract_string(fields, 'MEmail')
                        copernica_id = int( profile['ID'] )

                        unsub = profile['removed'] or self._extract_string(fields, 'MSubscriberRawState') != 'STATUS_SUBSCRIBED' or self._extract_string(fields, 'MNewsletter') != 'YES' or self._extract_string(fields, 'AfgemeldNieuwsbrief') == 'JA'

                        # Profile ID name
                        copernica_name = (' ').join([cfirstname, clastname])
                        if verbose:
                            print("Copernica customer name: {} (Copernica ID {}, Email {})".format(copernica_name,copernica_id,cemail))

                        record = df_customers.loc[email_to_cid[cemail],:] if cemail in email_to_cid else None
                        if record is not None:
                            
                            if copernica_id in cop_to_email and cop_to_email[copernica_id] != cemail:
                                print("  Found record for Copernica ID {} with email {} (new {}) in customers table.".format(copernica_id, cop_to_email[copernica_id], cemail))
                            
                            customer_id = email_to_cid[cemail]
                            if verbose:
                                print("  Matched in customers table with Customer_ID {} ({}, {})".format(customer_id, record.Name, record.Email))

                            if df_customers.loc[customer_id,'Copernica_ID'] == -1:
                                n_new = 1 + n_new

                            df_customers.loc[customer_id,'Copernica_ID'] = copernica_id
                            df_customers.loc[customer_id,'Copernica_Unsubscribed'] = unsub
                            #pids[lookup_id] = int(pid)
                            n_linked = 1 + n_linked

                        n_found = 1 + n_found

                    cur_profile = 1 + cur_profile
            else:
                print("[link_and_add_to_customers] Call to retrieve {} profiles starting from {} failed.".format(total_profiles, cur_profile))

        print("{:,}/{:,} ({:.2f}%). Found {:,}. Linked {:,} ({:.2f}%). New {:,}.".format(
            total_profiles, total_profiles, 100.0, 
            n_found, n_linked, 
            100.0*float(n_linked)/np.max([1,n_found]),
            n_new
        ))

        df_customers.reset_index(inplace=True)

        return df_customers
    
    
class CopernicaPredictionsLoader:
    
    def __init__(self, database='HumaiTestDB', humai_pred_collection = 'HumaiPredictions', access_token = 'a4b898dfeeb9e67e55136004c2889ba7675a71e0ebbbbc44afa1dcb593220231eb9d20f31261dc0fa214a515b444628f50c51e53e30a235e129d0f452877b2a8'):
        
        self.api = CopernicaREST(access_token)
        self.ready = False
        self.humai_database_id = -1
        self.humai_collection_id = -1
        
    def create_or_init(self, database='HumaiTestDB', humai_pred_collection = 'HumaiPredictions'):
        
        self._create_fields_and_collection(database, humai_pred_collection)
        
    def _create_elements(self, endpoint, df):
    
        _, data = self.api.get(endpoint)

        existing_elements = {d['name']:True for d in data['data']}

        success = True
        for index, row in df.iterrows():

            if row['name'] in existing_elements:
                print("[_create_elements] Found {}".format(row['name']))
            else:
                print("[_create_elements] Creating {}...".format(row['name']))

                new_element = row.to_dict()
                response = self.api.post(endpoint, data=new_element, verbose=True)

                if response.status_code == 201:
                    print("  Created.")
                else:
                    print("  Failed to create.")
                    success = False
                    
        return success
        
    def _create_fields_and_collection(self, database, humai_pred_collection = 'Humai_Predictions'):
        
        ## Set data
        
        self.humai_database_id = -1
        self.humai_collection_id = -1
        self.ready = False
        
        required_fields = [
            ('Humai_Customer_ID','text','',True),
        ]

        df_fields = pd.DataFrame(required_fields, columns=['name','type','value','displayed'])

        required_interests = [
            ('OS_1', 'Humai_Interests'),
            ('OS_2',' Humai_Interests'),
            ('SIX_MONTH', 'Humai_Interests')
        ]

        df_interests = pd.DataFrame(required_interests, columns=['name','group'])

        required_collection_fields = [
            ('Humai_Customer_ID','text','',True),
            ('Humai_Mail_ID','integer',-1,True),
            ('Type','text','PersonalizedMailFlow',True),
            ('Date','date','2020-01-01',True),
            ('DatetimeSlot','text','Midnightto12PM', True),
            ('Group','text','A',True)
        ]

        df_collection_fields = pd.DataFrame(required_collection_fields, columns=['name','type','value','displayed'])
        
        ## Creation logic
        
        response, data = self.api.get('databases')
        if response.status_code == 200:
            
            databases = {db['name']:db['ID'] for db in data['data']}
            self.humai_database_id = int(databases[database]) if database in databases else -1
                
        if self.humai_database_id >= 0:
            
            print("[_create_fields_and_collection] Found database '{}', ID: {}".format(database, self.humai_database_id))
            
            response, data = self.api.get('database/{}/collections'.format(self.humai_database_id))
            if response.status_code != 200:
                print("[_create_fields_and_collection] Could not retrieve collections for database {}".format(database))
                return
                
            collections = {c['name']:c['ID'] for c in data['data']}
            #print(collections)
            self.humai_collection_id = int(collections[humai_pred_collection]) if humai_pred_collection in collections else -1
            #print(self.humai_collection_id)
            
            if self.humai_collection_id == -1:
                
                response = self.api.post('database/{}/collections'.format(self.humai_database_id), data={'name':humai_pred_collection})
                if response.status_code != 201:
                    print("Could not create collection: {}".format(humai_pred_collection))
                    return
                
            if self.humai_collection_id >= 0:
                print("[_create_fields_and_collection] Found collection '{}', ID: {}".format(humai_pred_collection, self.humai_collection_id))
                                       
            success = self.humai_database_id >= 0 and self.humai_collection_id >= 0
            
            if success:
                
                print("Checking fields...")
                success = success & self._create_elements('database/{}/fields'.format(self.humai_database_id), df_fields)
                print("Checking interests...")
                success = success & self._create_elements('database/{}/interests'.format(self.humai_database_id), df_interests)
                print("Checking collection fields...")
                success = success & self._create_elements('collection/{}/fields'.format(self.humai_collection_id), df_collection_fields)

                self.ready = success
            
            print("[_create_fields_and_collection] Ready => {}".format(self.ready))
        else:
            
            print("[_create_fields_and_collection] Database {} does not exist.".format(database))

            
    def push(self, df, pred_type='PersonalizedMailFlow', segment_columns = None, segment_names = None, verbose=False):

        if not self.ready:
            print("[push_predictions_to_copernica] Not ready, call create_or_init()")
            return
        
        nn = len(df)
        ii = 0

        dfg = df.groupby(by='Copernica_ID')
        for copernica_id, df_predictions in dfg:
            
            if copernica_id == -1:
                print("  Skipping invalid Copernica ID: {} with predictions {}".format(copernica_id, df_predictions))
                ii = len(df_predictions) + ii
            else:
                customer_id = df_predictions.iloc[0, :]['Customer_ID']

                response, data = self.api.get('profile/{}'.format(copernica_id), verbose=False)
                if response.status_code == 200:#requests.codes.ok:

                    if verbose:
                        print("Copernica ID {}, Humai Customer ID {} == {}".format(data['ID'], data['fields']['Humai_Customer_ID'], customer_id))
                        for field in data['fields']:
                            print("  {} -> {}".format(field, data['fields'][field]))

                    #
                    # Update existing profile fields
                    #

                    fields_data = {
                        'Humai_Customer_ID' : str(customer_id)
                    }
                    response = self.api.put('profile/{}/fields'.format(copernica_id), data=fields_data, verbose=False)

                    if segment_columns is not None:
                        interests_data = {}
                        row = df_predictions.iloc[0,:]
                        for col,name in zip(segment_columns, segment_names):
                            interests_data[name] = row[col]

                        # Update (PUT) existing interests
                        response = self.api.put('profile/{}/interests'.format(copernica_id), data=interests_data, verbose=False)

                    #
                    # Create predictions as subprofiles
                    #

                    for index, row in df_predictions.iterrows():

                        if ii % 500 == 0:
                            print("{:,}/{:,} ({:.2f} %)".format(ii, nn, 100.0*ii/nn))

                        subprofile = {
                            'Humai_Customer_ID' : str(customer_id),
                            'Humai_Mail_ID' : int(row['Email_ID']),
                            'Type' : pred_type,
                            'Date' : row['Date'].strftime('%Y-%m-%d'),
                            'DatetimeSlot' : row['Time_Of_Day'],
                            'Channel' : 'Email',
                            'Group' : 'B'
                        }

                        response = self.api.post(
                            'profile/{}/subprofiles/{}'.format(copernica_id, self.humai_collection_id), 
                            data=subprofile, verbose=False
                        )

                        ii = 1 + ii

                        #response.status_code, response.text, response.reason
                else:
                    print("Could not retrieve Copernica ID {}".format(copernica_id))

                    ii = len(df_predictions) + ii
            
            
        print("{:,}/{:,} ({:.2f} %)".format(nn, nn, 100.0))
        

    def remove(self, df, pred_type = 'PersonalizedMailFlow', verbose=False):

        if not self.ready:
            print("[push_predictions_to_copernica] Not ready, call create_or_init()")
            return
        
        cpids = df['Copernica_ID'].unique().tolist()
        nn = len(cpids)
        ii = 0
        
        for copernica_id in cpids:
            
            if copernica_id == -1:
                print("  Skipping invalid Copernica ID: {}".format(copernica_id))
            
            if ii % 500 == 0:
                print("{:,}/{:,} ({:.2f} %)".format(ii, nn, 100.0*ii/nn))
            
            if verbose:
                print("Copernica ID {}".format(copernica_id))

            response, data = self.api.get('profile/{}/subprofiles/{}'.format(copernica_id, self.humai_collection_id), verbose=False)
            if response.status_code == 200:#requests.codes.ok:

                for subprofile in data['data']:
                    if subprofile['fields']['Type'] == pred_type:
                        self.api.delete('subprofile/{}'.format(subprofile['ID']))
                        if verbose:
                            print("  Deleted subprofile ID {}, created {}, type {}".format(subprofile['ID'], subprofile['created'], subprofile['fields']['Type']))
                        
            ii = 1 + ii
            
        print("{:,}/{:,} ({:.2f} %)".format(nn, nn, 100.0))
        

def get_database_id(api, database):
    """
    Get the 'ID' field for database in Copernica.
    """
    
    response, data = api.get('databases')
    if response.status_code == 200:
            
        databases = {db['name']:db['ID'] for db in data['data']}
        return int(databases[database]) if database in databases else -1
                
    return -1


class CopernicaCustomersHelper:
    """
    Helper class for converting between Customer IDs and Copernica IDs, given a customers table.
    """
    
    def __init__(self, gbq):
        
        self.df_customers = None
        self.gbq = gbq
        
        return
    
    
    def load_table(self, customers_table, flush_cache=False):
        
        self.df_customers = self.gbq.download_table_to_pandas(customers_table, flush_cache=flush_cache)
        
        hh.decrypt_columns(self.df_customers, columns=['Name','Email','Address'])
        
        num_unknown = len( self.df_customers[self.df_customers['Copernica_ID'] == -1] )
        print("[CopernicaCustomersHelper::load_table] Total number of customers without a known Copernica ID: {:,}/{:,} ({:.2f} %)".format(
            num_unknown, len(self.df_customers), 100.0*num_unknown/len(self.df_customers)
        ))
        
        self.df_customers.drop(index=self.df_customers[self.df_customers['Copernica_ID'] == -1].index, inplace=True)
        self.df_customers.dropna(subset=['Copernica_ID'], inplace=True)
        
        print("  Removed these. Total left: {:,}".format(len(self.df_customers)))
        #df_customers.sort_values(by=['Copernica_ID']).head()
        
        
    def get_customer_ids_for_copernica_ids(self, df, remove_missing=False):
        
        if self.df_customers is None:
            print("[CopernicaCustomersHelper::get_customer_ids_for_copernica_ids] No customers table.")
            return None

        cop_to_cid = { cop:cid for cop,cid in zip(self.df_customers.Copernica_ID.values, self.df_customers.Customer_ID.values) }

        df_out = df.copy()
        df_out.loc[:,'Customer_ID'] = df_out['Copernica_ID'].apply(lambda x: cop_to_cid[x] if x in cop_to_cid else '')
        hu.columns_as_str(df_out, columns=['Customer_ID'], drop_empty=True)

        return df_out


    def get_copernica_ids_for_customer_ids(self, df, remove_missing=False):
        
        if self.df_customers is None:
            print("[CopernicaCustomersHelper::get_copernica_ids_for_customer_ids] No customers table.")
            return None
        
        cid_to_cop = { cid:cop for cop,cid in zip(self.df_customers.Copernica_ID.values, self.df_customers.Customer_ID.values) }

        df_out = df.copy()
        df_out.loc[:,'Copernica_ID'] = df_out['Customer_ID'].apply(lambda x: cid_to_cop[x] if x in cid_to_cop else -1)
        df_out.drop(index=df_out[df_out['Copernica_ID'] == -1].index, inplace=True)

        return df_out 

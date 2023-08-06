import pandas as pd

import humailib.utils as hlu
import humailib.hasher as hasher
from humailib.cloud_tools import GoogleCloudStorage, GoogleBigQuery

class CustomerIDGenerate:
    
    def __init__(self):
        self.cid = 0
        self.customer_id_lookup = {}
        self.customer_table = []
        
    def generate_customer_ids_from_name_address_email(
        self, 
        df, name_col='Name', addr_col='Address', email_col='Email', 
        verbose=False
    ):
      
        num_new = 0
        ii = 1
        n = df[name_col].nunique()
        cids = []
        
        dfg = df[[name_col, addr_col, email_col]].groupby(by=[name_col])
        
        if verbose:
            print("0/{:,} ({:.2f}%)".format(n, 0))
        
        for name, data in dfg:
            #print(name)
            
            name = name.strip().upper()
    
            if verbose and ii % 5000 == 0:
                print("{:,}/{:,} ({:.2f}%) New IDs created: {:,}".format(ii, n, 100.0*ii/n, num_new))

            id_by_email = {}
            id_by_addr = {}
            if name in self.customer_id_lookup:
                id_by_email, id_by_addr = self.customer_id_lookup[name]
    
            for _, row in data.iterrows():
                new_email = row[email_col].strip().upper()
                new_addr = row[addr_col].strip().upper()
                if not new_email in id_by_email and not new_addr in id_by_addr:
                    id_by_email[ new_email ] = self.cid
                    id_by_addr[ new_addr ] = self.cid
                    #print(cid)
                    cids.append(self.cid)
                    
                    self.customer_table.append([self.cid, name, new_email, new_addr])
                    self.cid = 1 + self.cid
                    num_new = 1 + num_new
                else:
                    if new_email in id_by_email:
                        id_by_addr[ new_addr ] = id_by_email[ new_email ]
                    elif new_addr in id_by_addr:
                        id_by_email[ new_email ] = id_by_addr[ new_addr ]

                    #print(addr[ ad ])
                    cids.append( id_by_addr[ new_addr ] )

            self.customer_id_lookup[name] = [id_by_email, id_by_addr]

            ii = 1 + ii
            
        if verbose:
            print("{:,}/{:,} ({:.2f}%). New IDs created: {:,}".format(n, n, 100.0, num_new))
    
        return cids
    
    def get_customer_id_table(self):
        
        if self.customer_table is not None:
            
            data = [tuple(c) for c in self.customer_table]
            df = pd.DataFrame(data, columns=['Customer_ID','Name','Email','Address'])
            hlu.columns_as_str(df, columns=['Name','Email','Address'])
            
            return df
        
        return None
    
    def upload_and_replace_customers_to_bq(self, dataset_table_name):
        
        if self.customer_table is None or self.customer_id_lookup is None:
            return
        
        gbq = GoogleBigQuery()
        df = self.get_customer_id_table()

        hasher.encrypt_columns(df, columns=['Name','Email','Address'])
        gbq.upload_and_replace_table(df, dataset_table_name)
        
    def merge_and_upload_customers_to_bq(self, dataset_table_name):
        
        if self.customer_table is None or self.customer_id_lookup is None:
            return
        
        gbq = GoogleBigQuery()
        df_old = gbq.download_table_to_pandas(dataset_table_name)
        if df_old is None:
            return self.upload_and_replace_customers_to_bq(dataset_table_name)
        
        # Keep only those rows that we haven't touched.
        df_old.drop(columns=['Name','Email','Address'], inplace=True)
        #hlu.columns_as_str(df_old, columns=['Name','Email','Address'])
        #hasher.decrypt_columns(df_old, columns=['Name','Email','Address'])
        
        print(df_old.head())
        
        df_new = self.get_customer_id_table()
        
        print(df_new.head())
        
        df_merged = df_old.merge(df_new, left_on='Customer_ID', right_on='Customer_ID', how='outer')
        
        print(df_merged.head())

        hasher.encrypt_columns(df_merged, columns=['Name','Email','Address'])
        gbq.upload_and_replace_table(df_merged, dataset_table_name)
        
    def download_customers_from_bq(self, dataset_table_name, from_cache=True):
        
        self.__init__()
        
        gbq = GoogleBigQuery()
        df = gbq.download_table_to_pandas(dataset_table_name, from_cache)
        if df is None:
            return False
        
        hlu.columns_as_str(df, columns=['Name','Email','Address'])
        hasher.decrypt_columns(df, columns=['Name','Email','Address'])
        
        self.cid = len(df)
        self.customer_table = df[['Customer_ID','Name','Email','Address']].to_numpy().tolist()
        
        for d in self.customer_table:
            
            cid = d[0]
            name = d[1]

            id_by_email = {}
            id_by_addr = {}
            if name in self.customer_id_lookup:
                id_by_email, id_by_addr = self.customer_id_lookup[name]
                
            new_email = d[2]
            new_addr = d[3]
            
            id_by_email[ new_email ] = cid
            id_by_addr[ new_addr ] = cid

            self.customer_id_lookup[name] = [id_by_email, id_by_addr]
            
        return True
        
        
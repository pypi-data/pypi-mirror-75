import pandas as pd
import numpy as np

from pandas.api.types import is_float_dtype, is_numeric_dtype, is_string_dtype
#from humailib.cloud_tools import GoogleBigQuery, GoogleCloudStorage

humai_table_field_types = {
    """
    Column type definitions from the data dictionary.
    
    https://humai.sharepoint.com/:w:/s/Platform/ET6ZzN-QgiJIpLdbVMkFz0oBe9_UOhSoau0Zvbo7HJ-5lQ?e=OxMlYv
    """
    'transactions' : {
        'datetime' : ['Datetime'],
        'string' : ['Transaction_ID','Branch_ID','Customer_ID','Status','Single_Item_Product_ID'],
        'float' : ['Total_Gross','Discount','Amount_Paid'],
        'int' : ['Total_Num_Items_Purchased']
    },
    'items' : {
        'datetime' : ['Datetime'],
        'string' : ['Transaction_ID','Product_ID','Name'],
        'float' : ['Total', 'Discount'],
    },
    'mailings' : {
        'datetime' : ['Send_Datetime'],
        'string' : ['Broadcast_ID','Campaign_ID'],
        'int' : ['Num_Customers']
    },
    'mailings_events' : {
        'datetime' : ['Activity_Datetime', 'Send_Datetime'],
        'string' : ['Broadcast_ID','Customer_ID','Activity','Description'],
    },
    'customers' : {
        'string' : ['Customer_ID','Email','Name','Address'],
    },
    'products' : {
        'string' : ['Name','Product_ID','SKU'],
        'float' : ['Price'],
    },
    'customer_characteristics' : {
        'string' : ['Customer_ID']
    },
    'product_characteristics' : {
        'string' : ['Customer_ID']
    }
}


def convert_table_columns(df, table_type = 'transactions', datetime_format='%Y-%m-%d %H:%M:%S'):
    
    """
    Convert table column types to table column type definitions as specified in the data dictionary:
    
    https://humai.sharepoint.com/:w:/s/Platform/ET6ZzN-QgiJIpLdbVMkFz0oBe9_UOhSoau0Zvbo7HJ-5lQ?e=OxMlYv
    """
    
    types = humai_table_field_types[table_type]
    if 'datetime' in types:
        columns_as_datetime(df, columns=types['datetime'], datetime_format=datetime_format)
    if 'string' in types:
        columns_as_str(df, columns=types['string'], uppercase=False, drop_empty=False)
    if 'float' in types:
        columns_as_float(df, columns=types['float'], na_replace_value=None, drop_na=False)
    if 'int' in types:
        columns_as_int(df, columns=types['int'], na_replace_value=None, drop_na=False)

    for c in df.columns: print("  {} -> {}".format(c, df[c].dtype))
        
        
def load_table(
    gbq, 
    dataset_table,
    table_type,
    datetime_columns = None,
    datetime_format = '%Y-%m-%d %H:%M:%S', 
    flush_cache = True,
):
    """
    Load table and convert column types
    """    
         
    print("[load_table] Loading table...")
    df = gbq.download_table_to_pandas(dataset_table, flush_cache=flush_cache)
    
    print("[load_table] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)    
    
    return df


def load_csv(
    gcs,
    filename,
    table_type,
    datetime_columns = None,
    datetime_format='%Y-%m-%d %H:%M:%S',
    flush_cache = True
):
    """
    Load CSV from GCS and convert column types.
    """
    
    print("[load_table] Loading table...")
    df = gcs.download_csv(filename, flush_cache=flush_cache)
    
    print("[load_table] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)
    
    return df


def load_and_merge_tables(
    gbq, 
    dataset,
    table_type,
    date_ranges,
    datetime_columns = None,
    datetime_format = '%Y-%m-%d %H:%M:%S', 
    flush_cache = True,
):
    """
    1. Load tables by date range. 
    2. Remove duplicate rows.
    3. Convert column types
    """    
    
    print("[load_and_merge_tables] Loading tables...")
    df = None
    for date_range in date_ranges:
        df_tmp = gbq.download_table_to_pandas(
            "{}.{}_{}".format(dataset, table_type, date_range),
            flush_cache=flush_cache
        )
        if df is None:
            df = df_tmp.copy()
        else:
            df = df.append(df_tmp)

    print("[load_and_merge_tables] Dropping duplicate rows...")
    df.drop_duplicates(inplace=True)
    
    print("[load_and_merge_tables] Converting table columns...")
    if datetime_columns is not None:
        columns_as_datetime(df, columns=datetime_columns, datetime_format=datetime_format)
    convert_table_columns(df, table_type=table_type, datetime_format=datetime_format)
    
    return df
    


def column_stats(df, col_name, max_rows=5):
    """
    Print out column statistics.
    """
    
    isna = df[col_name].isna().sum()
    print("NaNs: {:,} out of {:,} ({:.2f}%)".format(isna, len(df), 100.0*isna/len(df)))
    print("== Describe ==")
    print(df[col_name].describe())
    
    if not is_float_dtype(df[col_name]):
        print("== Value counts ==")
        print(df[col_name].value_counts()[:max_rows])
        
    print("== Head ==")
    print(df[col_name].head(n=max_rows))
    
          
def columns_as_str(df, columns, uppercase=False, drop_empty=False):
          
    """
    Convert columns to string, and convert to uppercase if specified.

    Note: This is done inplace.
    """
    
    for c in columns:
        if c in df:
            if uppercase:    
                df.loc[:,c] = df[c].astype(str, skipna=True).str.upper()
            else:
                df.loc[:,c] = df[c].astype(str, skipna=True)

            if drop_empty:
                df.loc[:,c].replace(to_replace='', value=np.nan, inplace=True)
                df.dropna(subset=[c], inplace=True)
            else:
                df.loc[:,c].fillna('', inplace=True)

            
def columns_as_datetime(df, columns, datetime_format='%Y-%m-%d %H:%M:%S'):
    
    """
    Convert columns to time-zone-agnostic datetime.

    Note: This is done inplace.
    """
    
    for c in columns:
        if c in df:
            df.loc[:,c] = pd.to_datetime(df[c], format=datetime_format, utc=True).dt.tz_convert(None)


def columns_as_float(df, columns, na_replace_value=None, drop_na=True):
    
    """
    Convert columns to float.

    Note: This is done inplace.
    """
    
    if columns is None:
        columns = df.columns
        
    if na_replace_value is None:
        na_replace_value = np.nan
        
    for c in columns:
        if c in df and not is_float_dtype(df[c]):
            
            if is_string_dtype(df[c]):
                df.loc[:,c].replace({
                    '' : np.nan, 'nan' : np.nan, 'NaN' : np.nan, 'None' : np.nan
                }, inplace=True)
                
            if drop_na:
                df.dropna(subset=[c], how='any', inplace=True)
            else:
                df.loc[:,c].fillna(na_replace_value, inplace=True)
                
            df.loc[:,c] = df[c].astype('float64', skipna=False)
        

def columns_as_int(df, columns, na_replace_value=None, drop_na=True):
    
    """
    Convert string/float columns to integer.

    Note: This is done inplace.
    """
    
    if not drop_na and na_replace_value is None:
        na_replace_value = -1.0

    columns_as_float(df, columns, na_replace_value, drop_na)
    
    for c in columns:
        if c in df:
            df.loc[:,c] = df[c].astype('int64', skipna=False)


def transactions_cleanup(df, datetime_column, tid_column = 'Transaction_ID', cid_column = 'Customer_ID', datetime_format='%Y-%m-%d %H:%M:%S'):
    
    """
    Perform common transaction data cleanup.

    Note: This is done inplace.
    """
    
    df.loc[:,datetime_column] = pd.to_datetime( df[datetime_column], format=datetime_format)
    df.loc[:,datetime_column].dropna(inplace=True)

    # Get transactions date range
    print('Date range from {0} to {1}'.format(df[datetime_column].min(), df[datetime_column].max())) 
    
    # Remove column 'Unnamed: 0' if it exists
    if 'Unnamed: 0' in df:
        df.drop('Unnamed: 0', axis=1, inplace=True)
        print("Removed unnamed index column")

    print("Before dropping empty Transaction IDs: {:,}".format(len(df)))

    # Drop Transaction_ID's that are empty
    df.loc[:,tid_column].replace('', np.nan, inplace=True)
    df.dropna(subset=[tid_column], inplace=True)

    print("After: {:,}".format(len(df)))
    
    print("Before dropping empty Customer IDs: {:,}".format(len(df)))

    # Drop [cid]'s that are empty
    df.loc[:,cid_column].replace('', np.nan, inplace=True)
    df.dropna(subset=[cid_column], inplace=True)

    print("After: {:,}".format(len(df)))


def email_ensure_zero_or_one_activity_per_broadcast(
    df, cid_column = 'Customer_ID', activity_column = 'Activity', 
    activity_datetime_column = 'Activity_Datetime',
    verbose=True
):

    """
    Ensure each email sent to each customer has only one event: either a delivery, an open, a click, or a transaction,
    in that order. Keep only the first (in time) occurrence of it.

    Note: This is done inplace.
    """
    
    conv_table = {
        'DELIVERY' : 0,
        'OPEN' : 1,
        'CLICK' : 2,
        'TRANSACTION' : 3
    }
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] converting activities to ordinals...")
    
    #df.loc[:,'activity_id'] = df[activity_column].apply(
    #    lambda x: conv_table[x] if x in conv_table else -1
    #)
    df.loc[:,'activity_id'] = df[activity_column].replace(to_replace=conv_table)

    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] get max...")

    result = df.groupby(by=[cid_column, 'Broadcast_ID'])['activity_id'].max()
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] determining which rows to keep...")
        
    df.loc[:,'keep'] = df.apply(lambda x: 1 if result[x[cid_column],x['Broadcast_ID']] == x['activity_id'] else 0, axis=1)

    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] dropping...")
    df.drop(index=df[df.keep == 0].index, inplace=True)
    
    if verbose:
        print("[email_ensure_zero_or_one_activity_per_broadcast] sorting and keeping only the first occurence of the activity...")
        
    df.sort_values(by=[cid_column, 'Broadcast_ID', activity_datetime_column], inplace=True)
    df.drop_duplicates(subset=[cid_column, 'Broadcast_ID'], keep='first', inplace=True)

    del df['keep']
    del df['activity_id']



def email_keep_activities(df, activities):
    
    """
    Keep only certain email activities, remove the rest.

    Note: This is done inplace.
    """
    
    keep = df.Activity.isin(activities)
    df.drop(index=df[~keep].index, inplace=True)
    
    
def email_activity_stats(df, activity_column='Activity'):
    
    n = []
    n.append(len(df[df[activity_column] == 'DELIVERY']))
    n.append(len(df[df[activity_column] == 'OPEN']))
    n.append(len(df[df[activity_column] == 'CLICK']))
    n.append(len(df[df[activity_column] == 'TRANSACTION']))
    n.append(len(df[df[activity_column] == 'UNSUBSCRIBE']))
    n.append(len(df) - np.sum(n))
    N = np.sum(n)
    
    stats = {
        'Delivered' : n[0],
        'Delivered_perc' : 100.0 * n[0]/N,
        'Opens' : n[1],
        'Opens_perc' : 100.0 * n[1]/N,
        'Clicks' : n[2],
        'Clicks_perc' : 100.0 * n[2]/N,
        'Transactions' : n[3],
        'Transactions_perc' : 100.0 * n[3]/N,
        'Unsubscribes' : n[4],
        'Unsubscribes_perc' : 100.0 * n[4]/N,
        'Other' : n[5],
        'Other_perc' : 100.0 * n[5]/N,
        'Total' : np.sum(n)
    }

    return stats


def print_email_activity_stats(df, activity_column='Activity'):
    
    stats = email_activity_stats(df, activity_column=activity_column)
    
    print("Deliveries:   {:,} ({:.2f} %)".format(stats['Delivered'], stats['Delivered_perc']))
    print("Opens:        {:,} ({:.2f} %)".format(stats['Opens'], stats['Opens_perc']))
    print("Clicks:       {:,} ({:.2f} %)".format(stats['Clicks'], stats['Clicks_perc']))
    print("Transactions: {:,} ({:.2f} %)".format(stats['Transactions'], stats['Transactions_perc']))
    print("Unsubscribes: {:,} ({:.2f} %)".format(stats['Unsubscribes'], stats['Unsubscribes_perc']))
    print("Other:        {:,} ({:.2f} %)".format(stats['Other'], stats['Other_perc']))
    print("Total:        {:,}".format(stats['Total']))
    
    

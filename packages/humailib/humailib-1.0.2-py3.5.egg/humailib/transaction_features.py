import numpy as np
import pandas as pd
import datetime

def get_training_basic_features_transactions(df, date_column, cid, max_hist_len, min_timespan_wks=3, min_unique_wks = 2, make_weeks_whole = True, verbose=False):
    
    df.loc[:,'week_of_year'] = df.loc[:,date_column].apply(lambda x: x.weekofyear)

    dfg_customers = df.sort_values(by=[cid, date_column]).groupby(by=[cid])
    nc = len(dfg_customers)
    print("Number of customers: {:,}".format(nc))
    
    features = []

    ii = 0

    for cid, g in dfg_customers:

        if ii % 5000 == 0:
            print("  {:,}/{:,} ({:.2f} %)".format(ii, nc, 100.0*ii/nc))

        timespan_wks = int((g.iloc[-1,:][date_column] - g.iloc[0,:][date_column]).days / 7) + 1
        if timespan_wks >= min_timespan_wks:
            #print(cid)
            #print(g)
            cutoff_wks = np.random.randint(0, max(0, min(max_hist_len-1, timespan_wks-1))) if timespan_wks > 1 else 0
            
            start_date = g.iloc[0,:][date_column]
            end_date = start_date + datetime.timedelta(weeks=cutoff_wks)
            #print("Start: {}, end {}".format(start_date, end_date))
            timespan_wks = int((end_date - g.iloc[0,:][date_column]).days / 7) + 1
            
            transactions = g[ (g[date_column] >= start_date) & (g[date_column] <= end_date) ].copy()
            if transactions['week_of_year'].nunique() >= min_unique_wks:
                #print(g)

                observed = 1 if g.iloc[-1,:][date_column] == transactions.iloc[-1,:][date_column] else 0
                n_trans = len(transactions) - observed

                transactions.drop_duplicates(subset=['week_of_year'], keep='last', inplace=True)
                act_wks = len(transactions) - observed

                if observed:
                    last_trans_dur_wks = int((transactions.iloc[-1,:][date_column] - transactions.iloc[-2,:][date_column]).days / 7) + 1
                    timespan_wks = int((transactions.iloc[-2,:][date_column] - transactions.iloc[0,:][date_column]).days / 7) + 1
                else:
                    last_trans_dur_wks = int((end_date - transactions.iloc[-1,:][date_column]).days / 7) + 1
                    timespan_wks = int((transactions.iloc[-2,:][date_column] - transactions.iloc[0,:][date_column]).days / 7) + 1

                nonact_wks = max(0, timespan_wks - act_wks)
                #print("start_week {}, end_week {}".format(start_week, end_week))
                #print("observed {}, last_trans_dur {}, n_trans {}, act_wks {}, nonact_wks {}, timespan_wks {}".format(observed, last_trans_dur, n_trans, act_wks, nonact_wks, timespan_wks))

                features.append((cid, observed, transactions.iloc[-2,:][date_column], last_trans_dur_wks, n_trans, act_wks, nonact_wks, timespan_wks))
        
        ii = 1 + ii

    print("  {:,}/{:,} ({:.2f} %)".format(ii, nc, 100.0*ii/nc))
    
    df_features = pd.DataFrame(
        features, columns=[
            'cid', 'observed', 'last_transaction_date', 'last_trans_dur_wks', 'n_trans', 'act_wks', 'nonact_wks', 'timespan_wks'
        ])

    return df_features

def get_prediction_basic_features_transactions(df, timepoint, max_hist_len = 12,
                                           date_column = 'Datetime', cid_column = 'Customer_ID', 
                                           verbose=False):
    
    df.loc[:,'week_of_year'] = df[date_column].apply(lambda x: x.weekofyear)

    dfg_customers = df.sort_values(by=[cid_column, date_column]).groupby(by=[cid_column])
    nc = len(dfg_customers)
    print("Number of customers: {:,}".format(nc))
    print("Transaction stats: {}".format(dfg_customers['Transaction_ID'].count().describe()))
    
    features = []

    ii = 0

    for cid, g in dfg_customers:

        if ii % 5000 == 0:
            print("  {:,}/{:,} ({:.2f} %)".format(ii, nc, 100.0*ii/nc))

        if len(g) >= 1:
            #print("cid {}".format(cid))
            #print("g (n={}) {}".format(len(g),g))
            
            end_date = g.iloc[-1,:][date_column]
            start_date = end_date - datetime.timedelta(weeks=max_hist_len)
            #print("Start: {}, end {}".format(start_date, end_date))
            transactions = g[ (g[date_column] >= start_date) & (g[date_column] <= end_date) ].copy()
            timespan_wks = int((transactions.iloc[-1,:][date_column] - transactions.iloc[0,:][date_column]).days / 7) + 1
            
            #print("Resulting frame length: {}".format(len(transactions)))
            #if len(transactions) > 1:
            #    print("yay")
                        
            #last_trans_dur_wks = int((timepoint - transactions.iloc[-1,:][date_column].tz_convert(None)).days / 7) + 1
            last_trans_dur_wks = int((timepoint - transactions.iloc[-1,:][date_column]).days / 7) + 1
            
            n_trans = len(transactions)
            
            #print("transactions {}".format(transactions))
            
            transactions.drop_duplicates(subset=['week_of_year'], keep='last', inplace=True)
            act_wks = len(transactions)

            nonact_wks = max(0, timespan_wks - act_wks)
            #print("start_week {}, end_week {}".format(start_week, end_week))
            #print("n_trans {}, act_wks {}, nonact_wks {}, timespan_wks {}".format(n_trans, act_wks, nonact_wks, timespan_wks))

            features.append((cid, end_date, last_trans_dur_wks, n_trans, act_wks, nonact_wks, timespan_wks))
        
        ii = 1 + ii

    print("  {:,}/{:,} ({:.2f} %)".format(ii, nc, 100.0*ii/nc))
    
    df_features = pd.DataFrame(
        features, columns=[
            cid_column, 'last_trans_date', 'last_trans_dur_wks', 'n_trans', 'act_wks', 'nonact_wks', 'timespan_wks'
        ])

    return df_features


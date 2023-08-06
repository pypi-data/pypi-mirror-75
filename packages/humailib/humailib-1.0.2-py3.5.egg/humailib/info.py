class Info(dict):
    
    def __init__(self):
        
        return
    
    def init_for_email(
        self, 
        dataset_base, date_range, activity, max_hist_len, 
        activity_column, activity_datetime_column, 
        send_datetime_column,
        cid_column,
        working_dir
    ):
        self['dataset_base'] = dataset_base
        self['dataset_table_base'] = dataset_base + '.mailings_events'
        self['date_range'] = date_range
        self['activity'] = activity
        self['max_hist_len'] = max_hist_len
        self['activity_column'] = activity_column
        self['activity_datetime_column'] = activity_datetime_column
        self['send_datetime_column'] = send_datetime_column
        self['cid_column'] = cid_column
        self['working_dir'] = working_dir
        
        self.__init_datasetname()
        self.__init_intermediate_and_training_files_email()
        self.__init_pipeline_files()
        self.__init_model_files()
        
        
    def init_for_transactions(
        self, 
        dataset_base, date_range, max_hist_len,
        datetime_column, cid_column,
        working_dir
    ):
        self['dataset_base'] = dataset_base
        self['dataset_table_base'] = dataset_base + '.transactions'
        self['date_range'] = date_range
        self['activity'] = 'transactions'
        self['max_hist_len'] = max_hist_len
        self['datetime_column'] = datetime_column
        self['cid_column'] = cid_column
        self['working_dir'] = working_dir
        
        self.__init_datasetname()
        self.__init_intermediate_and_training_files_transactions()
        self.__init_pipeline_files()
        self.__init_model_files()
        
        
    def init_for_products(
        self, 
        dataset_base, date_range, max_hist_len,
        datetime_column, cid_column, product_column,
        working_dir
    ):
        self['dataset_base'] = dataset_base
        self['dataset_table_base'] = dataset_base + '.transactions'
        self['date_range'] = date_range
        self['activity'] = 'products'
        self['max_hist_len'] = max_hist_len
        self['datetime_column'] = datetime_column
        self['cid_column'] = cid_column
        self['product_column'] = product_column
        self['working_dir'] = working_dir
        
        self.__init_datasetname()
        self.__init_intermediate_and_training_files_products()      
        self.__init_pipeline_files()
        self.__init_model_files_product()
        
        
    def __init_datasetname(self):
        
        self['source_datasets'] = ['{}_{}'.format(self['dataset_table_base'], dr) for dr in self['date_range']]
        self['datasetname'] = '_'.join([self['dataset_table_base']]+self['date_range']).replace('.', '_')
        

    def __init_intermediate_and_training_files_base(self):
        
        self['hist_file_cached'] = "{}/data/{}_histories_{}.csv".format(
            self['working_dir'], self['datasetname'], self['activity']
        )
        
        self['features_file'] = "{}/data/{}_features_max_hist_len_{}_{}.csv".format(
            self['working_dir'], self['datasetname'], self['max_hist_len'], self['activity']
        )
        
        self['training_file'] = "{}/data/{}_training_features_max_hist_len_{}_{}.csv".format(
            self['working_dir'], self['datasetname'], self['max_hist_len'], self['activity']
        )
        
        self['validation_file'] = "{}/data/{}_validation_features_max_hist_len_{}_{}.csv".format(
            self['working_dir'], self['datasetname'], self['max_hist_len'], self['activity']
        )
        
        self['test_file'] = "{}/data/{}_test_features_max_hist_len_{}_{}.csv".format(
            self['working_dir'], self['datasetname'], self['max_hist_len'], self['activity']
        )
        
        
    def __init_intermediate_and_training_files_email(self):
        
        self.__init_intermediate_and_training_files_base()
        
        
    def __init_intermediate_and_training_files_transactions(self):
        
        self.__init_intermediate_and_training_files_base()
        
        self['basic_features_file'] = "{}/data/{}_basic_features_{}_{}.csv".format(
            self['working_dir'], self['datasetname'], self['max_hist_len'], self['activity']
        )
        
        
    def __init_intermediate_and_training_files_products(self):
        
        self['transactions_features_file'] = "{}/data/{}_trans_features_{}.csv".format(
            self['working_dir'], self['datasetname'], self['activity']
        )
        
        self['items_features_file'] = "{}/data/{}_items_features_{}.csv".format(
            self['working_dir'], self['datasetname'], self['activity']
        )
        

    def __init_model_files(self):
        
        self['model_file'] = "{}/model/{}/model.joblib".format(
            self['working_dir'], self['activity']
        )
        
        
    def __init_model_files_product(self):
        
        self['model_file'] = "{}/model/model/{}/model.pkl".format(
            self['working_dir'], self['activity']
        )
        
        
    def __init_pipeline_files(self):
        
        self['transform_pipeline_file'] = "{}/model/{}/transform_pipeline.joblib".format(
            self['working_dir'], self['activity']
        )
        
        self['transform_custom_functions_file'] = "{}/model/{}/transform_custom_functions.pkl".format(
            self['working_dir'], self['activity']
        )


    
        

        
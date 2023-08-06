import pandas as pd
import numpy as np
import datetime

from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.externals import joblib

from humailib.cloud_tools import GoogleCloudStorage
from humailib.transformers import DataframeFeatureUnion

class PipelineBuilder:
    """
    This class allows you to build a pipeline, by executing and adding one ore more steps 
    at a time, in a way that lends itself well to how data transformation is implemented in Notebooks.
    """
    
    def __init__(self):
        
        self.steps = {}
        self.step_names = {}
        
        self.current = 'default'
        self.steps[self.current] = []
        self.step_names[self.current] = {}
        
        return
    
    def new_pipeline(self, name):
        
        self.steps[name] = []
        self.step_names[name] = {}
        self.current = name
    
    def transform_and_add(self, steps, df):
        
        pipeline = Pipeline(steps)
        df_out = pipeline.transform(df)
        
        self.add(steps)
        
        return df_out
    
    def add(self, steps):
        
        for step in steps:
            if step[0] not in self.step_names[self.current]:
                self.steps[self.current].append(step)
                self.step_names[self.current][step[0]] = len(self.steps[self.current])-1
                
        return
    
    def build(self, pipelines=None, catch_all_params=None, verbose=True):
        
        assert pipelines is not None and len(pipelines)>0
        
        if isinstance(pipelines, str):
            pipelines = [pipelines]
        
        sub_names = []
        sub_pipes = []
        for pipeline_name in pipelines:
            if pipeline_name in self.steps and len(self.steps[pipeline_name]) > 0:
                sub_names.append(pipeline_name)
                sub_pipes.append(self.steps[pipeline_name])
                
        pipe_out = Pipeline([
            (name, Pipeline(sub)) for name,sub in zip(sub_names,sub_pipes)
        ])
        
        if verbose:
            print("[PipelineBuilder::build] Built:")
            print(pipe_out.steps)
        
        if catch_all_params is not None:
            for catch_all_name, value in catch_all_params.items():
                for pipeline_name in pipelines:
                    # Get the parameters for all components in this pipeline.
                    components_params = pipe_out.named_steps[pipeline_name].get_params()
                    # See if any parameters have names that contain the catch-all name
                    params = {name:value for name,_ in components_params.items() if catch_all_name in name}
                    # Set these to have the catch-all value
                    if verbose:
                        print("[PipelineBuilder::build] Setting params {}".format(params))
                    pipe_out.named_steps[pipeline_name].set_params(**params)
        
        return pipe_out
    
    def load(self, filename, gcs=None, cache_dir='./cache'):
        
        if 'gs://' in filename:
            cache_file = Path(cache_dir + '/' + filename.split('/')[-1])
            gcs.download_file(filename, cache_file)
            pipeline = joblib.load(cache_file)
        else:
            pipeline = joblib.load(filename)
            
        self.__init__()
        for name, sub in pipeline.steps:
            self.steps[ name ] = sub.steps
            self.step_names[ name ] = {sub_step_name:i for i,(sub_step_name,_) in enumerate(sub.steps)}
            
        return
    
    def save(self, filename, gcs=None, cache_dir='./cache'):
        
        if len(self.steps) == 0:
            return
        
        pipeline = self.build(pipelines=[name for name in self.step_names])
        
        if 'gs://' in filename:
            if gcs is None:
                gcs = GoogleCloudStorage()
            cache_file = cache_dir + '/' + filename.split('/')[-1]
            #print(cache_file)
            joblib.dump(pipeline, cache_file)
            gcs.upload_file(cache_file, filename)
        else:
            joblib.dump(pipeline, filename)
        
        return
    
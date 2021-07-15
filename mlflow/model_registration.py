"""
MLOps: Deploy a recommendation system as AWS Hosted Interactive Web Service
"""
def reader(df):
    """
    return a data parsed with Reader class
    args:
        df: pandas dataframe
    returns:
        data parsed
    """
    mindata = df.rating.min()
    maxdata = df.rating.max()
    reader = Reader(rating_scale=(mindata,maxdata))
    data = Dataset.load_from_df(df[['userID', 'itemID', 'rating']], reader)
    return data
    
def preparer(data, method=None, test_size=0.25):
    """ 
    return train and test sets 
    args: 
      data: data parsed with Reader class
      method: for sampling data. 'train_test_split' option. Default None
    returns: 
      trainset and testset
    """
    if method == 'train_test_split':
        trainset, testset = train_test_split(data, test_size=test_size)
    trainset = data.build_full_trainset()
    testset = trainset.build_testset()
    
    return trainset, testset

def trainer(trainset, bsl_options):
    """ 
    return trained model 
    args: 
      trainset: training data parsed with Reader class
      bsl_option: algorithm options 
    returns: 
      trained model
    """
    algo = BaselineOnly(bsl_options=bsl_options)
    model = algo.fit(trainset)
    return model

def predictor(model, testset):
    """ 
    return trained model and predictions
    args: 
      model: trained model
      testset: test data parsed with Reader class 
    returns: 
      trained model and predictions
    """
    predictions = model.test(testset)
    return model, predictions

def tuner(data, bsl_options_grid, param_model):
    """ 
    return model parameters, tuning history and best tuned model
    args: 
      data: data parsed with Reader class 
      bsl_options_grid:  algorithm options grid
      param_model: error measures and cross validation parameters 
    returns: 
      param_model, history_tune, tuned_model
    """
    
    gs = GridSearchCV(BaselineOnly, bsl_options_grid, **param_model)
    gs.fit(data)
    
    history_tune=pd.DataFrame.from_dict(gs.cv_results)
    
    best_bsl_options = gs.best_params['rmse']
    
    return param_model, history_tune

 # Define utils functions for prediction readability

def get_Iu(trainset, uid):
    """
    return the number of items rated by given user
    args: 
      uid: the id of the user
    returns: 
      the number of items rated by the user
    """
    try:
        return len(trainset.ur[trainset.to_inner_uid(uid)])
    except ValueError: # user was not part of the trainset
        return 0

def get_Ui(trainset, iid):
    """
    return number of users that have rated given item
    args:
      iid: the raw id of the item
    returns:
      the number of users that have rated the item.
    """
    try: 
        return len(trainset.ir[trainset.to_inner_iid(iid)])
    except ValueError:
        return 0
    
def plotter_hist(data, productId):
    plt.hist(data_prep_4.loc[data_prep_4['productId'] == '2']['prod_ratings'])
    plt.xlabel('rating')
    plt.ylabel('Number of ratings')
    plt.title('Number of ratings 2 has received')

def mlflow_tune_tracker(data, algo_name, param_grid, param_model, method=None, rundesc='myruntuned'):
    """ 
    return the run id and experiment id of tuned model
    args: 
      algo_name: the name of tuned algorithm 
      param_grid:  algorithm options grid
      param_model: error measures and cross validation parameters 
    returns: 
      run_id, experiment_id
    """
    
    with mlflow.start_run(run_name=algo_name) as run:

        # Store run_id and experiment_id
        run_id=run.info.run_uuid
        experiment_id=run.info.experiment_id
        
        #Read data
        data_parse = reader(data)

        #Tune
        params, history_tune = tuner(data_parse, param_grid, param_model)

        #History
        for index, row in history_tune.iterrows():
            with mlflow.start_run(experiment_id=experiment_id, run_name=algo_name + str(index), nested=True) as subruns:

                #Set variables 
                bsl_options = row['params']
                params_tune = {**params, **bsl_options}
                trainset, testset = preparer(data_parse, method)

                #Log params
                mlflow.log_params(params_tune)
                mlflow.log_metric('fit_time',round(row['mean_fit_time'], 3))
                mlflow.log_metric('test_time', round(row['mean_test_time'], 3))
                mlflow.log_metric('test_rmse_mean', round(row['mean_test_rmse'], 3))
                mlflow.log_metric('test_mae_mean', round(row['mean_test_mae'], 3))
                
                #Log Model (artefact)
                temp = tempfile.NamedTemporaryFile(prefix="model_", suffix=".pkl")
                temp_name = temp.name
                try:
                    model, predictions = predictor(trainer(trainset, bsl_options), testset)
                    dump.dump(temp_name, predictions, model)
                    mlflow.log_artifact(temp_name, 'model')
                finally:
                    temp.close()

                 #Log best and worst predictions. Log charts for validation
                df = pd.DataFrame(predictions, columns=['uid', 'iid', 'rui', 'est', 'details'])
                df['Iu'] = [get_Iu(trainset, uid) for uid in df.uid]
                df['Ui'] = [get_Ui(trainset, iid) for iid in df.iid]
                df['err'] = abs(df.est - df.rui)
                best_predictions = df.sort_values(by='err')[:10]
                worst_predictions = df.sort_values(by='err')[-10:]
                
                temp_dir = tempfile.TemporaryDirectory(dir  =  outdata, prefix='predictions_')
                temp_dirname = temp_dir.name
                temp_file_best = tempfile.NamedTemporaryFile(prefix="best-predicitions_", suffix=".csv", dir=temp_dirname)
                temp_filename_best = temp_file_best.name
                temp_file_worst = tempfile.NamedTemporaryFile(prefix="worst-predicitions_", suffix=".csv", dir=temp_dirname)
                temp_filename_worst = temp_file_worst.name
                try:
                    best_predictions.to_csv(temp_filename_best, index=False)                    
                    worst_predictions.to_csv(temp_filename_worst, index=False)
                    mlflow.log_artifact(temp_dirname)
                finally:
                    temp_file_best.close()
                    temp_file_worst.close()
                    temp_dir.cleanup()
                
                    
        MlflowClient().set_tag(run_id,
                   "mlflow.note.content",
                   rundesc)

#     return run_id, experiment_id   

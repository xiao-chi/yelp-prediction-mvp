# yelp_predict.py
# create final prediction model by stacking lasso, ridge, GBM, SVR, and random forest models
# these 5 models have been created and saved as .sav files separately in 'yelp_prediction_model.ipynb'
# this script is used in the dashboard

import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# load models from disk
LASSO = 'models/lasso_model.sav'
RIDGE = 'models/ridge_model.sav'
GBM = 'models/gbm_model.sav'
SVR = 'models/svr_model.sav'
RF = 'models/rf_model.sav'

lasso_best = pickle.load(open(LASSO, 'rb'))
ridge_best = pickle.load(open(RIDGE, 'rb'))
gbm_best = pickle.load(open(GBM, 'rb'))
svr_best = pickle.load(open(SVR, 'rb'))
rf_best = pickle.load(open(RF, 'rb'))


# return star rating prediction based on inputs of business features x
def predict(x):
    lasso_pred = lasso_best.predict(x)
    ridge_pred = ridge_best.predict(x)
    gbm_pred = gbm_best.predict(x)
    svr_pred = svr_best.predict(x)
    rf_pred = rf_best.predict(x)

    data = {'lasso_pred': lasso_pred[0], 'ridge_pred': ridge_pred[0], 'gbm_pred': gbm_pred[0],
            'svr_pred': svr_pred[0], 'rf_pred': rf_pred[0]}
    all_pred = pd.DataFrame(data, index=['0'])

    all_pred['lasso_pred'] = all_pred['lasso_pred'].astype(float).fillna(0.0)
    all_pred['ridge_pred'] = all_pred['ridge_pred'].astype(float).fillna(0.0)
    all_pred['gbm_pred'] = all_pred['gbm_pred'].astype(float).fillna(0.0)
    all_pred['svr_pred'] = all_pred['svr_pred'].astype(float).fillna(0.0)
    all_pred['rf_pred'] = all_pred['rf_pred'].astype(float).fillna(0.0)

    # final model weights models differently based on accuracy
    all_pred['pred'] = all_pred.apply(lambda row: 0.2*row['lasso_pred'] + 0.2*row['ridge_pred'] + 0.15*row['gbm_pred']
                                                  + 0.4*row['svr_pred'] + 0.05*row['rf_pred'],
                                      axis=1)

    avg_pred = all_pred['pred']
    return avg_pred.get(0)

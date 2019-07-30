import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plotlift(y_true,soft_pred):
    df = pd.DataFrame(np.array([y_true,soft_pred]).T,columns=['true','soft'])
    df.sort_values(by='soft',ascending=False,inplace=True)
    lift = pd.concat([df.groupby('soft').count(),df.groupby('soft').sum()],axis=1)
    lift.sort_index(ascending=False,inplace=True)
    lift.columns = ['strate size','positive']
    lift['negative'] = lift['strate size'] - lift['positive']
    n_positive = df['true'].sum()
    n_negative = df['true'].count()-n_positive
    lift.index.name = 'threshold'
    lift['Group size'] = lift['strate size'].cumsum()
    lift['Group hit probability'] = lift['positive'].cumsum() / lift['Group size']
    lft = lift['Group hit probability'].values / (n_positive /(n_positive+n_negative))
    gr = lift['Group size'].values / len(y_true)
    plt.plot(gr,lft)
    mx = np.max(lft * (gr >= 0.1))
    plt.xlim((0.1, 1))
    plt.ylim((0,1.3*mx))
    plt.grid()
    return 


from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

class count_transformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, col_names = [], threshold_up=None, threshold_down=None, add_rare=False):
        self.col_names = col_names
        self.add_rare = add_rare
        
        if threshold_up is None:
            self.threshold_up = [-np.inf] * len(col_names)
        else:
            self.threshold_up = threshold_up

        if threshold_down is None:
            self.threshold_down = [-np.inf] * len(col_names)
        else:
            self.threshold_down = threshold_down

        if (len(self.threshold_up) != len(self.threshold_down) or
                len(self.threshold_up) != len(self.col_names)):
            raise ValueError('...')
        

    def fit(self, X, y=None):

        X = pd.DataFrame(X)
        
        counts_dict_list = []
        israre_dict_list = []
        
        for i in range(len(self.col_names)):
            ser = X[self.col_names[i]].value_counts()
            
            if self.add_rare:
                israre_dict_list.append((ser<self.threshold_down[i]).to_dict())
                
            t = self.threshold_up[i]
            le = {j:1+i for i,j in zip(range(len(ser[ser>t])) ,ser[ser>t].values)}
            ser = ser.apply(lambda x:le[x] if x>t else 0)
            counts_dict_list.append(ser.to_dict())
            
            
        self.counts_dict_list_ = counts_dict_list
        self.israre_dict_list = israre_dict_list
        return self

    def transform(self, X):

        # Check is fit had been called
        check_is_fitted(self, ['counts_dict_list_'])

        # Input validation
        Xt = pd.DataFrame(X).copy()

        for col, count_dict in zip(self.col_names, self.counts_dict_list_):
            Xt[col] = X[col].apply(lambda x:count_dict[x] if x in count_dict else 0)

        if self.add_rare:
            for col, rare in zip(self.col_names, self.israre_dict_list):
                Xt['rare-' + str(col)] = X[col].apply(lambda x:rare[x] if x in rare else 1)

        return Xt

    
    
class myold_count_transformer(BaseEstimator, TransformerMixin):
    
    def __init__(self, col_names = [], threshold_up=None, threshold_down=None, add_rare=False):
        self.col_names = col_names
        self.threshold_up = threshold_up
        self.threshold_down = threshold_down
        self.add_rare = add_rare

    def fit(self, X, y=None):

        X = pd.DataFrame(X)
        counts_dict_list = []
        for col in self.col_names:
            counts_dict_list.append(X[col].value_counts().to_dict())
        self.counts_dict_list_ = counts_dict_list

        return self

    def transform(self, X):

        # Check is fit had been called
        check_is_fitted(self, ['counts_dict_list_'])

        # Input validation
        Xt = pd.DataFrame(X).copy()

        if self.threshold_up is None:
            threshold_up = [-np.inf] * len(self.col_names)
        else:
            threshold_up = self.threshold_up

        if self.threshold_down is None:
            threshold_down = [-np.inf] * len(self.col_names)
        else:
            threshold_down = self.threshold_down

        if (len(threshold_up) != len(threshold_down) or
                len(threshold_up) != len(self.col_names) or
                len(threshold_up) != len(self.counts_dict_list_)):
            raise ValueError('...')

        for col, count_dict, thresh_up, thresh_down in zip(
                self.col_names, self.counts_dict_list_, threshold_up,
                threshold_down):

            def apply_count(value):
                if value in count_dict:
                    count = count_dict[value]
                    if count < thresh_up:
                        return 0
                    else:
                        return count
                else:
                    return 0

            Xt[col] = X[col].apply(apply_count)

            if self.add_rare:

                def is_rare(value):
                    if value in count_dict:
                        if count_dict[value] < thresh_down:
                            return 1
                        else:
                            return 0
                    else:
                        return 1

                Xt['rare-' + str(col)] = X[col].apply(is_rare)

        return Xt

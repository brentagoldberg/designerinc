import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix as coma
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from scipy.sparse import hstack
import scipy
import matplotlib.pyplot as plt

import sys
sys.path.append("..")
import transform_df as ld



style_cols_init = ['Mid-Century_style',
 'Rustic_style',
 'ArtsandCrafts_style',
 'Regency_style',
 'Transitional_style',
 'Traditional_style',
 'HollywoodRegency_style',
 'Industrial_style',
 'Modern_style',
 'Contemporary_style',
 'Asian_style',
 'Coastal_style']

use_cols_init = ['color_blue',
 'color_brown',
 'color_gray',
 'color_purple',
 'color_yellow',
 'color_pink',
 'color_green',
 'color_teal',
 'color_orange',
 'color_black',
 'color_white',
 'color_red']




class StyleRFC():
    '''
    This class object creates and random forest classifier models for each of the styles inputted, as well as the features inputted.
    
    '''

    
    
    def __init__(self,df,style_cols=style_cols_init,use_cols=use_cols_init,n_estimators=100):
        '''
        Initiate the model with the current best model parameters, or input a different DataFrame, sytle list, or features to use.
        
        INPUT:
        Nothing required, the following is optional
        df: Pandas DataFrame
        style_cols: list of column names in DataFrame to use
        use_cols: list of column names
        n_estimators: number of estimators for each RandomForestClassifier
        
        OUTPUT:
        nothing
        
        CREATED VARIABLES: All dictionaries indexed by style name
        
        model_dict: a dictionary to store the random forest classifier models in this object for each style
        model_bar: a dictionary to store the plots in this object for each style
        model_features: a dictionary to store the top 25 features for each model in this object for each style
        model_scores: a dictionary to store the confusion matrix (conmatrix), accuracy, precision, 
                    recall, false positive (fp), true positive (tp), false negative (fn), true negative (tn)
        
        '''
        self.style_cols = style_cols
        self.use_cols = use_cols
        self.df = df
        self.n_estimators = n_estimators
        self.model_dict = {}
        #self.model_bar = {} deprecated
        self.model_features = {}
        self.metrics_dict = {}
        self.model_predict = {}  ### add to explanation
        self.columns = []
        pass
    
    def run_rfcs(self):
        '''
        Runs multiple Random Forest Classifiers for the different styles to be modeled.
        
        INPUT: nothing
        OUTPUT: nothing
        
        Different functions save and pass model information.
        '''
        ##iterating of the list of style types. as of this note, there are 12 to model.
        
        for style_col in self.style_cols:
            
            filtered_df = self.filter_df_for_style(style_col,self.df)
            
            self.test_rfc(filtered_df,style_col)
            self.record_predictions(style_col)
        
        pass
            

    def filter_df_for_style(self,style_col,df):
        '''
        Identifies the target column, creates a filter where at least one style had to be pre-identified. 
                        Returns filtered DataFrame
                        
        INPUT:
        style_col: string. name of the column used as the target
        df: Pandas DataFrame to be filtered --> requires passing in to avoid overwriting the original df
        
        OUTPUT:
        filtered_df: Pandas DataFrame with the set of usable samples
        
        
        '''
        df['target'] = df[style_col] ### The target column is coded as 1 or 0
        
        df['style_tot'] = 0                                ####workaround to sum columns without a slicing error
        for style in self.style_cols:
            df['style_sum'] = df[style] + df["style_tot"]
            df['style_tot'] = df['style_sum']
            df.drop('style_sum',axis=1,inplace=True)
        
        filtered_df = df[(df['target'] != 0) | (df['style_tot'] >= 1)]  #### leaving an option to filter out more identified rows
        
        return filtered_df
    
    def test_rfc(self,filtered_df,style_col):
        '''
        Transforming, training, fitting, scoring, and graphing are called in this function. Only fitting happens here.
        All of the functionality lives here to avoid saving and calling multiple X, y, X_train, Y_train variables.
        
        INPUT:
        
        filtered_df: Pandas DataFrame with the total usable sample set
        style_col: string. name of the column used as the target
        
        OUTPUT: None
        
        the model is saved to a model_dict in this function
        
        '''
        
        X,y,labels = self.df_for_fit(filtered_df,style_col)
        
        X_train, X_test, Y_train, Y_test = tts(X,y)
        
        rfc = RandomForestClassifier(n_estimators=self.n_estimators)
        
        rfc.fit(X_train,Y_train)                                       ######Fitting the model to split training data
        
        self.model_dict[style_col] = rfc                               ######Saving the model for later use / pickling
        
        self.con_matrix(X_test,Y_test,style_col)                       ######Scoring the model
        
        self.graph_it(rfc,labels,style_col)                            ######Plotting the feature importance for top 25
        
        pass
    
    def df_for_fit(self,filtered_df,style_col):
        '''
        Vectorizing the text using TF-IDF Vectorizer (sklearn). Adding in numerical columns for use. Retaining labels.
        
        INPUT:
        filtered_df: pandas DataFrame limited to a subset of labeled items
        style_col: string. Style name of column and used as tag for saving information
        
        OUTPUT:
        X: numpy sparse array with all data to be used for the model pre train-test split
        Y: list of target values (0 or 1)
        labels: list of column titles from the vectorizer
        
        '''
        vectorizer = TfidfVectorizer(stop_words='english',max_features=1000)
        vector = vectorizer.fit_transform(filtered_df['new_text'])
        labels = vectorizer.get_feature_names()
        y = list(filtered_df[style_col])
        X = scipy.sparse.hstack((vector,filtered_df[self.use_cols].to_sparse()))
        
        return X,y,labels
    
    def con_matrix(self,X_test,Y_test,style_col):
        '''
        Producing a Confusion Matrix, with associated metrics, for future analysis. Saving to metrics_dict for analysis
        
        INPUT:
        X_test: sparse numpy array with held-out data to use for prediction
        Y_test: list with actual target data to compare the predict against.
        style_col: string. Style name of column and used as tag for saving information
        
        OUTPUT:
        None
        
        SAVED:
        metrics_dict: "conmatrix":conmatrix,"tn":tn,"fp":fp,"fn":fn,"precision":precision,"recall":recall,"accuracy":accuracy
        for the current model labeled as style
        
        PRINTED:
        metrics print on the screen as models are being built to ensure the process is running correctly
        
        '''
        
        y_predict = self.model_dict[style_col].predict(X_test)
        
        conmatrix = coma(Y_test,y_predict)
        
        tn,fp,fn,tp = conmatrix.ravel()
        
        ##### Printing these on screen so that the user can verify that the program is running, and not hung up.
        
        print style_col
        print conmatrix
        print "tn: ",tn,"fp: ",fp,"fn: ",fn,"tp: ",tp
        
        precision = tp / float(tp+fp)
        recall = tp / float(tp+fn)
        accuracy = (tp + tn) / float(tp + tn + fp + fn)
        
        print "Precision is: ", precision
        print "Recall is: ", recall
        print "Accuracy is: ", accuracy
        
        self.metrics_dict[style_col] = {"conmatrix":conmatrix,"tn":tn,"fp":fp,"fn":fn,"precision":precision,"recall":recall,"accuracy":accuracy}
    
    def graph_it(self,model,labels,style_col):
        '''
        graph_it does two things: Saves most important features to a dictionary for each model, and saves a plot
        
        INPUT:
        model:
        labels:
        style_col:
        
        OUTPUT:
        none
        
        SAVED:
        model_features_df[style_col]: saves the top 25 features and their scores for future review and analysis
        
        PRINTED:
        plot of top 25 feature importances
        '''
        
        x_labels = list(labels)
        for i in self.use_cols:
            x_labels.append(i)
        self.columns = list(x_labels)
        
        n_features = 25
        features_df = pd.DataFrame(model.feature_importances_,index=x_labels).nlargest(n_features,0)
        features_df.columns = ['scores']
        self.model_features[style_col] = features_df
        #### Needs to be cleaned up
        scores = features_df['scores']
        chart_label = list(features_df.index)
        
        num_cols = range(1,n_features+1)
        plt.bar(num_cols,list(scores),align='center')
        plt.xticks(num_cols,chart_label,rotation='vertical')
        plt.show()
        
        pass
    
    def record_predictions(self,style_col):
        '''
        NOT YET IMPLEMENTED
        '''
        
        filtered_df,y,labels = self.df_for_fit(self.df,style_col)
#        x_labels = list(labels)
#        for i in self.use_cols:
#            x_labels.append(i)
#        filtered_df = pd.DataFrame(filtered_df)
#        filtered_df.columns = x_labels
#        for col in list(filtered_df.columns):
#            if col not in self.columns:
#                filtered_df[col] = 0
#        
#        filtered_df = filtered_df[self.columns]
        print "filtered"
        self.model_predict[style_col] = self.model_dict[style_col].predict_proba(filtered_df)
        print "saved" ###check for sorted issue
        
if __name__ == "__main__":
    df = ld.main()
    
    for i in list(df.columns):
        if "id_" in i:
            use_cols_init.append(i)

    use_cols_init.remove('Solid_style')
    
    style_models = StyleRFC(df)
    
    style_models.run_rfcs()
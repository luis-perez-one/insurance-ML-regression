import numpy as np
import pandas as pd
import itertools

def get_numerical_features(dataframe, y_name):
    num_feats = dataframe.select_dtypes(include=['int64', 'float64'])
    if y_name in num_feats.columns:
        num_feats.drop(y_name, axis='columns', inplace=True)
    num_feats = {'names':num_feats.columns, 'array':np.array(num_feats)}
    return num_feats



def slice_categorical_features(dataframe, y_name):
    cat_feats = dataframe.select_dtypes(include='category')
    if y_name in cat_feats.columns:
        cat_feats.drop(y_name, axis='columns', inplace=True)
    return cat_feats
    


def drop_features(features_array, features_names, features_selected, **kwargs):
    ## kwargs = selection_objective=[remove(default), keep]
        
    if 'selection_objective' not in kwargs.keys():
        selection_objective = 'remove'
    selection_objective = kwargs['selection_objective']
    selection_objective_valid = ['remove', 'keep']
    assert_msg = f'selection_objective = {selection_objective} invalid value. Valid options = {selection_objective_valid}.'
    assert (selection_objective in selection_objective_valid), assert_msg
    
    features = pd.DataFrame(features_array, columns=features_names)
    
    cols_to_drop = []
    if selection_objective == 'keep':
        for c in features.columns:
            if c not in features_selected:
                cols_to_drop.append(c)
    else:
        cols_to_drop = features_selected

    features.drop(cols_to_drop, axis='columns', inplace=True)
    features = {'names':features.columns,
                'set':np.array(features)
            }
    
    return features



def gen_dummy_col_names(dataframe):
    category_dataframe = dataframe.select_dtypes(include='category')
    dummy_col_names = []
    for c in category_dataframe.columns:
        unique_col_vals = category_dataframe[c].unique().tolist()
        dummy_col_names.append([c + '_' + val for val in unique_col_vals])
    
    return dummy_col_names



def gen_dummy_cols_inner_combinations(dummy_col_names):
    #dummy_col_names should be a list of lists, ie
    #[['sex_female', 'sex_male'], ['smoker_yes', 'smoker_no']]
    dummy_cols_inner_combinations = []
    for col_list in dummy_col_names:
        col_list.sort()
        list_lenght = len(col_list)
        if list_lenght > 1:
            for lenght in range(2, list_lenght+1):
                for subset in itertools.combinations(col_list, lenght):
                    dummy_cols_inner_combinations.append(subset)
    
    dummy_cols_inner_combinations = [list(element) for element in dummy_cols_inner_combinations]
    dummy_cols_inner_combinations = [' '.join(element) for element in dummy_cols_inner_combinations]
      
    return(dummy_cols_inner_combinations)



def clean_interaction_features(features_array, features_names, categorical_features_names, dummies_inner_combinations, interaction_degree):
    #this function remove non-sense terms like categorical terms n-powered
    #ie. smoker_yes^2 and inner combinations of categorical terms ie.:
    #(sex_female sex_male)
    
    # generate all expressions that if partially matched in feature names
    # will get them dropped
    non_sense_expressions = []
    for c in categorical_features_names:
        for degree in range (2, interaction_degree+1):
            expression = c + '^' + str(degree)
            non_sense_expressions.append(expression)
            
    non_sense_expressions.extend(dummies_inner_combinations)
    
    # generate a list of the columns to be dropped
    features = pd.DataFrame(features_array, columns=features_names)
    cols_to_drop = []
    for c in features.columns:
        for expression in non_sense_expressions:
            if c.find(expression) != -1:
                cols_to_drop.append(c)
    cols_to_drop = set(cols_to_drop)
    
    features.drop(cols_to_drop, axis='columns', inplace=True)
    
    features = {'names':features.columns, 'set':np.array(features)}
    
    return features
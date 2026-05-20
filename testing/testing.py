import os
import pandas as pd
# import wget
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from MED3pa.datasets import DatasetsManager
from MED3pa.med3pa import Med3paExperiment
from MED3pa.models import BaseModelManager
from MED3pa.visualization.mdr_visualization import visualize_mdr
from MED3pa.visualization.profiles_visualization import visualize_tree


med3pa_params = {"uncertainty_metric":"sigmoidal_error",
    "ipc_type":'RandomForestRegressor',
    "ipc_params":{'n_estimators': 100},
    "apc_params":{'max_depth': 6},
    "ipc_grid_params":{'n_estimators': [50, 100, 200],
                     'max_depth': [2, 4, 6]},
    "apc_grid_params":{'min_samples_leaf': [2, 4, 6]},
    "samples_ratio_min":0,
    "samples_ratio_max":10,
    "samples_ratio_step":5,
    "evaluate_models":True}

# #data preprocessing --> might also want to apply this
# #  After applying preprocessing and exclusion criteria following Zeng et al.,
# # 50 the final MIMIC-IV dataset included 16 271 admissions
# def ihm_process(df):
#     #look at database to do preprocessing
#     pass
# #Get data
# os.makedirs("data/datasets/ihm",exist_ok=True)
# #replace this with the datasets from MIMIC and elCU
# wget.download('https://zenodo.org/records/.../dataset.csv?download=1',out = os.cwd + "\\data\\datasets\\ihm\\dataset.csv")
# df = pd.read_csv(os.cwd + "\\data\\datasets\\ihm\\dataset.csv")
# x,y = ihm_process(df)
# x_train, x_evaluation, y_train, y_evaluation = train_test_split(x, y, test_size=0.3, random_state=54288)
# #base model
# clf_ihm = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1) #ask for these numbers

# datasets_ihm = DatasetsManager()
# datasets_ihm.set_from_data(
#     dataset_type="testing",
#     observations=x_evaluation.to_numpy(),
#     true_labels=y_evaluation,
#     column_labels=x_evaluation.columns
# )
# base_model_manager_ihm = BaseModelManager(model=clf_ihm)
# results_ihm = Med3paExperiment.run(
#     datasets_manager=datasets_ihm,
#     base_model_manager=base_model_manager_ihm,
#     **med3pa_params
# )
# results_ihm.save(file_path='results/ihm')


# visualize_mdr(result=results_ihm, filename='results/ihm/mdr')
# visualize_tree(result=results_ihm, filename='results/ihm/profiles')




#data preprocessing
def oym_process(df):
    # One hot encoding of categorical variables
    categorical_variables = ['living_status', 'admission_group', 'service_group']
    df = pd.get_dummies(df, columns=categorical_variables)
    df = pd.get_dummies(df, columns=['gender'], drop_first=True)
    df = df.sample(frac=0.1,random_state=42).reset_index(drop=True)
    # convert "True/False" to int
    boolean_variables = ['CSO', 'oym']
    df[boolean_variables] = df[boolean_variables].astype(int)
    
    x_features = df.drop(columns=['oym'])
    y = df['oym'].to_numpy()
    return x_features, y

#get data
os.makedirs("data/datasets/oym",exist_ok=True)
#replace this with the datasets from “AdmDemoDx” dataset
# wget.download('https://zenodo.org/records/.../dataset.csv?download=1',out = os.cwd + "\\data\\datasets\\oym\\dataset.csv")
# df = pd.read_csv(os.cwd + "\\data\\datasets\\oym\\dataset.csv")
df = pd.read_csv(r"C:\Users\thanh\Documents\Work\MEDomics\med3pa\testing\dataset.csv")
x,y = oym_process(df)
x_train, x_evaluation, y_train, y_evaluation = train_test_split(x, y, test_size=0.3, random_state=54288)
#base model
clf_oym = RandomForestClassifier(max_depth=4,random_state=42).fit(x_train,y_train)

#meta analysis part
datasets_oym = DatasetsManager()
datasets_oym.set_from_data(
    dataset_type="testing",
    observations=x_evaluation.to_numpy(),
    true_labels=y_evaluation,
    column_labels=x_evaluation.columns
)
base_model_manager_oym = BaseModelManager(model=clf_oym)

results_oym = Med3paExperiment.run(
    datasets_manager=datasets_oym,
    base_model_manager=base_model_manager_oym,
    **med3pa_params
)
# Save the results to a specified directory
results_oym.save(file_path='results/oym')

# Visualize results
visualize_mdr(result=results_oym, filename='results/oym/mdr')
visualize_tree(result=results_oym, filename='results/oym/profiles')

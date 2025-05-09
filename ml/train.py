import azureml.core
from azureml.core import Workspace, Dataset, Experiment
from azureml.train.automl import AutoMLConfig
import pandas as pd

# Carregue o Workspace do Azure ML
ws = Workspace.from_config()

# Obtenha o Dataset
dataset = Dataset.get_by_name(ws, name='vendas-temperatura')

# Converta o Dataset para um DataFrame do pandas
df = dataset.to_pandas_dataframe()

# Selecione as colunas para treinamento
X = df[['Temperatura (°C)']]
y = df['Quantidade de Vendas']

# Configuração do AutoML
automl_config = AutoMLConfig(
    task='regression',
    primary_metric='r2_score',
    experiment_timeout_minutes=15,
    enable_early_stopping=True,
    compute_target='aml-cluster',  # Nome do cluster de computação
    training_data=dataset,
    label_column_name='Quantidade de Vendas',
    # block_list=["LinearRegression"],  # Opcional: para forçar o uso de LinearRegression
    n_cross_validations=5,
    # featurization='auto', # Opcional: para customizar a engenharia de features
    enable_model_explainability=True,
    verbosity=logging.INFO,
    model_explainability=True,
    # blacklisted_models = ["LinearRegression"],
    # max_cores_per_iteration = -1,
    # enable_dnn = False,
    # enable_voting_ensemble = False,
    # enable_stack_ensemble = False,
    # exit_score_threshold = 0.99999,
    # max_concurrent_iterations = 1,
    # max_nodes = 1,
    # node_count = 1,
    # time_column_name = None,
    # drop_column_names = None,
    # weight_column_name = None,
    # cv_split_column_names = None,
    # feature_subset = None,
    # dataset_language = None,
    # dataset_id = None,
    # positive_label = None,
    # test_data = None,
    # test_size = None,
    # validation_data = None,
    # validation_size = None,
    # cv_folds = None,
    # cv_number_of_folds = None,
    # cv_split_indices = None,
    # enable_tf = False,
    # enable_subsampling = True,
    # subsample_size = 0.5,
    # enable_feature_sweeping = True,
    # feature_sweeping_timeout = 3600,
    # feature_sweeping_metric = 'r2_score',
    # feature_sweeping_n_trials = 100,
    # feature_sweeping_keep_top_n_features = 10,
    # feature_sweeping_enable_cache = True,
    # feature_sweeping_enable_parallel_execution = True,
    # feature_sweeping_enable_cross_validation = True,
    # feature_sweeping_cv_folds = 5,
    # feature_sweeping_cv_split_column_names = None,
    # feature_sweeping_cv_split_indices = None,
    # feature_sweeping_enable_subsampling = True,
    # feature_sweeping_subsample_size = 0.5,
    # feature_sweeping_enable_tf = False,
    # feature_sweeping_enable_dnn = False,
    # feature_sweeping_enable_stack_ensemble = False,
    # feature_sweeping_enable_voting_ensemble = False,
    # feature_sweeping_enable_model_explainability = True,
    # feature_sweeping_model_explainability_timeout = 3600,
    # feature_sweeping_model_explainability_metric = 'r2_score',
    # feature_sweeping_model_explainability_n_trials = 100,
    # feature_sweeping_model_explainability_keep_top_n_features = 10,
    # feature_sweeping_model_explainability_enable_cache = True,
    # feature_sweeping_model_explainability_enable_parallel_execution = True,
    # feature_sweeping_model_explainability_enable_cross_validation = True,
    # feature_sweeping_model_explainability_cv_folds = 5,
    # feature_sweeping_model_explainability_cv_split_column_names = None,
    # feature_sweeping_model_explainability_cv_split_indices = None,
    # feature_sweeping_enable_subsampling = True,
    # feature_sweeping_subsample_size = 0.5,
    # feature_sweeping_enable_tf = False,
    # feature_sweeping_enable_dnn = False,
    # feature_sweeping_enable_stack_ensemble = False,
    # feature_sweeping_enable_voting_ensemble = False,
    # feature_sweeping_enable_model_explainability = True,
    # feature_sweeping_model_explainability_timeout = 3600,
    # feature_sweeping_model_explainability_metric = 'r2_score',
    # feature_sweeping_model_explainability_n_trials = 100,
    # feature_sweeping_model_explainability_keep_top_n_features = 10,
    # feature_sweeping_model_explainability_enable_cache = True,
    # feature_sweeping_model_explainability_enable_parallel_execution = True,
    # feature_sweeping_model_explainability_enable_cross_validation = True,
    # feature_sweeping_model_explainability_cv_folds = 5,
    # feature_sweeping_model_explainability_cv_split_column_names = None,
    # feature_sweeping_model_explainability_cv_split_indices = None,
    # feature_sweeping_enable_subsampling = True,
    # feature_sweeping_subsample_size = 0.5,
    # feature_sweeping_enable_tf = False,
    # feature_sweeping_enable_dnn = False,
    # feature_sweeping_enable_stack_ensemble = False,
    # feature_sweeping_enable_voting_ensemble = False,

)

# Crie um experimento
experiment = Experiment(ws, 'previsao-vendas-sorvete')

# Execute o experimento
run = experiment.submit(automl_config, show_output=True)
run.wait_for_completion(show_output=True)

# Obtenha o melhor modelo
best_run, fitted_model = run.get_output()

# Imprima os resultados
print(best_run)
print(fitted_model)

# Registre o modelo
model = run.register_model(model_path='outputs/model.pkl', model_name='previsao-vendas-modelo')

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

# Defina as variaveis para facilitar a configuracao
variable "subscription_id" {
  type        = string
  description = "Sua Subscription ID do Azure"
  default     = "<SUA_SUBSCRIPTION_ID>"
}

variable "resource_group_name" {
  default = "rg-gelato-magico"
}

variable "location" {
  default = "eastus2" # Escolha uma regiao Azure proxima
}

variable "aml_workspace_name" {
  default = "amlw-gelato-magico"
}

variable "storage_account_name" {
  default = "stagelatomagico"
  # Adicione um sufixo para garantir a unicidade
}

variable "container_name" {
  default = "data"
}

# 1. Grupo de Recursos
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# 2. Conta de Armazenamento (para armazenar os dados)
resource "azurerm_storage_account" "sa" {
  name                     = lower(var.storage_account_name)
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# 3. Container na Conta de Armazenamento
resource "azurerm_storage_container" "container" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.sa.name
  container_access_type = "private"
}

# 4. Azure Machine Learning Workspace
resource "azurerm_machine_learning_workspace" "aml" {
  name                    = var.aml_workspace_name
  resource_group_name     = azurerm_resource_group.rg.name
  location                = azurerm_resource_group.rg.location
  storage_account_id      = azurerm_storage_account.sa.id
  identity {
    type = "SystemAssigned"
  }
}

# 5. Azure Machine Learning Compute Cluster (para treinamento do modelo)
resource "azurerm_machine_learning_compute_cluster" "aml_compute" {
  name                       = "aml-cluster"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  machine_learning_workspace_id = azurerm_machine_learning_workspace.aml.id
  vm_size                    = "Standard_DS3_v2" # Uma VM adequada para cargas de trabalho de ML
  scale_settings {
    min_node_count = 0
    max_node_count = 2
    idle_seconds_before_scaledown = 1800
  }
  identity {
    type = "SystemAssigned"
  }
}

# 6. Azure Machine Learning Environment (para definir as dependencias do modelo)
resource "azurerm_machine_learning_environment" "aml_env" {
  name                       = "gelato-env"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.aml.id
  conda_dependencies         = <<CONDA
name: project_environment
channels:
  - conda-forge
dependencies:
  - python=3.8
  - scikit-learn
  - pandas
  - azureml-core
  - azureml-dataset-tabular
CONDA
}

# 7. Azure Machine Learning Dataset (referenciando os dados na conta de armazenamento)
resource "azurerm_machine_learning_dataset_tabular" "aml_dataset" {
  name                       = "vendas-temperatura"
  machine_learning_workspace_id = azurerm_machine_learning_workspace.aml.id
  type                       = "tabular"
  file_system_data_asset {
    storage_account_id = azurerm_storage_account.sa.id
    file_path          = "${azurerm_storage_container.container.name}/vendas.csv" # Assumindo que o arquivo CSV sera carregado aqui
  }
  schema {
    delimiter = ","
    encoding  = "utf8"
    header    = "present"
    columns {
      name = "Data da Venda"
      type = "string"
    }
    columns {
      name = "Quantidade de Vendas"
      type = "integer"
    }
    columns {
      name = "Temperatura (°C)"
      type = "number"
    }
  }
}

# dio-modelo-de-machine-learning-vendas-gelatoinc
## Previsão de Vendas de Sorvete com Azure Machine Learning: esse projeto visa usar o Azure Machine Learning para prever quantos sorvetes serão vendidos com base na temperatura do ambiente.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte:

1.  **Uma assinatura ativa do Azure:** Se você ainda não tem uma, pode criar uma [aqui](https://azure.microsoft.com/pt-br/free/).
2.  **Azure CLI instalado:** Siga as instruções de instalação para o seu sistema operacional [aqui](https://docs.microsoft.com/pt-br/cli/azure/install-azure-cli).
3.  **Terraform instalado:** Siga as instruções de instalação para o seu sistema operacional [aqui](https://www.terraform.io/downloads).
4.  **Conta GitHub:** Para acessar este repositório.
5.  **Permissões adequadas no Azure:** A conta que você usa no Azure CLI precisa ter permissões para criar recursos no grupo de recursos e nos serviços definidos nos arquivos Terraform (normalmente "Owner" ou "Contributor").

### Passo 1: Inicializar o Terraform
- Navegue até o diretório do repositório no seu terminal e execute o seguinte comando para inicializar o Terraform: `terraform init`
### Passo 2: Planejar a Criação dos Recursos
- Execute o seguinte comando para visualizar os recursos que o Terraform irá provisionar no Azure: `terraform plan`
### Passo 3: Provisionar no Azure os recrusos necessários:
- Para provisionar os recursos no Azure, execute o seguinte comando: `terraform apply --auto-approve`
### Passo 4: Verificar os Recursos no Azure
- Após a conclusão do terraform apply, você poderá verificar os recursos criados no portal do Azure:
  * Um Grupo de Recursos chamado rg-gelato-magico (ou o nome que você definiu).
  * Uma Conta de Armazenamento com um container chamado data.
  * Um Workspace do Azure Machine Learning chamado amlw-gelato-magico (ou o nome que você definiu).
  * Um Cluster de Computação do Azure Machine Learning chamado aml-cluster.
  * Um Ambiente do Azure Machine Learning chamado gelato-env.
  * Um Dataset Tabular do Azure Machine Learning chamado vendas-temperatura.
  * Observação: o arquivo vendas.csv precisará ser carregado manualmente para o container data na conta de armazenamento.
    - Usando o Azure CLI para carregar o vendas.csv (após o provisionamento): `az storage blob upload --account-name <NOME_DA_CONTA_DE_ARMAZENAMENTO> --container-name data --file vendas.csv --name vendas.csv`
### Passo 5: Executar o Script Python para Treinar o Modelo: [ml/train.py](https://github.com/dbengp/dio-modelo-de-machine-learning-vendas-gelatoinc/blob/main/ml/train.py) com `python train.py`
### Passo 6: Implementar o Modelo
- Para implementar o modelo e criar um endpoint para fazer previsões em tempo real, você pode usar o Azure Machine Learning SDK ou a interface do usuário do Azure Machine Learning. A documentação do Azure Machine Learning fornece exemplos detalhados: https://docs.microsoft.com/pt-br/azure/machine-learning/how-to-deploy-managed-online-endpoints.



## Movie Review Pipeline Airflow

Este é um projeto de estudo que visa realizar a implementação de um processo ETL utilizando Airflow para gerenciamento de fluxo. Os dados utilizados são informações de avaliação de filmes disponibilizados no site AdoroCinema e são coletados com o uso de um Web Scraper. Atualmente os dados extraídos da página web são agrupados em um arquivo .csv e então são armazenados em um bucket AWS S3.

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/5tj8vipcy05ar43k2011.png)

Este ainda é um projeto em desenvolvimento, como sinalizado no diagrama acima, a parte 1 já está implementada e é possível ler mais sobre a implementação [nesta publicação do meu blog](https://mayaramachado.dev/etl-airflow-s3-spark-redshift-web-scraping.html). Como próximos passos, será realizado a implementação da integração do Airflow com o Apache Spark para realizar processamento nos dados armazenados no AWS S3 e o resultado desse processamento será armazenado em um Data Warehouse no Redshift.

### Pré-requisitos para execução local

  - docker e docker-compose em sua máquina.
  - Uma conta AWS.
  - *aws cli* instalado em sua máquina.
  - Bucket S3 configurado.


Para executar esse projeto em sua máquina você precisa antes configurar o acesso a AWS. As configurações de credenciais da AWS utilizadas pelo projeto Airflow dentro do container Docker são obtidas através do arquivo local .aws gerado no momento que você executa o seguinte comando no bash:

```bash
$ aws configure
```
Portanto, antes de iniciar o container garanta que sua máquina já possui acesso a aws.

Além disso, é importante criar um bucket na sua conta AWS e substituir pelo nome do seu Bucket que será o local que o projeto enviará o arquivo, alterar no arquivo *dags/movie_review.py*

### Execução

Para executar o projeto basta apenas estar no diretório raiz do projeto e executar o comando:

```bash
$ docker-compose up -d
```

Que o ambiente será construído, após alguns instantes o Airflow estará rodando e você poderá acessar em seu navegador no endereço http://localhost:8080. Ao entrar no painel admin do Airflow você poderá dar início ao processamento e depois acompanhar a execução. 

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/hmzflm7jjg9n9juj3e91.png)
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/ttkbhind0noawfp9l62t.png)
![Alt Text](https://dev-to-uploads.s3.amazonaws.com/i/wq019n62mi3j66f5bb0v.png)


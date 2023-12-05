# creditModel

Budowa modelu przewidywania defaultów na podstawie danych z:
https://www.kaggle.com/competitions/credit-default-prediction-ai-big-data/overview

# Kroki

1. Tworzenie i aktywacja środowiska wirtualnego
```bash
python -m venv env
source env/bin/activate
```

2. Instalacja kedro i utworzenie projektu
```bash
pip3 install kedro
kedro new
```
Po uruchomieniu tej drugiej komendy musimy podać nazwe projektu np "creditModel", a następnie przejść do stworzonego folderu
```bash
cd creditModel
```

3. Instalacja potrzebnych pakietów
```bash
pip install jupyterlab
pip3 install "kedro-datasets[pandas.CSVDataSet]"
pip3 install kedro-viz
pip install kedro-mlflow
pip3 install seaborn
pip instal scikit-learn
pip3 install matplotlib
pip3 install mlflow
```

4. Pobierz i rozpakuj dane do katalogu 01_raw z https://www.kaggle.com/competitions/credit-default-prediction-ai-big-data/overview

5. Uzupełnij plik conf/base/catalog.yml tak aby zarejstrować swoje datasety

```yml
test:
  type: pandas.CSVDataSet
  filepath: data/01_raw/test.csv

train:
  type: pandas.CSVDataSet
  filepath: data/01_raw/train.csv

sampleSubmission:
  type: pandas.CSVDataSet
  filepath: data/01_raw/sampleSubmission.csv
```

6. Otwórz notebook i dokonaj analizy danych na przykładzie ```creditmodel/notebooks/Analiza.ipynb```
Aby otworzyć notebook wpisz komendę
```bash
kedro jupyter lab
```
7. Zautomatyzuj proces budowy modelu poprzez stworzenie pipelinów kedro.
Tworzenie pipelinów:
```bash
kedro pipeline create data_processing
kedro pipeline create modelling
```
Następnie wzorując się na plikach z repozyroium ```creditmodel/src/creditmodel/pipelines/modelling/``` oraz ```creditmodel/src/creditmodel/pipelines/data_processing/nodes.py```
utwórz pipeliny do budowy modelu. 
* Pomiń wszystkie logowania mlflow

8. Zwizualizuj swoje pipeliny poprzez polecenie
```bash
kedro viz
```
9. Odpal nowy terminal, aktywuj obecne srodowisko wirtualne i uruchom mlflow na wskazanym porcie:
```bash
source env/bin/activate 
mlflow server --port 8081
```
Po wykonaniu tej komendy, otwórz przeglądarkę i wejdź na: http://localhost:8081/
Pozostaw terminal odpalony, aby nie zakłócać działania mlflow.

10. W poprzednim terminalu odpal komendę:
```bash
kedro mlflow init
```
Spowoduje ona utworzenie pliku ```creditmodel/conf/local/mlflow.yml```. Uzupełnij go zgodnie z tym repozytorium.
Dodaj logowania do mlflow zgodnie ze skryptami w plikach ```nodes.py```
11. Uruchom pipeline
```bash
kedro run
```
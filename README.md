This is a server side for PanTeraV.
In order to run this server, follow these steps:
* First, install using pip the requirements.
In the folder "requirements_for_backend" there are 2 files. Please install both of them.
In order to install the packages, run "pip install -r requirements_for_backend/base_requirements.txt",
"pip install -r requirements_for_backend/server_requirements.txt".
* Second, you can run the server by running application.py.
This operation will open the server in the local host (ip - 0.0.0.0) which listens to all inputs from client.
The routes that the client can call to are in the tali.py file.
* Explanation about the needed files:
    * In the datasets filder, you will find some files you need in order the server to work:
    entities.csv - dataframe that describes the entities in the dataset.
    KLOutput_class0 - output of the KarmaLego algorithm, with the discovered TIRPs.
    states.csv - details about the states in the dataset.
    symbols_to_names - json that maps symbol number to its string name.
    TIRPs_json - legacy file. Can be ignored (depends on the whole system, not this standalone version).
    Symbol_TIRPs - directory with all the indexes of the TIRPs. This is the output of the indexing algorithm of PanTeraV.
    * The given dataset to explore is the Falls dataset, that is describes in the paper.
    The discovered TIRPs are a small version of KarmaLego output with VS=0.6.
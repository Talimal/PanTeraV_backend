We are excited to introduce the instructions for PanTeraV application. PanTeraV is a part
of Tali Malenboim’s thesis. Tali is (currently) a PhD student, with the guidance of
Professor Robert Moskovitch. Our lab is called Complex Data Analytics (CDA) lab in Ben
Gurion University of the Negev. Due to the sharing community in the CDA lab, PanTeraV
was integrated into the CDA lab website, which consists of multiple algorithms and
platforms. In order to submit the system application by itself, we made a standalone
version of the PanTeraV’s server and client. Both of these can be explored and executed
using the supplied links in this document.
In order to execute the whole system of PanTeraV, which includes both a server side and
a client side, please follow the instructions.

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

For any further information, please contact us talimal@post.bgu.ac.il. 
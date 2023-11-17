import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *   
from schema import *
from sqlalchemy.ext.declarative import declarative_base
import json
import requests

# Créer le moteur de base de données SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./../db/newdatabase.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Déclarer la base de données

Base.metadata.create_all(bind=engine)

# Créer la session de base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def load_relationship_asn():
    print('Hello')
    
    # Charger le fichier dans un DataFrame Pandas
    file_path = '../../manrs/20231001.as-rel.txt'
    df = pd.read_csv(file_path, sep='|', comment='#', header=None, names=['asn_1', 'asn_2', 'type'])
    
    # Convertir les valeurs en chaînes
    df['asn_1'] = df['asn_1'].astype(str)
    df['asn_2'] = df['asn_2'].astype(str)
    df['type'] = df['type'].astype(str)
    
    # Convertir le DataFrame Pandas en liste de dictionnaires
    data_list = df.to_dict(orient='records')
    
    # Ajouter les données à la base de données
    for data in data_list:
        relationship_asn = RelationshipAsn(**data)
        relationship_asn_table = RelationshipAsnTable(**relationship_asn.__dict__)
        db.add(relationship_asn_table)
    db.commit()


def load_data_as_mapping():
    print('Hello')
    
    # Charger le fichier JSON dans un dictionnaire
    with open('../../manrs/ii.as-org.v01.2023-01.json', 'r') as file:
        asorg_data = json.load(file)
    
    # Convertir le dictionnaire en DataFrame Pandas
    df = pd.DataFrame(asorg_data.values(), index=asorg_data.keys())
    
    # Renommer les colonnes au bon format
    new_columns = {
        "Status": "status",
        "Reference Orgs": "reference_orgs",
        "Sibling ASNs": "sibling_asns",
        "Name": "name",
        "Descr": "descr",
        "Website": "website",
        "Comparison with CA2O": "comparison_with_ca2O",
        "Comparison with PDB": "comparison_with_pdb",
        "PDB.org_id": "pdb_org_id",
        "PDB.org": "pdb_org"
    }
    df.rename(columns=new_columns, inplace=True)
    
    # Convertir les colonnes en chaînes
    df["asn"] = df.index.astype(str)
    df["status"] = df["status"].astype(str)
    df["reference_orgs"] = df["reference_orgs"].astype(str)
    df["sibling_asns"] = df["sibling_asns"].astype(str)
    df["name"] = df["name"].astype(str)
    df["descr"] = df["descr"].astype(str)
    df["website"] = df["website"].astype(str)
    df["comparison_with_ca2O"] = df["comparison_with_ca2O"].astype(str)
    df["comparison_with_pdb"] = df["comparison_with_pdb"].astype(str)
    df["pdb_org_id"] = df["pdb_org_id"].astype(str)
    df["pdb_org"] = df["pdb_org"].astype(str)
    
    # Insérer les données dans la table DatasetASMapping en utilisant to_sql

    # Convertir le DataFrame Pandas en liste de dictionnaires
    data_list = df.to_dict(orient='records')
    # Créer une liste d'instances DelegatedStatsTable
    instances = [DatasetASMappingTable(**data) for data in data_list]
    
    # Insérer les données en bloc dans la base de données
    db.bulk_save_objects(instances)
    db.commit()
    db.close()
    
def load_categorized_asn():
    print('Hello')
    
    category_df = pd.read_csv('../../manrs/2023-05_categorized_ases.csv', dtype=str)
    selected_columns = ['ASN', 'Category 1 - Layer 1', 'Category 1 - Layer 2']
    category_df = category_df.loc[:, selected_columns]

    header_mapping = {'ASN': 'asn',
                  'Category 1 - Layer 1': 'category_1',
                  'Category 1 - Layer 2': 'category_2'}
    category_df = category_df.rename(columns=header_mapping)
    category_df['asn'] = category_df['asn'].str.replace('AS', '')
    
    # Insérer les données dans la table DatasetASMapping en utilisant to_sql

    for index, row in category_df.iterrows():
        categorized_asn = CategorizedAsnTable(
            asn=row['asn'],
            category_1=row['category_1'],
            category_2=row['category_2'],
        )
        db.add(categorized_asn)

    db.commit()
    db.close()


def load_nro_data():
    print('Hello')
    
    file_path = 'manrs_2023-08/nro-delegated-stats'
    skip_rows = 5  # Nombre de lignes à sauter avant de commencer à lire les données
    df = pd.read_csv(file_path, sep='|', skiprows=skip_rows, header=None, names=['registry', 'cc', 'type', 'start', 'value', 'date', 'status', 'opaque_id', 'extensions'], dtype=str)
    
    # Créer la session de base de données
    db = SessionLocal()
    
    # Convertir le DataFrame Pandas en liste de dictionnaires
    data_list = df.to_dict(orient='records')
    # Créer une liste d'instances DelegatedStatsTable
    nro_instances = [DelegatedStatsTable(**data) for data in data_list]
    
    # Insérer les données en bloc dans la base de données
    db.bulk_save_objects(nro_instances)
    db.commit()
    db.close()
    
    
def load_manrs_data():
    header = {
        'Authorization': 'Bearer ccd3f5e0-f101-4eda-8238-441df282afcc',
        'Content-Type': 'application/json'
    }
    data = {
            "method":"getTableExport",
            "arguments":[{
                "name":"e",
                "value":{
                    "timeRange":{
                        "start":"202309",
                        "duration":1
                    },
                    "asn":None,
                    "network":None,
                    "holder":None,
                    "group":None,
                    "geo":None,
                    "scope":{
                        "filtering":"grip"
                    }
                }},{
                    "name":"t",
                    "value":{
                        "severity":["severities#/all"],
                        "scope":["actions#/all"],
                        "sortInfo":[{
                            "dimension":"asnName",
                            "order":"ascending"
                        }],
                        "skip":0,"limit":100
                    }},{
                        "name":"a",
                        "value":{"delimiter":"semicolon"}
                        }]}
    response = requests.post('https://observatory.manrs.org/api/default/getTableExport', headers=header, json=data)
    manrs_data =response.json()

    del manrs_data['rows'][0]
    print('Start')
    try:
        for row in manrs_data['rows']:
            values = row.split(';')
            
            manrs_results = ManrsDataTable(
                    asn =values[0],
                    holder = values[1],
                    country =values[2],
                    un_regions =values[3],
                    un_sub_regions =values[4],
                    rir_regions =values[5],
                    filtering =None if not values[6] else float(values[6]),
                    antispoofing =None if not values[7] else float(values[7]),
                    coordination =None if not values[8] else float(values[8]),
                    irr =None if not values[9]  else float(values[9]),
                    rpki =None if not values[10]  else float(values[10])
            )
            db.add(manrs_results)
    except Exception as e:
        print(e)
        print(values)
    print('finish')
    db.commit()
    db.close()
    
    
def load_rov_data():
    response = requests.get('https://api.rovista.netsecurelab.org/rovista/api/overview?offset=0&count=27622&sortBy=rank&sortOrder=asc')
    rovs_data =response.json()
    print('Start')
    try:
        len(rovs_data['data'])
        for row in rovs_data['data']:
            rov = RovDataTable(
                    asn =row['asn'],
                    rank = row['rank'],
                    country = row['country'],
                    ratio = row['ratio'],
                    lastUpdatedDate = row['lastUpdatedDate'],
            )
            db.add(rov)
    except Exception as e:
        print(e)
        print(rovs_data)
    print('finish')
    db.commit()
    db.close()
    

    
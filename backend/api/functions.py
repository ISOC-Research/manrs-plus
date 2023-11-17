# functions.py
from sqlalchemy.orm import Session
from typing import List
import requests
import csv, ast, json
from models import *
from models import CategorizedAsnTable, ManrsDataTable
from sqlalchemy.orm import aliased
from fastapi import  HTTPException
from sqlalchemy import and_, or_, select
import pandas as pd


def read_file_and_extract_content(file_path: str):
    with open(file_path, "r") as file:
        if file_path.endswith(".json"):
            content = json.load(file)
        elif file_path.endswith(".csv"):
            content = read_csv(file)
        elif file_path.endswith(".txt"):
            content = read_txt(file)
        else:
            content = read_txt(file)
            #raise ValueError("Unsupported file format")

    return content

def read_csv(file):
    data_list = []
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
            data_list.append(row)
    return data_list

def read_txt(file):
    content = [line.strip() for line in file.readlines()]
    return content




def get_rov_from_api( asn):
    response = requests.get(f'https://api.rovista.netsecurelab.org/rovista/api/AS-roa-ratios/{asn}')
    try:
        rovs_data =response.json()
        print(rovs_data)
        return rovs_data[-1]['ratio']
    except Exception as err:
        print(err)
        
def get_rov_from_db(db: Session, asn):
    rov_data = db.query(RovDataTable).filter(RovDataTable.asn == asn).first()
    if rov_data:
        return rov_data.ratio
        
def get_asns_by_country(db: Session, country):
    delegated_stats_data = db.query(ManrsDataTable).filter(ManrsDataTable.country == country).all()
    asns = []
    for row in delegated_stats_data:
        asns.append(row.asn)
    return asns

def get_manrs_metrics_by_asn(db: Session, asn):
    data = db.query(ManrsDataTable).filter(ManrsDataTable.asn == asn).first()
    return data

def get_siblings(db, asn):
    dataset_mapping_data = db.query(DatasetASMappingTable).filter(DatasetASMappingTable.asn == str(asn)).first()
    return ast.literal_eval(dataset_mapping_data.sibling_asns)

def get_asns_by_category(db, category):
    categorized_asn_data = db.query(CategorizedAsnTable).filter(or_(CategorizedAsnTable.category_1 == str(category), CategorizedAsnTable.category_2 == str(category))).all()
    asns = []
    for row in categorized_asn_data:
        asns.append(row.asn)
    return asns


def get_all_categories(db):
    categorized_asn_data = db.query(CategorizedAsnTable).all()
    categories = set()
    for row in categorized_asn_data:
        if row.category_1 is not None:
            categories.add(row.category_1)
        if row.category_2 is not None:
            categories.add(row.category_2)
    return sorted(categories)

def get_all_countries(db):
    manrs_data = db.query(ManrsDataTable).all()
    countries = set()
    for row in manrs_data:
        if row.country is not None:
            countries.add(row.country)
    sorted_countries = sorted(countries)
    return sorted_countries


def get_asns_by_country_and_category(db, country, category, limit=0, offset=100):
    asns = []
    try:
        asns_country = get_asns_by_country(db, country)
        asns_category = get_asns_by_category(db, category)
        for asn in asns_country:
            if asn in asns_category:
                asns.append(asn)
        return asns

    except Exception as err:
        print(err)
        return []

# Function to check the database connection
def check_database_connection(db: Session):
    try:
        # Execute a query to check the database connection
        result = db.query(ManrsDataTable).first()
        if not result:
            raise HTTPException(status_code=500, detail="The database is inaccessible at startup.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error at startup: {str(e)}")
    

def get_providers_from_db(db, asn, level_two):
    providers_data = db.query(RelationshipAsnTable).filter(and_(RelationshipAsnTable.asn_2 == str(asn), RelationshipAsnTable.type == '-1')).all()
    providers = {}
    for l1 in providers_data:
        providers[l1.asn_1]= []
        if level_two:
            provider_l2_data = db.query(RelationshipAsnTable).filter(and_(RelationshipAsnTable.asn_2 == str(l1.asn_1), RelationshipAsnTable.type == '-1')).all()
            for l2 in provider_l2_data:
                providers[l1.asn_1].append(l2.asn_1)
    return providers

    
def get_metrics_db(db: Session, asn: str):
    metrics = get_manrs_metrics_by_asn(db, asn)
    rov = get_rov_from_db(db, asn)
    filtering = metrics.filtering if hasattr(metrics, 'filtering') else 0
    coordination = metrics.coordination if hasattr(metrics, 'coordination') else 0
    antispoofing = metrics.antispoofing if hasattr(metrics, 'antispoofing') else 0
    irr = metrics.irr if hasattr(metrics, 'irr') else 0
    rpki = metrics.rpki if hasattr(metrics, 'rpki') else 0
    rov = rov if rov is not None else 0

    filtering = filtering or 0
    coordination = coordination or 0
    antispoofing = antispoofing or 0
    irr = irr or 0
    rpki = rpki or 0
    rov = rov or 0
   
    data = {
        "filtering": filtering,
        "coordination": coordination,
        "antispoofing": antispoofing,
        "irr": irr,
        "rpki": rpki,
        "rov": rov,
        "score": float((filtering + coordination + antispoofing + irr + rpki + rov))
    }
    
    return {
        "name": metrics.holder if hasattr(metrics, 'holder') else None,
        "country": metrics.country if hasattr(metrics, 'country') else None,
        "metrics": data,
    }
    

def get_providers_data(db: Session, asn: str, detail: bool, level_two: bool):
    
    manrs_data = get_metrics_db(db, asn)
    providers = get_providers_from_db(db, asn, level_two)
    if detail:
        for key in providers.keys():
           
            providers_details = {}
            
            for key_l2 in providers[key]:
                providers_details[key_l2] = {'detail': get_metrics_db(db, key_l2)} 
            providers[key] = {'detail': get_metrics_db(db, key), 'providers_l2': providers_details }
    
              
    return {
        "detail":{
            "name": manrs_data['name'],
            "country": manrs_data['country'],
            "metrics": manrs_data['metrics'] if detail else {},
        },
        "providers": providers
    }
  
    
def get_providers_level_two_data(db: Session, providers, detail: bool):
    providers_l2 = {}
    for provider in providers:
        providers_l2[provider]=get_providers_from_db(db, provider)
        
                
    return providers_l2


def transform_data(existing_data):
    # Créez une structure pour stocker les données transformées
    transformed_data = {
        "category": existing_data.get("category", ""),
        "country": existing_data.get("country", ""),
        "networks": {},
        "count": existing_data.get("count", 0)
    }

    providers_l2 = {}
    providers = {}
    asns = {}

    for data in existing_data['networks'].items():
        
        if data[1]['providers']:
            for data2 in data[1]['providers'].items():
                providers[data2[0]] = data2[1]['details']
                print(data[1]) 
        else:
            asns[data[0]] = data[1]['detail']


    return transformed_data
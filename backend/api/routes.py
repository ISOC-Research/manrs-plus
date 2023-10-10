# routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SessionLocal, get_db  
from functions import *  
from models import *

router = APIRouter()

@router.get("/get_providers")
async def get_providers(
    asn: str = Query(default="22"),
    level_two: bool = Query(default=False),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    if asn is None:
        raise HTTPException(status_code=403, detail="asn is required")
    
    providers = get_providers_from_db(db, asn, level_two)
    
    return {"asn": asn, "providers": providers}

@router.get("/get_categories")
async def get_categories(
    db: SessionLocal = Depends(get_db)
):
    
    data = get_all_categories(db)
    
    return {"data": data}  


@router.get("/get_countries")
async def get_countries(
    db: SessionLocal = Depends(get_db)
):
    
    data = get_all_countries(db)
    
    return {"data": data}  

@router.get("/get_asns")
async def get_asns(
    category: str = Query(None),
    country: str = Query(None),
    detail: bool = Query(None),
    level_two: bool = Query(default=False),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    
    if category and country:
        asns = get_asns_by_country_and_category(db, country, category)
        
        asns_metrics = {}
        for asn in asns:
            asns_metrics[asn]=get_providers_data(db, asn, detail, level_two)
        return {
                "category": category,
                "country": country,
                "networks": asns_metrics,
                "count": len(asns_metrics)
               }
    elif category:
        asns = get_asns_by_category(db, category)
        asns_metrics = {}
        # Perform pagination
        asns = asns[skip : skip + limit]
        
        for asn in asns:
            asns_metrics[asn]=get_providers_data(db, asn, detail, level_two)
        
        return {
                "category": category,
                "networks": asns_metrics,
                "count": len(asns_metrics)
               }  
    elif country:
        asns = get_asns_by_country(db, country)
        asns_metrics = {}
        for asn in asns:
            asns_metrics[asn]=get_providers_data(db, asn, detail, level_two)
        return {
                "country": country,
                "networks": asns_metrics,
                "count": len(asns_metrics)
               }    
    else:
       return {
           "data": {}
       } 
    
    
@router.get("/get_siblings")
async def get_sibligs(
    asn: str = Query(default="22"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    if asn is None:
        raise HTTPException(status_code=403, detail="asn is required")
    
    siblings = get_siblings(db, asn)
    
    return {"asn": asn, "siblings": siblings}


@router.get("/get_rovs")
async def get_rovs(
    asn: str = Query(default="22"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    if asn is None:
        raise HTTPException(status_code=403, detail="asn is required")
    
    rov = get_rov_from_db(db, asn)
    
    return {"asn": asn, "rov": rov}    
        
        
@router.get("/get_metrics_manrs")
async def get_metrics_manrs(
    asn: str = Query(default="22"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    if asn is None:
        raise HTTPException(status_code=403, detail="asn is required")
    
    data = get_manrs_metrics_by_asn(db, asn)
    
    return {"asn": asn, "data": data}  


@router.get("/get_metrics")
async def get_metrics(
    asn: str = Query(default="22"),
    skip: int = Query(0),
    limit: int = Query(10),
    db: SessionLocal = Depends(get_db)
):
    if asn is None:
        raise HTTPException(status_code=403, detail="asn is required")
    
    metrics = get_manrs_metrics_by_asn(db, asn)
    rov = get_rov_from_api(asn)
    
    data = {
        
        "filtering": metrics.filtering,
        "coordination": metrics.coordination,
        "antispoofing": metrics.antispoofing,
        "irr": metrics.irr,
        "rpki": metrics.rpki,
        "rov": rov
    }
    
    return {
        "asn": asn, 
        "name": metrics.holder,
        "country": metrics.country,
        "metrics": data
    }    
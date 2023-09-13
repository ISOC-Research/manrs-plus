
from pydantic import BaseModel

class ManrsData(BaseModel):
    asn : str
    holder : str
    country : str
    un_regions : str
    un_sub_regions : str
    rir_regions : str
    filtering : float
    antispoofing : float
    coordination : float
    irr : float
    rpki : float 
    
class RovData(BaseModel):
    
    asn : str
    rank : int
    country : str
    ratio : float
    lastUpdatedDate : str

class DatasetASMapping(BaseModel):
    asn: str
    status: str
    reference_orgs: str
    sibling_asns: str
    name: str
    descr: str
    website: str
    comparison_with_ca2O: str
    comparison_with_pdb: str
    pdb_org_id: str
    pdb_org: str
    
class DelegatedStatsRecord(BaseModel):
    registry: str
    cc: str
    type: str
    start: str
    value: str
    date: str
    status: str
    opaque_id: str
    extensions: str
    
class CategorizedAsn(BaseModel):
    asn_1: str
    asn_2: str
    type: str   
    

class RelationshipAsn(BaseModel):
    asn_1: str
    asn_2: str
    type: str


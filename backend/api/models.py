# models.py
from sqlalchemy import Column, DateTime, Integer, String, Float, create_engine
from datetime import datetime
from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ManrsDataTable(Base):
    __tablename__ = "manrs_data"

    id = Column(Integer, primary_key=True, index=True)
    asn = Column(String, nullable=True)
    holder = Column(String, nullable=True)
    country = Column(String, nullable=True)
    un_regions = Column(String, nullable=True)
    un_sub_regions = Column(String, nullable=True)
    rir_regions = Column(String, nullable=True)
    filtering = Column(Float, nullable=True)
    antispoofing = Column(Float, nullable=True)
    coordination = Column(Float, nullable=True)
    irr = Column(Float, nullable=True)
    rpki = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class RovDataTable(Base):
    __tablename__ = "rovs_data"

    id = Column(Integer, primary_key=True, index=True)
    asn = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)
    country = Column(String, nullable=True)
    ratio = Column(Float, nullable=True)
    lastUpdatedDate = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatasetASMappingTable(Base):
    __tablename__ = "dataset_as_mapping"

    id = Column(Integer, primary_key=True, index=True)
    asn = Column(String, nullable=True)
    status = Column(String, nullable=True)
    reference_orgs = Column(String, nullable=True)  # Stocker une liste de références d'organisations au format JSON
    sibling_asns = Column(String, nullable=True)     # Stocker une liste de frères ASN au format JSON
    name = Column(String, nullable=True)
    descr = Column(String, nullable=True)
    website = Column(String, nullable=True)
    comparison_with_ca2O = Column(String, nullable=True)
    comparison_with_pdb = Column(String, nullable=True)
    pdb_org_id = Column(String, nullable=True)
    pdb_org = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class DelegatedStatsTable(Base):
    __tablename__ = "delegated_stats"

    id = Column(Integer, primary_key=True, index=True)
    registry = Column(String, nullable=True)
    cc = Column(String, nullable=True)
    type = Column(String, nullable=True)
    start = Column(String, nullable=True)
    value = Column(String, nullable=True)
    date = Column(String, nullable=True)
    status = Column(String, nullable=True)
    opaque_id = Column(String, nullable=True)
    extensions = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class CategorizedAsnTable(Base):
    __tablename__ = "categorized_asn"

    id = Column(Integer, primary_key=True, index=True)
    asn = Column(String, unique=True)
    category_1 = Column(String, nullable=True)
    category_2 = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RelationshipAsnTable(Base):
    __tablename__ = "relationship_asn"

    id = Column(Integer, primary_key=True, index=True)
    asn_1 = Column(String, nullable=True)
    asn_2 = Column(String, nullable=True)
    type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
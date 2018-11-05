from typing import Dict

from rdflib import Namespace
from rdflib.namespace import NAME_START_CATEGORIES

MGI = Namespace('http://www.informatics.jax.org/accession/MGI:')
NUCC = Namespace('https://www.ncbi.nlm.nih.gov/nuccore/')
UNIPROT = Namespace('http://identifiers.org/uniprot/')
CCDS = Namespace('http://identifiers.org/ccds/')
PUBMED = Namespace('http://identifiers.org/pubmed/')
NCBIGENE = Namespace('https://www.ncbi.nlm.nih.gov/gene/')
MIM = Namespace('http://identifiers.org/mim/')
ENSEMBL = Namespace('http://identifiers.org/ensembl/')
homology = Namespace('http://data2services/model/association/homology/')

# Fix to allow CURI type uri's
from metamodel.utils.namespaces import HGNC, BIOENTITY

NAME_START_CATEGORIES.append('Nd')

namespace_map: Dict[str, Namespace] = {
    'biolink': BIOENTITY,
    'HGNC': HGNC,
    'MGI': MGI,
    'NUCC': NUCC,
    'UNIPROT': UNIPROT,
    'CCDS': CCDS,
    'PUBMED': PUBMED,
    'NCBIGENE': NCBIGENE,
    'MIM': MIM,
    'EMSEMBL': ENSEMBL
}
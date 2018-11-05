import unittest

from jsonasobj import as_json

from biolinkmodel import datamodel
from biolinkmodel.utils.extended_datamodel import KG
from biolinkmodel.utils.namespaces import CCDS, PUBMED, UNIPROT, NCBIGENE, MIM, ENSEMBL, MGI, NUCC
from metamodel.utils.namespaces import HGNC


class BiolinkModelConstructorTestCase(unittest.TestCase):

    def test_simple_model(self):
        knowledge_graph = KG(id=HGNC)
        knowledge_graph.kg_source = "Test"

        # {
        #     "@id" : "http://data2services/model/association/homology/0000794741fef27a48583ffa57bba3d3",
        #     "@type" : [ "http://bioentity.io/vocab/GeneToGeneHomologyAssociation" ],
        #     "http://bioentity.io/vocab/gene_to_gene_association_object" : [ {
        #       "@id" : "http://identifiers.org/mgi/MGI:1925179"
        #     } ],
        #     "http://bioentity.io/vocab/gene_to_gene_association_subject" : [ {
        #       "@id" : "http://identifiers.org/hgnc:28304"
        #     } ],
        #     "http://bioentity.io/vocab/relation" : [ {
        #       "@id" : "http://bioentity.io/vocab/homologous_to"
        #     } ]
        #   }
        knowledge_graph.add_association(datamodel.GeneToGeneHomologyAssociation,
                                        HGNC["28304"], MGI["1925179"])

        # {
        #     "@id" : "http://data2services/model/association/transcript/d360d2e95faaa55bcc4ec856acd05652",
        #     "@type" : [ "http://bioentity.io/vocab/TranscriptToGeneRelationship" ],
        #     "http://bioentity.io/vocab/transcript_to_gene_relationship_object" : [ {
        #       "@id" : "http://identifiers.org/hgnc:10388"
        #     } ],
        #     "http://bioentity.io/vocab/transcript_to_gene_relationship_subject" : [ {
        #       "@id" : "https://www.ncbi.nlm.nih.gov/nuccore/NM_001018"
        #     } ]
        #   }
        # TODO: what relationship should be used
        knowledge_graph.add_association(datamodel.TranscriptToGeneRelationship,
                                        NUCC.NM_001018, HGNC['10388'], 'expresses')

        # "@id" : "http://identifiers.org/hgnc:10388",
        #     "@type" : [ "http://bioentity.io/vocab/Gene" ],
        #     "http://bioentity.io/vocab/category" : [ {
        #       "@value" : "gene with protein product"
        #     }, {
        #       "@value" : "protein-coding gene"
        #     } ],
        #     "http://bioentity.io/vocab/filler" : [ {
        #       "@id" : "http://data2services/model/status/Approved"
        #     }, {
        #       "@id" : "https://data2services/model/gene-family/RPS"
        #     } ],
        #     "http://bioentity.io/vocab/has_gene_product" : [ {
        #       "@id" : "http://identifiers.org/uniprot/P62841"
        #     } ],
        #     "http://bioentity.io/vocab/id" : [ {
        #       "@value" : "HGNC:10388"
        #     } ],
        #     "http://bioentity.io/vocab/iri" : [ {
        #       "@id" : "http://identifiers.org/hgnc:10388"
        #     } ],
        #     "http://bioentity.io/vocab/located_in" : [ {
        #       "@id" : "http://identifiers.org/ccds/CCDS12067"
        #     } ],
        #     "http://bioentity.io/vocab/name" : [ {
        #       "@value" : "ribosomal protein S15"
        #     } ],
        #     "http://bioentity.io/vocab/publications" : [ {
        #       "@id" : "http://identifiers.org/pubmed/2159154"
        #     } ],
        #     "http://bioentity.io/vocab/same_as" : [ {
        #       "@id" : "https://www.ncbi.nlm.nih.gov/gene/6209"
        #     }, {
        #       "@id" : "http://identifiers.org/mim/180535"
        #     }, {
        #       "@id" : "http://identifiers.org/ensembl/ENSG00000115268"
        #     } ],
        #     "http://bioentity.io/vocab/systematic_synonym" : [ {
        #       "@value" : "RPS15"
        #     } ],
        #     "http://bioentity.io/vocab/update_date" : [ {
        #       "@value" : "2014-11-19"
        #     } ],
        #     "http://data2services/vocab/Status" : [ {
        #       "@value" : "Approved"
        #     } ],
        #     "http://www.w3.org/2000/01/rdf-schema#label" : [ {
        #       "@value" : "ribosomal protein S15"
        #     } ]
        #   }
        thing = knowledge_graph.add_entity(datamodel.Gene, HGNC['10388'])
        thing.category = ['gene with gene product', 'protein-coding gene']
        thing.filler = ["http://data2services/model/status/Approved", "https://data2services/model/gene-family/RPS"]
        thing.located_in = CCDS.CCDS12067
        thing.publications = [PUBMED["159154"]]
        thing.has_gene_product = UNIPROT.P62841
        thing.name = "ribosomal protein S15"
        thing.systematic_synonym = "RPS15"
        thing.same_as = [NCBIGENE['6209'], MIM['180535'], ENSEMBL.ENSG00000115268]
        thing.update_date = "2014-11-19"

        print(as_json(knowledge_graph))
        print(knowledge_graph.as_rdf(strip_prefixes=True))


if __name__ == '__main__':
    unittest.main()

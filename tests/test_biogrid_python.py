import unittest

from jsonasobj import as_json, JsonObj


from biolinkmodel import datamodel
from rdflib import Namespace, Graph, BNode

HGNC = Namespace('http://identifiers.org/hgnc#')
MGI = Namespace('http://www.informatics.jax.org/accession/MGI:')
BIO = Namespace('http://bioentity.io/vocab/')
homology = Namespace('http://data2services/model/association/homology/')
transcript = Namespace('http://data2services/model/association/transcript/')
NUCC = Namespace('https://www.ncbi.nlm.nih.gov/nuccore/')


class BiolinkModelConstructorTestCase(unittest.TestCase):

    def test_simple_model(self):
        knowledge_graph = datamodel.KnowledgeGraph(id=homology.a1)
        knowledge_graph['@context'] = "../context.jsonld"
        knowledge_graph.prefixes['HGNC'] = HGNC
        knowledge_graph.entities[BNode()] = datamodel.GeneToGeneHomologyAssociation(
            id = BIO.homologous_to,
            subject = HGNC["M28340"],
            object = MGI["1925179"],
            relation = BIO.homologous_to)

        knowledge_graph.entities[BNode()] = datamodel.TranscriptToGeneRelationship(
            id = BIO.affects_activity_of,
            subject=NUCC.NM_001018,
            object=HGNC['10388'],
            relation = BIO.affects_activity_of)
        print(as_json(knowledge_graph))
        g = Graph()
        g.namespace_manager.bind('MGI', MGI)
        g.namespace_manager.bind('HGNC', HGNC)
        g.parse(data=as_json(knowledge_graph), format="json-ld")

        print(g.serialize(format="turtle").decode())
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

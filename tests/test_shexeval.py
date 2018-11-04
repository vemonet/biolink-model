import os
import sys
import unittest

from CFGraph import CFGraph
from pyshex import ShExEvaluator
from rdflib import Graph, URIRef


class ShexEvalTestCase(unittest.TestCase):

    def shextest(self, rdf_file: str, shex_file: str, focus: str, cfgraph: bool=False) -> None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        g = CFGraph() if cfgraph else Graph()
        g.load(os.path.join(base_dir, 'rdf', rdf_file), format="turtle")
        evaluator = ShExEvaluator(g,
                                  os.path.join(base_dir, 'shex', shex_file),
                                  focus,
                                  "http://bioentity.io/vocab/SchemaDefinition")
        result = evaluator.evaluate(debug=False)
        for rslt in result:
            if not rslt.result:
                print(f"Error: {rslt.reason}")
        self.assertTrue(all(r.result for r in result))

    def test_meta_shexeval_no_collections(self):
        self.shextest("meta.ttl", "metanc.shex", "https://biolink.github.io/metamodel/ontology/meta.ttl", cfgraph=True)

    def test_meta_shexeval_collections(self):
        self.shextest("meta.ttl", "meta.shex", "https://biolink.github.io/metamodel/ontology/meta.ttl", cfgraph=False)

    def test_biolink_shexeval_no_collections(self):
        self.shextest("biolink-model.ttl", "metanc.shex",
                      "https://biolink.github.io/biolink-model/ontology/biolink.ttl", cfgraph=True)

    @unittest.skipIf(True, "Biolink collections tests have recursion problems")
    def test_biolink_shexeval_collections(self):
        self.shextest("biolink-model.ttl", "meta.shex",
                      "https://biolink.github.io/biolink-model/ontology/biolink.ttl", cfgraph=False)

    @unittest.skipIf(True, "Test data not ready to go")
    def test_drugbank_shex(self):
        source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source'))
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        g = CFGraph()
        g.load(os.path.join(base_dir, 'rdf', "biolink-model.ttl"), format="turtle")
        g.load(os.path.join(source_dir, 'biolink_drugbank.ttl'), format="turtle")
        evaluator = ShExEvaluator(g,
                                  os.path.join(source_dir, '..', '..', 'shex', 'metanc.shex'),
                                  URIRef("http://identifiers.org/drugbank/DB00206"),
                                  "http://bioentity.io/vocab/Drug")
        result = evaluator.evaluate(debug=True)
        for rslt in result:
            if not rslt.result:
                print(f"Error: {rslt.reason}")
        self.assertTrue(all(r.result for r in result))

    @unittest.skipIf(False, "Test data not ready to go")
    def test_hgnc_shex(self):
        # http://identifiers.org/hgnc:20394>
        source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source'))
        g = Graph()
        g.load(os.path.join(source_dir, 'biolink-hgnc.jsonld'), format="json-ld")
        evaluator = ShExEvaluator(g,
                                  os.path.join(source_dir, '..', '..', 'shex', 'biolink-model.shex'),
                                  URIRef("<http://identifiers.org/hgnc:20394>"),
                                  "http://bioentity.io/vocab/Gene")
        result = evaluator.evaluate(debug=False)
        for rslt in result:
            if not rslt.result:
                print(f"Error: {rslt.reason}")
        self.assertTrue(all(r.result for r in result))



if __name__ == '__main__':
    unittest.main()

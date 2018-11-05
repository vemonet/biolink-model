import re
from typing import Optional, Union, Dict, Type

from jsonasobj import as_json
from rdflib import URIRef, BNode, Graph

from biolinkmodel import context_jsonld_loc
from biolinkmodel.datamodel import KnowledgeGraph, Association, GeneToGeneHomologyAssociation, NamedThing
from biolinkmodel.utils.namespaces import BIOENTITY, namespace_map

relation_defaults: Dict[Association, URIRef] = {GeneToGeneHomologyAssociation: BIOENTITY.homologous_to}


class KG(KnowledgeGraph):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self['@context'] = context_jsonld_loc

    @staticmethod
    def get_slot_type(slot: str, cls: Type[Association]) -> Optional[Type[NamedThing]]:
        if slot in cls.__annotations__:
            return cls.__annotations__['subject']
        else:
            for base in cls.__bases__:
                typ = KG.get_slot_type(slot, base)
                if typ:
                    return typ
        return None


    def add_association(self, cls: Type[Association], subject: URIRef, object_: URIRef,
                        relation: Optional[Union[str, URIRef]]=None) -> Association:
        id_ = BNode()
        if not relation:
            relation = relation_defaults.get(cls)
            if not relation:
                raise ValueError("relation parameter must be supplied")
        subj_type = self.get_slot_type('subject', cls)
        # if subject not in self.entities:
        #     self.entities[subject] = subj_type()
        relation = BIOENTITY[relation] if not isinstance(relation, URIRef) else relation
        assoc = cls(id=id_, subject=subject, object=object_, relation=relation)
        self.relationship_types[assoc.id] = assoc
        return assoc

    def add_entity(self, cls: Type[NamedThing], id_: URIRef) -> NamedThing:
        thing = cls(id=id_)
        self.entities[id_] = thing
        return thing

    def as_rdf(self, strip_prefixes: bool=False, **kwargs) -> str:
        g = Graph()
        for ns in namespace_map.keys():
            g.bind(ns, namespace_map[ns])
        g.parse(data=as_json(self), format="json-ld")
        rval = g.serialize(format="turtle", **kwargs).decode()
        if strip_prefixes:
            rval = re.sub(r'^@prefix .*\n', '', rval, flags=re.MULTILINE )
        return rval

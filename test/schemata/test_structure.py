import unittest
from lxml import etree as ET

class StructureTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = ET.RelaxNG(file="./../../schemata/problem-structure.rng")
    
    def test_valid_structures(self):

        structures = ["valid-structure-1.xml",
                      "valid-structure-2.xml"]
        for i, structure in enumerate(structures):
            with self.subTest(i=i+1):
                parsed = ET.parse(structure)
                self.schema.assertValid(parsed)

    def test_invalid_structures(self):
        pass
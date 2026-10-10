import unittest

from pipeline.specsense.parser import OutputParser


class OutputParserTests(unittest.TestCase):
    def test_parses_multiple_recommendations_from_json_array(self):
        llm_output = '''
        Here are the top recommendations:
        [
          {
            "product_name": "Laptop A",
            "prod_desc": "Lightweight laptop",
            "price": 29999,
            "rating": 4.5,
            "hard_matches": ["16GB RAM"],
            "soft_matches": ["Lightweight"],
            "trade_offs": ["Slightly above budget"],
            "Unmet_needs": ["No dedicated GPU"]
          },
          {
            "product_name": "Laptop B",
            "prod_desc": "Balanced performer",
            "price": 34999,
            "rating": 4.2,
            "hard_matches": ["Intel i5"],
            "soft_matches": ["Good battery"],
            "trade_offs": ["Average display"],
            "Unmet_needs": ["No SSD"]
          },
          {
            "product_name": "Laptop C",
            "prod_desc": "Budget friendly option",
            "price": 24999,
            "rating": 4.0,
            "hard_matches": ["Under budget"],
            "soft_matches": ["Good value"],
            "trade_offs": ["Lower rating"],
            "Unmet_needs": ["Less RAM"]
          }
        ]
        '''

        parser = OutputParser()
        result = parser.parse_llm_output(llm_output)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["product_name"], "Laptop A")
        self.assertEqual(result[1]["product_name"], "Laptop B")
        self.assertEqual(result[2]["product_name"], "Laptop C")


if __name__ == "__main__":
    unittest.main()

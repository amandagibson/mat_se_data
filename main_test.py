import unittest
import main


class MatAPI(unittest.TestCase):
    def test_get_category_ids(self):
        category_ids = main.get_category_ids()
        self.assertEqual(21, len(category_ids))

    def test_get_products_grouped_by_categories(self):
        grouped_products = main.get_products_grouped_by_category()
        self.assertEqual(21, len(grouped_products))

    def test_get_percentage_of_swedish_products_per_category(self):
        swedish_products = main.get_percentage_of_swedish_products_per_category()
        self.assertEqual(21, len(swedish_products))

    def test_get_number_of_products_per_category(self):
        products = main.get_number_of_products_per_category()
        self.assertEqual(21, len(products))

    def test_get_products_with_highest_co2_emission(self):
        emission_products = main.get_products_with_highest_co2_emission()
        self.assertEqual(21, len(emission_products))

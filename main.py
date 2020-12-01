import requests
from operator import itemgetter
import json


def get_subcategories():
    all_categories_response = requests.get("https://mat.se/api/product/getCategoryTree")
    all_categories_structured_response = all_categories_response.json()
    subcategories = all_categories_structured_response['subCategories']
    return subcategories


def get_category_ids():
    subcategories = get_subcategories()
    subcategory_ids = []
    for categories in subcategories:
        if categories['id'] is None:
            continue
        else:
            subcategory_ids.append({'id': categories['id'], 'category': categories['name']})
    return subcategory_ids


def get_products_grouped_by_category():
    category_ids = get_category_ids()
    all_products_grouped_by_category = []
    for category_id in category_ids:
        api_response = requests.get(f"https://mat.se/api/product/listByCategory?categoryId={category_id['id']}")
        category_response = api_response.json()
        all_products_grouped_by_category.append({'products': category_response, 'category': category_id['category']})
    return all_products_grouped_by_category


def get_percentage_of_swedish_products_per_category():
    products_per_category = get_products_grouped_by_category()
    percentage_of_swedish_products_per_category = []
    for product_group in products_per_category:
        number_of_products = 0
        number_of_swedish_products = 0
        for product in product_group['products']:
            number_of_products += 1
            if product['countryOfOrigin'] == 'SE':
                number_of_swedish_products += 1
        percentage = ((number_of_swedish_products / number_of_products) * 100)
        percentage_of_swedish_products_per_category.append(
            {'category': product_group['category'], 'percentage, swedish': percentage})
    return percentage_of_swedish_products_per_category


def get_number_of_products_per_category():
    subcategory_details = get_subcategories()
    number_of_products_per_category = []
    for single_category_details in subcategory_details:
        number_of_products = single_category_details['count']
        number_of_products_per_category.append(
            {'category': single_category_details['name'], 'number of products': number_of_products})
    return number_of_products_per_category


def get_products_with_highest_co2_emission():
    products_per_category = get_products_grouped_by_category()
    highest_emission_products = []
    for product_group in products_per_category:
        co2_values = []
        for product in product_group['products']:
            co2_values.append({'product': product['name'], 'emission': product['emission']})
        sorted_list = sorted(co2_values, key=itemgetter('emission'), reverse=True)
        highest_emission_products.append({'category': product_group['category'], 'products': sorted_list[:5]})
    return highest_emission_products


def export_data_to_files():
    percentage_of_swedish_products = get_percentage_of_swedish_products_per_category()
    number_of_products_per_category = get_number_of_products_per_category()
    highest_co2_emission_products = get_products_with_highest_co2_emission()
    with open('percentage_of_swedish_products.json', 'w') as f:
        json.dump(percentage_of_swedish_products, f, ensure_ascii=False, indent=4, sort_keys=True)
    with open('number_of_products.json', 'w') as f:
        json.dump(number_of_products_per_category, f, ensure_ascii=False, indent=4, sort_keys=True)
    with open('products_with_highest_emission.json', 'w')as f:
        json.dump(highest_co2_emission_products, f, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    export_data_to_files()

from flask import Flask, jsonify, request
import threading
import hashlib

app = Flask(__name__)

COMPANIES = ['company1', 'company2', 'company3', 'company4', 'company5']
TIMEOUT = 1.0

lock = threading.Lock()

def mock_fetch_products(company, category):
    mock_products = [
        {'name': f'Product {i}', 'price': 10.0 + i, 'rating': 4.5, 'discount': 0.0} for i in range(1, 11)
    ]
    return mock_products

def generate_unique_id(product):
    product_string = f"{product['name']}-{product['company']}-{product['price']}"
    return hashlib.md5(product_string.encode()).hexdigest()

@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_top_products(categoryname):
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sort_by', 'rating')
    order = request.args.get('order', 'desc')
    
    all_products = []

    with lock:
        for company in COMPANIES:
            products = mock_fetch_products(company, categoryname)
            for product in products:
                product['company'] = company
                product['id'] = generate_unique_id(product)
            all_products.extend(products)

    if sort_by in ['rating', 'price', 'discount']:
        all_products.sort(key=lambda x: x.get(sort_by, 0), reverse=(order == 'desc'))
    elif sort_by == 'company':
        all_products.sort(key=lambda x: x.get(sort_by, ''), reverse=(order == 'desc'))

    total_products = len(all_products)
    start = (page - 1) * n
    end = start + n
    paginated_products = all_products[start:end]

    return jsonify({
        'total': total_products,
        'page': page,
        'page_size': n,
        'products': paginated_products
    })

@app.route('/categories/<categoryname>/products/<productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    for company in COMPANIES:
        products = mock_fetch_products(company, categoryname)
        for product in products:
            product['company'] = company
            product['id'] = generate_unique_id(product)
            if product['id'] == productid:
                return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

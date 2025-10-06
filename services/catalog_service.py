from services.models import db, Product, RunningShoe, EverydayShoe, OfficialShoe, MountainShoe


def add_product(name, description, color, sizes, price, stock, category=None):
    """
    Factory pattern - creates appropriate product type based on category
    """
    if category == 'running':
        product = RunningShoe()
    elif category == 'everyday':
        product = EverydayShoe()
    elif category == 'official':
        product = OfficialShoe()
    elif category == 'mountain':
        product = MountainShoe()
    else:
        product = Product()

    # Set attributes
    product.name = name
    product.description = description
    product.color = color
    product.sizes = sizes
    product.price = float(price)
    product.stock = int(stock)

    db.session.add(product)
    db.session.commit()
    return product


def list_products(query=None, color=None, min_price=None, max_price=None, size=None,
                  in_stock=False, category=None, sort_by=None):
    """
    List products with filtering and sorting using SQLAlchemy queries
    """
    # Start with base query
    products_query = Product.query

    # Apply filters
    if query:
        products_query = products_query.filter(
            db.or_(
                Product.name.ilike(f'%{query}%'),
                Product.color.ilike(f'%{query}%')
            )
        )

    if color:
        products_query = products_query.filter(Product.color.ilike(f'%{color}%'))

    if min_price is not None:
        products_query = products_query.filter(Product.price >= min_price)

    if max_price is not None:
        products_query = products_query.filter(Product.price <= max_price)

    if in_stock:
        products_query = products_query.filter(Product.stock > 0)

    # Category filter using polymorphic identity
    if category:
        products_query = products_query.filter(Product.product_type == category)

    # Apply sorting
    if sort_by == 'name_asc':
        products_query = products_query.order_by(Product.name.asc())
    elif sort_by == 'name_desc':
        products_query = products_query.order_by(Product.name.desc())
    elif sort_by == 'price_asc':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.price.desc())
    else:
        products_query = products_query.order_by(Product.id.asc())

    # Execute query and get results
    results = products_query.all()

    # Filter by size (done in Python because sizes is a PickleType)
    if size is not None:
        results = [p for p in results if p.sizes and size in p.sizes]

    return results


def get_product(product_id):
    """Get product by ID"""
    return Product.query.get(product_id)


def get_product_category(product):
    """
    Polymorphism - Returns category name based on product type
    """
    if isinstance(product, RunningShoe):
        return 'running'
    elif isinstance(product, EverydayShoe):
        return 'everyday'
    elif isinstance(product, OfficialShoe):
        return 'official'
    elif isinstance(product, MountainShoe):
        return 'mountain'
    return 'general'


def update_product(product_id, name=None, description=None, color=None,
                   sizes=None, price=None, stock=None):
    """Update product details"""
    product = get_product(product_id)
    if not product:
        return None

    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if color is not None:
        product.color = color
    if sizes is not None:
        product.sizes = sizes
    if price is not None:
        product.price = float(price)
    if stock is not None:
        product.stock = int(stock)

    db.session.commit()
    return product


def delete_product(product_id):
    """Delete product"""
    product = get_product(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return True
    return False
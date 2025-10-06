from services.models import db, User, Product
from services.auth_service import create_user
from services.catalog_service import add_product


def init_sample_data():
    """Initialize sample users and products if database is empty"""

    # Check if data already exists
    if User.query.first() is not None:
        print("Database already initialized")
        return

    print("Initializing database with sample data...")

    # Create sample users
    create_user("admin@example.com", "admin123", is_admin=True)
    create_user("user1@example.com", "user123", is_admin=False)
    create_user("user2@example.com", "user123", is_admin=False)

    print("✓ Sample users created")

    # Create sample products
    add_product(
        "AirMax Runner",
        "Lightweight running shoes",
        "Black",
        [40, 41, 42, 43],
        89.99,
        10,
        "running"
    )

    add_product(
        "Classic Sneakers",
        "Everyday casual sneakers",
        "White",
        [38, 39, 40, 41, 42],
        59.99,
        15,
        "everyday"
    )

    add_product(
        "Mountain Boots",
        "Durable boots for hiking",
        "Brown",
        [42, 43, 44, 45],
        120.00,
        5,
        "mountain"
    )

    add_product(
        "Speed Racer",
        "Professional racing shoes",
        "Red",
        [39, 40, 41, 42],
        129.99,
        8,
        "running"
    )

    add_product(
        "Oxford Classic",
        "Elegant formal shoes",
        "Black",
        [40, 41, 42, 43, 44],
        149.99,
        12,
        "official"
    )

    add_product(
        "Comfort Walk",
        "All-day comfort sneakers",
        "Gray",
        [37, 38, 39, 40, 41],
        69.99,
        20,
        "everyday"
    )

    print("✓ Sample products created")
    print("Database initialization complete!")
    print("\nDefault login credentials:")
    print("Admin: admin@example.com / admin123")
    print("User1: user1@example.com / user123")
    print("User2: user2@example.com / user123")
from models import Item, Category, Transaction, Customer


def test_order_totals():
    """Test that transaction total cost is calculated correctly."""
    drinks = Category("Drinks")
    desserts = Category("Desserts")
    cola = Item("Cola", 1.50, drinks)
    pie = Item("Apple Pie", 3.00, desserts)
    
    transaction = Transaction()
    transaction.add_item(cola)
    transaction.add_item(pie)
    
    assert transaction.total_cost() == 4.50


def test_empty_totals():
    """Test that an empty transaction has a total cost of 0."""
    transaction = Transaction()
    assert transaction.total_cost() == 0.0
    assert len(transaction) == 0


def test_filter_menu_items_by_category():
    """Test filtering items by category."""
    drinks = Category("Drinks")
    desserts = Category("Desserts")
    cola = Item("Cola", 1.50, drinks)
    soda = Item("Soda", 1.25, drinks)
    pie = Item("Apple Pie", 3.00, desserts)
    
    all_items = [cola, soda, pie]
    
    # Filter by drinks category
    drinks_items = Item.filter_by_category(all_items, drinks)
    assert len(drinks_items) == 2
    assert cola in drinks_items
    assert soda in drinks_items
    assert pie not in drinks_items
    
    # Filter by desserts category
    desserts_items = Item.filter_by_category(all_items, desserts)
    assert len(desserts_items) == 1
    assert pie in desserts_items


def test_category_filter():
    """Test Category.filter() method."""
    drinks = Category("Drinks")
    cola = Item("Cola", 1.50, drinks)
    soda = Item("Soda", 1.25, drinks)
    
    filtered = drinks.filter()
    assert len(filtered) == 2
    assert cola in filtered
    assert soda in filtered


def test_item_sorting():
    """Test sorting items by price, popularity, and name."""
    drinks = Category("Drinks")
    cola = Item("Cola", 1.50, drinks, popularity_rating=4)
    soda = Item("Soda", 1.25, drinks, popularity_rating=3)
    
    items = [cola, soda]
    
    # Sort by price ascending
    sorted_price = Item.sort_by_price(items, ascending=True)
    assert sorted_price[0].name == "Soda"
    assert sorted_price[1].name == "Cola"
    
    # Sort by popularity descending
    sorted_pop = Item.sort_by_popularity(items, descending=True)
    assert sorted_pop[0].name == "Cola"
    assert sorted_pop[1].name == "Soda"
    
    # Sort by name
    sorted_name = Item.sort_by_name(items)
    assert sorted_name[0].name == "Cola"
    assert sorted_name[1].name == "Soda"


def test_customer_validity():
    """Test customer validity based on name and transaction history."""
    customer = Customer("Alice")
    assert not customer.is_valid()  # No transactions
    
    transaction = Transaction()
    customer.add_transaction(transaction)
    assert customer.is_valid()  # Now has a transaction
    
    invalid_customer = Customer("")
    invalid_customer.add_transaction(transaction)
    assert not invalid_customer.is_valid()  # Empty name

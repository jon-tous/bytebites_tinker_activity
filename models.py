# Backend models for ByteBites application
#
# Customer: tracks a user's name and a history of their transactions (purchase history).
# Item: represents a food/drink offered by ByteBites, with name, price, category,
#       and a popularity rating.
# Category: groups items by type (e.g. Drinks, Desserts) and supports filtering the
#           catalogue of items.
# Transaction: bundles selected items for a purchase and can compute the total cost.

from __future__ import annotations
from typing import List, Optional


class Item:
    """A food or drink offered by ByteBites."""

    def __init__(self, name: str, price: float, category: "Category",
                 popularity_rating: int = 0) -> None:
        if price < 0:
            raise ValueError("price must be non-negative")
        if not (0 <= popularity_rating <= 5):
            raise ValueError("popularity_rating must be between 0 and 5")
        self._name = name
        self._price = price
        self._popularity_rating = popularity_rating
        # assign category and register self with it; ensures the
        # bidirectional relationship stays consistent
        self._category: Category = category
        category.add_item(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def category(self) -> "Category":
        return self._category

    @property
    def popularity_rating(self) -> int:
        return self._popularity_rating

    def __repr__(self) -> str:
        return f"Item(name={self._name!r}, price={self._price}, category={self._category.name!r})"

    @staticmethod
    def sort_by_price(items: List[Item], ascending: bool = True) -> List[Item]:
        """Sort items by price.
        
        Args:
            items: List of Item objects to sort.
            ascending: If True, sort lowest to highest; if False, highest to lowest.
        
        Returns:
            New sorted list of items.
        """
        return sorted(items, key=lambda item: item.price, reverse=not ascending)

    @staticmethod
    def sort_by_popularity(items: List[Item], descending: bool = True) -> List[Item]:
        """Sort items by popularity rating.
        
        Args:
            items: List of Item objects to sort.
            descending: If True, sort highest to lowest; if False, lowest to highest.
        
        Returns:
            New sorted list of items.
        """
        return sorted(items, key=lambda item: item.popularity_rating, reverse=descending)

    @staticmethod
    def sort_by_name(items: List[Item]) -> List[Item]:
        """Sort items alphabetically by name.
        
        Args:
            items: List of Item objects to sort.
        
        Returns:
            New sorted list of items in alphabetical order.
        """
        return sorted(items, key=lambda item: item.name)

    @staticmethod
    def filter_by_category(items: List[Item], category: "Category") -> List[Item]:
        """Filter items by category.
        
        Args:
            items: List of Item objects to filter.
            category: The Category to filter by.
        
        Returns:
            New list containing only items in the specified category.
        """
        return [item for item in items if item.category == category]


class Category:
    """Group of related items (e.g. Drinks, Desserts)."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._items: List[Item] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def items(self) -> List[Item]:
        # return a copy to prevent external mutation
        return list(self._items)

    def add_item(self, item: Item) -> None:
        """Add an item to this category and set the item's category.
        If the item previously belonged to another category, its reference
        will be updated; duplicates are ignored."""
        if item not in self._items:
            self._items.append(item)
            item._category = self

    def filter(self) -> List[Item]:
        """Return all items in this category."""
        return self.items

    def __repr__(self) -> str:
        return f"Category(name={self._name!r}, items={len(self._items)})"


class Transaction:
    """A collection of items that constitute a single purchase."""

    def __init__(self) -> None:
        self._items: List[Item] = []

    @property
    def items(self) -> List[Item]:
        return list(self._items)

    def add_item(self, item: Item) -> None:
        self._items.append(item)

    def total_cost(self) -> float:
        return sum(item.price for item in self._items)

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Transaction(total={self.total_cost():.2f}, items={len(self._items)})"

    @staticmethod
    def sort_by_total(transactions: List[Transaction], descending: bool = True) -> List[Transaction]:
        """Sort transactions by total cost.
        
        Args:
            transactions: List of Transaction objects to sort.
            descending: If True, sort highest to lowest; if False, lowest to highest.
        
        Returns:
            New sorted list of transactions.
        """
        return sorted(transactions, key=lambda t: t.total_cost(), reverse=descending)


class Customer:
    """Represents a user of ByteBites with a purchase history."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._purchase_history: List[Transaction] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def purchase_history(self) -> List[Transaction]:
        return list(self._purchase_history)

    def add_transaction(self, transaction: Transaction) -> None:
        self._purchase_history.append(transaction)

    def is_valid(self) -> bool:
        """Basic sanity: nonempty name and at least one past transaction.
        This helps identify "real" users per the spec."""
        return bool(self._name and self._name.strip() and self._purchase_history)

    def __repr__(self) -> str:
        return f"Customer(name={self._name!r}, transactions={len(self._purchase_history)})"


# simple demonstration script; run this module directly to sanity-check behaviour
if __name__ == "__main__":
    # Create categories
    drinks = Category("Drinks")
    desserts = Category("Desserts")

    # Add items (they auto-register with categories)
    cola = Item("Cola", 1.50, drinks, popularity_rating=4)
    soda = Item("Soda", 1.25, drinks, popularity_rating=3)
    pie = Item("Apple Pie", 3.00, desserts, popularity_rating=5)
    burger = Item("Spicy Burger", 5.25, desserts, popularity_rating=3)
    cake = Item("Chocolate Cake", 4.50, desserts, popularity_rating=4)

    # Collect all items for sorting/filtering demos
    all_items = [cola, soda, pie, burger, cake]

    print("=== All Items ===")
    for item in all_items:
        print(f"  {item}")

    print("\n=== Sorting Items by Price (Ascending) ===")
    sorted_price = Item.sort_by_price(all_items, ascending=True)
    for item in sorted_price:
        print(f"  {item}")

    print("\n=== Sorting Items by Popularity (Descending) ===")
    sorted_popular = Item.sort_by_popularity(all_items, descending=True)
    for item in sorted_popular:
        print(f"  {item}")

    print("\n=== Sorting Items by Name ===")
    sorted_name = Item.sort_by_name(all_items)
    for item in sorted_name:
        print(f"  {item}")

    print("\n=== Filtering Items by Category (Desserts) ===")
    desserts_items = Item.filter_by_category(all_items, desserts)
    for item in desserts_items:
        print(f"  {item}")

    print("\n=== Category Filter (Drinks) ===")
    drinks_items = drinks.filter()
    for item in drinks_items:
        print(f"  {item}")

    # Build a transaction (customer order)
    order = Transaction()
    order.add_item(cola)
    order.add_item(pie)
    order.add_item(cake)

    print("\n=== Customer Order ===")
    for item in order.items:
        print(f"  {item}")
    print(f"Total Cost: ${order.total_cost():.2f}")

    # Customer with transaction history
    customer = Customer("Alice")
    customer.add_transaction(order)
    print(f"\nCustomer: {customer}")
    print(f"Is Valid: {customer.is_valid()}")

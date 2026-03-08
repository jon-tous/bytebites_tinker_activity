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
        """Return all items in this category.
        (placeholder for more complex filtering later)"""
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
    # create categories
    drinks = Category("Drinks")
    desserts = Category("Desserts")

    # items automatically add themselves to their category
    cola = Item("Cola", 1.50, drinks, popularity_rating=4)
    pie = Item("Apple Pie", 3.00, desserts, popularity_rating=5)
    burger = Item("Spicy Burger", 5.25, desserts, popularity_rating=3)

    # category contents
    print("Drinks category contains:", drinks.items)
    print("Desserts category contains:", desserts.items)

    # build a transaction
    t1 = Transaction()
    t1.add_item(cola)
    t1.add_item(burger)
    print("Transaction 1 items:", t1.items)
    print("Transaction 1 total:", t1.total_cost())

    # second transaction
    t2 = Transaction()
    t2.add_item(pie)
    print("Transaction 2 total:", t2.total_cost())

    # customer with history
    cust = Customer("Alice")
    cust.add_transaction(t1)
    cust.add_transaction(t2)
    print("Customer record:", cust)
    print("Purchase history:", cust.purchase_history)
    print("Is customer valid?", cust.is_valid())

    # expectations for manual check:
    # - drinks category should list cola only
    # - desserts category should contain pie and burger
    # - t1 total should equal 6.75
    # - t2 total should equal 3.0
    # - customer.history length should be 2 and is_valid True

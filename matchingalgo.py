from collections import deque
from datetime import datetime

class Order:
    def __init__(self, order_id, timestamp, side, price, quantity, order_type):
        self.order_id = order_id  # Unique identifier
        self.timestamp = timestamp  # Time when the order was placed
        self.side = side  # 'buy' or 'sell'
        self.price = price  # Price of the order (None for market orders)
        self.quantity = quantity  # Quantity of the order
        self.order_type = order_type  # 'limit' or 'market'

class OrderBook:
    def __init__(self):
        # Lists of tuples: (price, deque of orders), sorted appropriately
        self.buy_orders = []   # Sorted in descending order of price
        self.sell_orders = []  # Sorted in ascending order of price
        self.order_id_counter = 0

    def add_order(self, side, price, quantity, order_type):
        self.order_id_counter += 1
        timestamp = datetime.now().timestamp()
        order = Order(
            order_id=self.order_id_counter,
            timestamp=timestamp,
            side=side,
            price=price,
            quantity=quantity,
            order_type=order_type
        )
        self.process_order(order)

    def process_order(self, order):
        if order.side == 'buy':
            self.match_buy_order(order)
        elif order.side == 'sell':
            self.match_sell_order(order)

    def match_buy_order(self, order):
        # Attempt to match the buy order with existing sell orders
        while order.quantity > 0 and self.sell_orders:
            best_sell_price, sell_queue = self.sell_orders[0]  # Lowest sell price
            if order.order_type == 'limit' and (best_sell_price > order.price):
                break  # Cannot match, as best sell price is higher than buy price

            if order.order_type == 'market' or best_sell_price <= order.price:
                best_sell_order = sell_queue[0]
                traded_quantity = min(order.quantity, best_sell_order.quantity)

                # Execute trade
                order.quantity -= traded_quantity
                best_sell_order.quantity -= traded_quantity
                print(f"Trade executed: Buy Order {order.order_id} matched with Sell Order {best_sell_order.order_id}, "
                      f"Quantity: {traded_quantity}, Price: {best_sell_price}")

                # Remove fully filled sell orders
                if best_sell_order.quantity == 0:
                    sell_queue.popleft()
                    if not sell_queue:
                        self.sell_orders.pop(0)

                if order.quantity == 0:
                    return
            else:
                break  # No matching sell orders at acceptable prices

        # Add remaining limit order to the book
        if order.quantity > 0 and order.order_type == 'limit':
            self.add_to_order_book(order, self.buy_orders, reverse=True)
        elif order.quantity > 0:
            print(f"Market buy order {order.order_id} could not be fully filled; remaining quantity: {order.quantity}")

    def match_sell_order(self, order):
        # Attempt to match the sell order with existing buy orders
        while order.quantity > 0 and self.buy_orders:
            best_buy_price, buy_queue = self.buy_orders[0]  # Highest buy price
            if order.order_type == 'limit' and (best_buy_price < order.price):
                break  # Cannot match, as best buy price is lower than sell price

            if order.order_type == 'market' or best_buy_price >= order.price:
                best_buy_order = buy_queue[0]
                traded_quantity = min(order.quantity, best_buy_order.quantity)

                # Execute trade
                order.quantity -= traded_quantity
                best_buy_order.quantity -= traded_quantity
                print(f"Trade executed: Sell Order {order.order_id} matched with Buy Order {best_buy_order.order_id}, "
                      f"Quantity: {traded_quantity}, Price: {best_buy_price}")

                # Remove fully filled buy orders
                if best_buy_order.quantity == 0:
                    buy_queue.popleft()
                    if not buy_queue:
                        self.buy_orders.pop(0)

                if order.quantity == 0:
                    return
            else:
                break  # No matching buy orders at acceptable prices

        # Add remaining limit order to the book
        if order.quantity > 0 and order.order_type == 'limit':
            self.add_to_order_book(order, self.sell_orders, reverse=False)
        elif order.quantity > 0:
            print(f"Market sell order {order.order_id} could not be fully filled; remaining quantity: {order.quantity}")

    def add_to_order_book(self, order, order_list, reverse):
        # Add the order to the order book, maintaining price-time priority
        price_levels = [pl[0] for pl in order_list]
        if order.price in price_levels:
            index = price_levels.index(order.price)
            order_list[index][1].append(order)
        else:
            new_level = (order.price, deque([order]))
            order_list.append(new_level)
            order_list.sort(key=lambda x: x[0], reverse=reverse)

    def print_order_book(self):
        print("\nOrder Book:")
        print("Buy Orders:")
        for price, orders in self.buy_orders:
            total_quantity = sum(o.quantity for o in orders)
            print(f"  Price: {price}, Total Quantity: {total_quantity}")
        print("Sell Orders:")
        for price, orders in self.sell_orders:
            total_quantity = sum(o.quantity for o in orders)
            print(f"  Price: {price}, Total Quantity: {total_quantity}")
        print("\n")

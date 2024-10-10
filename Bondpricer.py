def bond_price(face_value, coupon_rate, periods, yield_to_maturity):
    """
    Calculate the price of a bond.

    Parameters:
    face_value (float): The bond's face value (e.g., 1000).
    coupon_rate (float): The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    periods (int): The number of periods until maturity.
    yield_to_maturity (float): The yield to maturity (as a decimal, e.g., 0.04 for 4%).

    Returns:
    float: The price of the bond.
    """
    coupon_payment = face_value * coupon_rate
    price = 0

    # Calculate the present value of the coupon payments
    for t in range(1, periods + 1):
        price += coupon_payment / (1 + yield_to_maturity) ** t

    # Calculate the present value of the face value (paid at maturity)
    price += face_value / (1 + yield_to_maturity) ** periods

    return price

def yield_to_maturity(face_value, coupon_rate, periods, market_price):
    """
    Estimate the yield to maturity (YTM) of a bond using an iterative approach.

    Parameters:
    face_value (float): The bond's face value (e.g., 1000).
    coupon_rate (float): The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    periods (int): The number of periods until maturity.
    market_price (float): The current market price of the bond.

    Returns:
    float: The estimated yield to maturity.
    """
    def bond_price_with_ytm(ytm):
        coupon_payment = face_value * coupon_rate
        price = 0

        for t in range(1, periods + 1):
            price += coupon_payment / (1 + ytm) ** t
        price += face_value / (1 + ytm) ** periods

        return price

    # Iteratively estimate the yield to maturity
    low, high = 0.0, 1.0
    tolerance = 1e-6
    while high - low > tolerance:
        mid = (low + high) / 2
        estimated_price = bond_price_with_ytm(mid)
        if estimated_price > market_price:
            high = mid
        else:
            low = mid

    return (low + high) / 2

def current_yield(face_value, coupon_rate, market_price):
    """
    Calculate the current yield of a bond.

    Parameters:
    face_value (float): The bond's face value (e.g., 1000).
    coupon_rate (float): The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    market_price (float): The current market price of the bond.

    Returns:
    float: The current yield of the bond.
    """
    coupon_payment = face_value * coupon_rate
    return coupon_payment / market_price

def duration(face_value, coupon_rate, periods, yield_to_maturity):
    """
    Calculate the Macaulay duration of a bond.

    Parameters:
    face_value (float): The bond's face value (e.g., 1000).
    coupon_rate (float): The annual coupon rate (as a decimal, e.g., 0.05 for 5%).
    periods (int): The number of periods until maturity.
    yield_to_maturity (float): The yield to maturity (as a decimal, e.g., 0.04 for 4%).

    Returns:
    float: The Macaulay duration of the bond.
    """
    coupon_payment = face_value * coupon_rate
    weighted_sum = 0
    price = bond_price(face_value, coupon_rate, periods, yield_to_maturity)

    for t in range(1, periods + 1):
        weighted_sum += (t * coupon_payment) / (1 + yield_to_maturity) ** t
    weighted_sum += (periods * face_value) / (1 + yield_to_maturity) ** periods

    return weighted_sum / price

if __name__ == "__main__":
    # Example usage
    face_value = 1000  # Face value of the bond
    coupon_rate = 0.05  # 5% annual coupon rate
    periods = 10  # 10 periods until maturity
    yield_to_maturity_value = 0.04  # 4% yield to maturity
    market_price = 950  # Current market price of the bond

    # Calculate bond price
    price = bond_price(face_value, coupon_rate, periods, yield_to_maturity_value)
    print(f"The price of the bond is: ${price:.2f}")

    # Estimate yield to maturity
    ytm = yield_to_maturity(face_value, coupon_rate, periods, market_price)
    print(f"The estimated yield to maturity is: {ytm:.4f}")

    # Calculate current yield
    current_yld = current_yield(face_value, coupon_rate, market_price)
    print(f"The current yield of the bond is: {current_yld:.4f}")

    # Calculate duration
    macaulay_duration = duration(face_value, coupon_rate, periods, yield_to_maturity_value)
    print(f"The Macaulay duration of the bond is: {macaulay_duration:.4f} years")
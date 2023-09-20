def find_combination(products, target, current_combination=[]):
    # If target is 0, we found a combination
    if target == 0:
        return current_combination
    # If no more products or negative target, no combination is found
    if not products or target < 0:
        return None
    # Try including the first product in the combination
    with_first = find_combination(products, target - products[0][1], current_combination + [products[0]])
    if with_first:
        return with_first
    # Try excluding the first product from the combination
    return find_combination(products[1:], target, current_combination)

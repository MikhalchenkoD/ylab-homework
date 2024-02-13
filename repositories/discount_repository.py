from database.models import Dish


class DiscountRepository:

    async def set_discount_for_dish(self, dish: Dish, discount: int) -> Dish:
        price = float(dish.price)
        discount_percentage = float(discount)
        discount_amount = (price * discount_percentage) / 100
        dish.price = str(round(price - discount_amount, 2))
        return dish

from .models import cart

def cart_context(request):
    user_id = request.session.get("user_id")

    if user_id:
        cart_items = cart.objects.filter(userid=user_id, orderstatus=1)
        cart_count = cart_items.count()
    else:
        cart_items = []
        cart_count = 0

    return {
        'cart_items': cart_items,
        'cart_count': cart_count
    }

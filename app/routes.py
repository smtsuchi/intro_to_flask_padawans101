from app import app
from flask import render_template, request
from flask_login import current_user
from .models import User, Product, Cart
from .apiauthhelper import token_required

@app.route('/')
def homePage():
    users = User.query.all()


    following_set = set()
    if current_user.is_authenticated:    
        who_i_am_following = current_user.followed.all()
        print(who_i_am_following)
        for u in who_i_am_following:
            following_set.add(u.id)
        
        for u in users:
            if u.id in following_set:
                u.flag = True
            


    return render_template('index.html', users=users)


@app.get('/api/products')
def getProductsAPI():
    products = Product.query.all()
    new_products = [p.to_dict() for p in products]
    return {
        'status': 'ok',
        'data': new_products,
        'total_results': len(new_products)
    }

@app.post('/api/cart/add')
@token_required
def addToCartAPI(user):
    data = request.json
    product_id = data['product_id']
    product = Product.query.get(product_id)
    if product:
        user.addToCart(product)
        return {
            'status': 'ok',
            'message': 'Succesfully added item to cart'
        }
    return {
        'status': 'not ok',
        'message': 'A product with that ID does not exist.'
    }

@app.get('/api/cart')
@token_required
def getCartAPI(user):
    cart = [Product.query.get(c.product_id).to_dict() for c in Cart.query.filter_by(user_id=user.id).all()]
    return {
        'status': 'ok',
        'cart': cart
    }

@app.post('/api/cart/remove')
@token_required
def removeFromCartAPI(user):
    data = request.json
    product_id = data['product_id']

    cart_item = Cart.query.filter_by(user_id=user.id).filter_by(product_id=product_id).first()
    if cart_item:
        cart_item.deleteFromDB()
        return {
            'status': 'ok',
            'message': 'Succesfully removed item from cart'
        }

   
#### STRIPE CHECKOUT ####
import stripe
from flask import redirect
import os
STRIPE_API_KEY=os.environ.get('STRIPE_API_KEY')
stripe.api_key = STRIPE_API_KEY

@app.post('/stripe')
def stripeCheckout():
    # receive ifno from react here
    data = request.form
    line_items = []
    for price_id, qty in data.items():
        line_items.append({
            'price': price_id,
            'quantity': qty
        })

    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url='https://padawans101.web.app/?success=true',
        cancel_url='https://padawans101.web.app/?cancel=true'
        )
    return redirect(checkout_session.url, code=303)

from app import application
from flask import jsonify, Response, session
from app.models import *
from app import *
import uuid
import datetime
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json


class SignUpRequest(Schema):
    name = fields.Str(default="name")
    username = fields.Str(default="username")
    password = fields.Str(default="userpass")
    level = fields.Int(default=0)


class LoginRequest(Schema):
    username = fields.Str(default="username")
    password = fields.Str(default="userpass")


class LogoutRequest(Schema):
    username = fields.Str(default="username")


class AddVendorRequest(Schema):
    user_id = fields.Str(default="user_id")


class VendorsListResponse(Schema):
    vendors = fields.List(fields.Dict())


class AddItemRequest(Schema):
    item_name = fields.Str(default="item name")
    restaurant_name = fields.Str(default="restaurant name")
    available_quantity = fields.Int(default=100)
    unit_price = fields.Int(default=100)
    calories_per_gm = fields.Int(default=10)


class PlaceOrderRequest(Schema):
    order_id = fields.Str(default="order id")


class GetOrdersByCustomerRequest(Schema):
    orders = fields.List(fields.Dict())


class OrdersListResponse(Schema):
    orders = fields.List(fields.Dict())


class ItemsListResponse(Schema):
    items = fields.List(fields.Dict())


class CreateOrderRequest(Schema):
    items = fields.List(fields.Dict())


class APIResponse(Schema):
    message = fields.Str(default="Success")


#  Restful way of creating APIs through Flask Restful
class SignUpAPI(MethodResource, Resource):
    @doc(description='Signup API', tags=['Signup API'])
    @use_kwargs(SignUpRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            user = User(
                uuid.uuid4(),
                kwargs['name'],
                kwargs['username'],
                kwargs['password'],
                kwargs['level']
            )

            db.session.add(user)
            db.session.commit()

            return APIResponse().dump(dict(message="User signed-up successfully")), 200

        except Exception as ex:
            print(str(ex))
            return APIResponse().dump(dict(message="User sign-up failed!")), 400


api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)


class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            user = User.query.filter_by(username=kwargs['username'], password=kwargs['password']).first()
            if user:
                session['user_id'] = user.user_id
                print(f'{user.username} logged in.')
                return APIResponse().dump(dict(message='User logged in')), 200

            else:
                print(f'{kwargs["username"]} logged in attempt failed.')
                return APIResponse().dump(dict(message='User not found or invalid credentials!')), 404

        except Exception as ex:
            print(str(ex))
            return APIResponse().dump(dict(message="User login failed!")), 400


api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)



class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @marshal_with(APIResponse) # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                session['user_id'] = None
                return APIResponse().dump(dict(message='User is successfully logged out')), 200

            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401

        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to logout User: {str(e)}')), 400
            

api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)


class AddVendorAPI(MethodResource, Resource):
    @doc(description='Add Vendor API', tags=['Vendor API'])
    @use_kwargs(AddVendorRequest, location=('json'))
    @marshal_with(APIResponse) # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_id = session['user_id']
                user_type = User.query.filter_by(user_id=user_id).first().level
                print(user_id)
                if user_type == 2:
                    vendor_user_id = kwargs['user_id']
                    print(vendor_user_id)
                    user = User.query.filter_by(user_id=vendor_user_id).first()
                    print(user.level)
                    user.level = 1
                    #db.session.add(user)
                    db.session.commit()
                    return APIResponse().dump(dict(message='Vendor is successfully added.')), 200
                else:
                    return APIResponse().dump(dict(message='Logged User is not an Admin')), 405
            else:
                return APIResponse().dump(dict(message='User is not logged in')), 401

        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to add vendor : {str(e)}')), 400

api.add_resource(AddVendorAPI, '/add_vendor')
docs.register(AddVendorAPI)

class GetVendorsAPI(MethodResource, Resource):
    @doc(description='Get Vendor API', tags=['Get Vendor API'])
    def get(self):
        try:
            if session['user_id']:
                user_level = User.query.filter_by(user_id=session['user_id']).first().level
                if user_level == 2:
                    vendors = User.query.filter_by(level=1)
                    vendors_list = list()
                    for vendor in vendors:
                        vendor_dict = dict()
                        vendor_dict['vendor_id'] = vendor.user_id
                        vendor_dict['name'] = vendor.name
                        vendors_list.append(vendor_dict)

                    return VendorsListResponse().dump(dict(vendors=vendors_list)), 200
                else:
                    return APIResponse().dump(dict(message="No privileges to view vendors")), 400
            else:
                return APIResponse().dump(dict(message="Not a logged in user")), 400

        except Exception as ex:
            return APIResponse().dump(dict(message="Failed to get vendor list!")), 400


api.add_resource(GetVendorsAPI, '/list_vendors')
docs.register(GetVendorsAPI)


class AddItemAPI(MethodResource, Resource):
    @doc(description='Add Item API', tags=['Add Item API'])
    @use_kwargs(AddItemRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):

        if session['user_id']:
            try:
                user_level = User.query.filter_by(user_id=session['user_id']).first().level
                if user_level == 1:
                    item = Item(
                        uuid.uuid4(),
                        session['user_id'],
                        kwargs['item_name'],
                        kwargs['calories_per_gm'],
                        kwargs['available_quantity'],
                        kwargs['restaurant_name'],
                        kwargs['unit_price']
                    )

                    db.session.add(item)
                    db.session.commit()

                    return APIResponse().dump(dict(message=f"{kwargs['item_name']} added to the inventory.")), 200
                else:
                    return APIResponse().dump(dict(message="Logged in user is not a vendor!")), 401

            except Exception as ex:
                print(ex)
                return APIResponse().dump(dict(message="Error while adding item")), 400

        else:
            return APIResponse().dump(dict(message="User not logged in!")), 401


api.add_resource(AddItemAPI, '/add_item')
docs.register(AddItemAPI)


class ListItemsAPI(MethodResource, Resource):
    @doc(description='List Items API', tags=['List All Items API'])
    def get(self):

        if session['user_id']:
            items = Item.query.all()
            items_list = list()
            for item in items:
                item_dict = dict()
                item_dict['item_id'] = item.item_id
                item_dict['item_name'] = item.item_name
                item_dict['calories_per_gm'] = item.calories_per_gm
                item_dict['available_quantity'] = item.available_quantity
                item_dict['unit_price'] = item.unit_price

                items_list.append(item_dict)

            return ItemsListResponse().dump(dict(items=items_list)), 200

        else:
            return APIResponse().dump(dict(message="User not logged in!")), 401


api.add_resource(ListItemsAPI, '/list_items')
docs.register(ListItemsAPI)


class CreateItemOrderAPI(MethodResource, Resource):
    @doc(description='Create Item Order API', tags=['Create Item Order API'])
    @use_kwargs(CreateOrderRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_level = User.query.filter_by(user_id=session['user_id']).first().level
                if user_level == 0:
                    order_id = uuid.uuid4()
                    order = Order(order_id, session['user_id'])
                    db.session.add(order)

                    for item in kwargs['items']:
                        item = dict(item)
                        order_item = OrderItems(
                            uuid.uuid4(),
                            order_id,
                            item['item_id'],
                            item['quantity']
                        )
                        db.session.add(order_item)
                    db.session.commit()

                    return APIResponse().dump(dict(message="Item order created successfully!")), 200

                else:
                    return APIResponse().dump(dict(message="Logged in user is not a customer!")), 401
            else:
                return APIResponse().dump(dict(message="User not logged in!")), 401

        except Exception as ex:
            print(f'Error: {ex}')
            return APIResponse().dump(dict(message="Failed to create item order!")), 400


api.add_resource(CreateItemOrderAPI, '/create_items_order')
docs.register(CreateItemOrderAPI)


class PlaceOrderAPI(MethodResource, Resource):
    @doc(description='Place Order API', tags=['Place Order API'])
    @use_kwargs(PlaceOrderRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            if session['user_id']:
                user_level = User.query.filter_by(user_id=session['user_id']).first().level
                if user_level == 0:
                    order_items = OrderItems.query.filter_by(order_id=kwargs['order_id'], is_active=1)
                    order = Order.query.filter_by(order_id=kwargs['order_id'], is_active=1).first()
                    total_amount = 0
                    for order_item in order_items:
                        item_id = order_item.item_id
                        quantity = order_item.quantity

                        item = Item.query.filter_by(item_id=item_id).first()
                        total_amount += item.unit_price * quantity
                        item.available_quantity = item.available_quantity - quantity

                    order.total_amount = total_amount
                    db.session.commit()
                    return APIResponse().dump(dict(message="Order placed successfully.")), 200

                else:
                    return APIResponse().dump(dict(message="Logged in user is not a customer!")), 401

            else:
                return APIResponse().dump(dict(message="Not a logged in user!")), 400
        except Exception as ex:
            print(f'Error: {ex}')
            return APIResponse().dump(dict(message="Failed to place order!")), 400


api.add_resource(PlaceOrderAPI, '/place_order')
docs.register(PlaceOrderAPI)


class ListOrdersByCustomerAPI(MethodResource, Resource):
    @doc(description='List Orders By Customer API', tags=['List Customer Orders API'])
    def get(self):
        try:
            if session['user_id'] is not None:

                user_level = User.query.filter_by(user_id=session['user_id']).first().level
                if user_level == 0:
                    orders = Order.query.filter_by(user_id=session['user_id'], is_active=1)
                    orders_list = list()
                    for order in orders:
                        order_items = OrderItems.query.filter_by(order_id=order.order_id, is_active=1)

                        order_dict = dict()
                        order_dict['order_id'] = order.order_id
                        order_dict['items'] = list()

                        for order_item in order_items:
                            order_item_dict = dict()
                            order_item_dict['item_id'] = order_item.item_id
                            order_item_dict['quantity'] = order_item.quantity
                            order_dict['items'].append(order_item_dict)

                        orders_list.append(order_dict)

                    return GetOrdersByCustomerRequest().dump(dict(orders=orders_list)), 200
                else:
                    return APIResponse().dump(dict(message="Logged in user is not a customer!")), 401
            else:
                return APIResponse().dump(dict(message="Not a logged in user!")), 401

        except Exception as ex:
            print(f'Error: {ex}')
            return APIResponse().dump(dict(message="Failed to get order list!")), 400


api.add_resource(ListOrdersByCustomerAPI, '/list_orders')
docs.register(ListOrdersByCustomerAPI)


class ListAllOrdersAPI(MethodResource, Resource):
    @doc(description='List All Orders API', tags=['List All Orders API'])
    def get(self):

        try:
            user_level = User.query.filter_by(user_id=session['user_id']).first().level
            if user_level == 2:
                orders = Order.query.filter_by(is_active=1)
                orders_list = list()
                for order in orders:
                    order_dict = dict()
                    order_dict['order_id'] = order.order_id
                    order_dict['user_id'] = order.user_id
                    order_dict['total_amount'] = order.total_amount
                    orders_list.append(order_dict)

                return OrdersListResponse().dump(dict(orders=orders_list)), 200

            else:
                return APIResponse().dump(dict(message="No listing privileges for the user")), 401

        except Exception as ex:
            print(f'Error: {ex}')
            return APIResponse().dump(dict(message="Failed to get order list!")), 400


api.add_resource(ListAllOrdersAPI, '/list_all_orders')
docs.register(ListAllOrdersAPI)


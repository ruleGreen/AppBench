# coding: utf-8
import os
from utils import *
from datetime import datetime

class Meituan:
    def __init__(self, user_name, user_password):
        self.desc = {
            "desc": "This is a meituan app for users to search for restaurants, put dishes in the order, confirm the order, cancel the order and show all the orders.",
            "base_required_arguments": {  
                "user_name (str)": "the user name of the user",
                "user_password (str)": "the password of the user"
            },
            "APIs": {
                    "search_restaurant": {
                        "is_transactional": False,
                        "desc": "search for a restaurant by name or category",
                        "additional_required_arguments": {
                            "query (str)": "the query to search for the restaurant",
                            "by (str)": "the way to search for the restaurant, either by name or category"
                        },
                        "results_arguments": {
                            "restaurant_id (str)": "the id of the restaurant",
                            "restaurant_name (str)": "the name of the restaurant",
                            "restaurant_category (str)": "the category of the restaurant",
                            "restaurant_description (str)": "the description of the restaurant"
                        }
                    },
                   
                    "put_dishes_in_order": {
                        "is_transactional": False,
                        "desc": "put dishes in the order",
                        "additional_required_arguments": {
                            "restaurant_id (str)": "the id of the restaurant",
                            "dish_with_quantity (dict)": "the id of the dishes with quantity"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "order_id (str)": "the id of the order",
                            "shop_name (str)": "the name of the shop",
                            "order_time (time)": "the time of the order, the format follows hh:mm",
                            "order_cost (float)": "the cost of the order",
                            "status (str)": "the status of the order",
                            "dishes (list)": "the list of the dishes in the order"
                        }
                    },

                    "confirm_order": {
                        "desc": "confirm the order",
                        "additional_required_arguments": {
                            "order_id (str)": "the id of the order"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the confirmed order, including the confirmed order number, the shop name, the order time, the order cost , the status of the order and the dishes in the order."
                        }
                    },

                    "cancel_order": {
                        "desc": "cancel the order",
                        "additional_required_arguments": {
                            "order_id (str)": "the id of the order"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the orders, including the cancelled  order number, the shop name, the order time, the order cost , the status of the order and the dishes in the order."
                        }
                    },

                    "show_all_orders": {
                        "desc": "show all the orders of the user",
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the orders, including the order number, the shop name, the order time, the order cost , the status of the order and the dishes in the order."
                           
                        }
                    }
            }
        }
       

        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "meituan_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.orders = user['orders']
                    self.user_name = user_name
                    self.user_password = user_password
                else:
                    return False
        
    def show_all_orders(self):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "meituan_data.json")
        success, data = read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                print(user['orders'])
                return True,user['orders']
                 
            print("No order found")
            return False

    def search_restaurant(self, query,by="name" ):
        if by == "name":
            restaurant_name = query
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "..", "database", "meituan_product_data.json")
            success,data=read_json(file_path)
            list= []
            for restaurant in data["restaurants"]:
                if restaurant["name"] == restaurant_name:
                    list.append(restaurant)
            if list==[]:
                print("No restaurant found")
                return False
            else:
                print(list)
                return list
        if by == "category":
            category = query
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "..", "database", "meituan_product_data.json")
            success,data=read_json(file_path)
            list= []
            for restaurant in data["restaurants"]:
                if restaurant["category"] == category:
                    list.append(restaurant)
            if list == []:
                print("No restaurant found")
                return False
            else:
                print(list)
                return list
    
               

    def put_dishes_in_order(self, restaurant_id, dish_with_quantity):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "meituan_data.json")
        success,data=read_json(file_path)
        file_path1 = os.path.join(current_directory, "..", "database", "meituan_product_data.json")
        success,data1=read_json(file_path1)
        total_price = 0
        dishes = []
        for restaurant in data1["restaurants"]:
            if restaurant["id"] == restaurant_id:
                for dish_id , quantity in dish_with_quantity.items():
                    for dish in restaurant["dishes"]:
                        if dish["id"] == dish_id:
                            dish_add={"id":dish_id,"name":dish["name"],"price":dish["price"], "description": dish["description"],"quantity":quantity}
                            dishes.append(dish_add)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                for restaurant in data1["restaurants"]:
                    if restaurant["id"] == restaurant_id:
                        for dish_id , quantity in dish_with_quantity.items():
                            for dish in restaurant["dishes"]:
                                if dish["id"] == dish_id:
                                    total_price += dish["price"] * quantity                     
                        new_order = {
                        "orderNumber": len(user["orders"]) + 1,
                        "shopName": restaurant["name"],
                        "orderTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "orderCost": total_price,
                        "status": "unconfirmed",
                        "dishes": dishes  # 这里假设您已经将菜品信息添加到了dishes列表中
                        }
                        user["orders"].append(new_order)
                save_json(file_path, data)
                return True,new_order

                                 
                           
        
    def confirm_order(self, order_id):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "meituan_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                for order in user["orders"]:
                    if order["orderNumber"] == order_id:
                        order["status"] = "confirmed"
                        save_json(file_path, data)
                        return True,order

    def cancel_order(self, order_id):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "meituan_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                for order in user["orders"]:
                    if order["orderNumber"] == order_id:
                        order["status"] = "cancelled"
                        save_json(file_path, data)
                        return True,order






if __name__ == "__main__":
   
    meituan = Meituan("xiyuanhao","123456")
   # meituan.show_all_orders()
    #meituan.search_restaurant_by_name("KFC")
   #meituan.search_restaurant_by_category("Fast food")
    #meituan.confirm_order("1")
   # meituan.cancel_order("1")
   # meituan.put_dishes_in_order("100005",{"1001":2,"1002":3})
  
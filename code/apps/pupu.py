from utils import read_json, save_json
import os
from datetime import datetime
class Pupu :
    def __init__(self, user_name, user_password):
        self.desc = {
            "desc": "This is a pupu app for users to search for shops and buy fruits, put items in the order, confirm the order, cancel the order and show all the orders.",
            "base_required_arguments": {  
                "user_name (str)": "the user name of the user",
                "user_password (str)": "the password of the user"
            },
            "APIs": {
                    "search_shop": {
                        "desc": "search for a shop by name or category",
                        "additional_required_arguments": {
                            "query (str)": "the query to search for the shop",
                            "by (str)": "the way to search for the shop, either by name or category"
                        },
                        "results_arguments": {
                            "shop_id (str)": "the id of the shop",
                            "shop_name (str)": "the name of the shop",
                            "shop_category (str)": "the category of the shop",
                            "shop_description (str)": "the description of the shop"
                        }
                    },
                   
                    "put_items_in_order": {
                        "desc": "put items in the order",
                        "additional_required_arguments": {
                            "shop_id (str)": "the id of the shop",
                            "dish_with_quantity (dict)": "the id of the items with quantity"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "order_id (str)": "the id of the order",
                            "shop_name (str)": "the name of the shop",
                            "order_time (time)": "the time of the order, the format follows hh:mm",
                            "order_cost (float)": "the cost of the order",
                            "status (str)": "the status of the order",
                            "items (list)": "the list of the  items in the order"
                        }
                    },
                    "confirm_order": {
                        "desc": "confirm the order",
                        "additional_required_arguments": {
                            "order_id (str)": "the id of the order"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the confirmed order, including the confirmed order number, the shop name, the order time, the order cost , the status of the order and the items in the order."
                        }
                    },
                    "cancel_order": {
                        "desc": "cancel the order",
                        "additional_required_arguments": {
                            "order_id (str)": "the id of the order"
                        },
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the orders, including the cancelled  order number, the shop name, the order time, the order cost , the status of the order and the items in the order."
                        }
                    },
                    "show_all_orders": {
                        "desc": "show all the orders of the user",
                        "results_arguments": {
                            "status (bool)": "the status of the operation",
                            "orders (list)": "the list of the orders, including the order number, the shop name, the order time, the order cost , the status of the order and the items in the order."
                           
                        }
                    }
                
            }
        }
       

        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "pupu_data.json")
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
        file_path = os.path.join(current_directory, "..", "database", "pupu_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                print(user['orders'])
                return True,user['orders']
                 
            print("No order found")
            return False

    def search_shop(self, query,by="name" ):
        if by == "name":
            shop_name = query
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "..", "database", "pupu_product_data.json")
            success,data=read_json(file_path)
            list= []
            for shop in data["shops"]:
                if shop["name"] == shop_name:
                    list.append(shop)
            if list==[]:
                print("No shop found")
                return False
            else:
                print(list)
                return list
        if by == "category":
            category = query
            current_directory = os.path.dirname(__file__)
            file_path = os.path.join(current_directory, "..", "database", "pupu_product_data.json")
            success,data=read_json(file_path)
            list= []
            for shop in data["shops"]:
                if shop["category"] == category:
                    list.append(shop)
            if list == []:
                print("No shop found")
                return False
            else:
                print(list)
                return list
    
               

    def put_items_in_order(self, shop_id, dish_with_quantity):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "pupu_data.json")
        success,data=read_json(file_path)
        file_path1 = os.path.join(current_directory, "..", "database", "pupu_product_data.json")
        success,data1=read_json(file_path1)
        total_price = 0
        items = []
        for shop in data1["shops"]:
            if shop["id"] == shop_id:
                for dish_id , quantity in dish_with_quantity.items():
                    for dish in shop["items"]:
                        if dish["id"] == dish_id:
                            dish_add={"id":dish_id,"name":dish["name"],"price":dish["price"], "description": dish["description"],"quantity":quantity}
                            items.append(dish_add)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                for shop in data1["shops"]:
                    if shop["id"] == shop_id:
                        for dish_id , quantity in dish_with_quantity.items():
                            for dish in shop["items"]:
                                if dish["id"] == dish_id:
                                    total_price += dish["price"] * quantity                     
                        new_order = {
                        "orderNumber": len(user["orders"]) + 1,
                        "shopName": shop["name"],
                        "orderTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "orderCost": total_price,
                        "status": "unconfirmed",
                        "items": items  
                        }
                        user["orders"].append(new_order)
                save_json(file_path, data)
                return True,new_order

                                 
                           
        
    def confirm_order(self, order_id):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "pupu_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
                for order in user["orders"]:
                    if order["orderNumber"]==order_id:
                        print(order)
                        order["status"] = "confirmed"
                        save_json(file_path, data)
                        return True,order
                    

    def cancel_order(self, order_id):
        current_directory = os.path.dirname(__file__)
        file_path = os.path.join(current_directory, "..", "database", "pupu_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            if user["username"] == self.user_name and user["password"] == self.user_password:
                for order in user["orders"]:
                    if order["orderNumber"] == order_id:
                        order["status"] = "cancelled"
                        save_json(file_path, data)
                        return True,order






if __name__ == "__main__":
   
    pupu = Pupu("xiyuanhao","123456")
    #pupu.show_all_orders()
    #pupu.search_shop("xiaobei fruit shop")
    #pupu.search_shop("supermarket","category")
    #pupu.confirm_order(1)
    # pupu.cancel_order(1)
  # pupu.put_items_in_order("100005",{"1001":2,"1002":3})
  
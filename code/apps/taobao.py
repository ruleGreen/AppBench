# coding: utf-8
import os
from utils import *
from datetime import datetime

class Taobao:
    def __init__(self, user_name, user_password):
        self.desc = {
            "desc": "This is a taobao app that allows users to search for products, add products to cart, and place orders. It also allows users to check their orders and",
            "base_required_arguments": {  
                "user_name (str)": "the user name of the user",
                "user_password (str)": "the password of the user"
            },
            "APIs": {
                  "serch_product": {
                    "desc": "search for a product",
                    "additional_required_arguments": {
                        "product_name (str)": "the name of the product to be searched"
                    },
                    "optional_arguments": {
                        "brand_name (str)": "the name of the barnd to be searched",
                    
                    },
                    "results_arguments": {
                        "product_id (str)": "the id of the product",
                        "product_name (str)": "the name of the product",
                        "product_price (float)": "the price of the product",
                        "product_quantity (int)": "the quantity of the product",
                        "product_description (str)": "the description of the product"
                    }
                  },
                  "check_cart": {
                    "desc": "check the products in the cart",
                    "additional_required_arguments": {}, 
                    "optional_arguments": {},
                    "results_arguments": {
                        "cart (list)": "a list of products in the cart"
                    }
                },
                "modify_cart": {
                    "desc": "modify the quantity of a product in the cart",
                    "additional_required_arguments": {
                        "product_id (str)": "the id of the product to be modified in the cart",
                        "quantity (int)": "the new quantity of the product to be modified in the cart"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is modified in the cart successfully, False otherwise"
                    }
                },
                "add_cart": {
                    "desc": "add a product to the cart",
                    "additional_required_arguments": {
                        "product_id (str)": "the id of the product to be added to the cart",
                        "quantity (int)": "the quantity of the product to be added to the cart"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is added to the cart successfully, False otherwise"
                    }
                },
                "delete_cart": {
                    "desc": "delete a product from the cart",
                    "additional_required_arguments": {
                        "product_id (str)": "the id of the product to be deleted from the cart"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is deleted from the cart successfully, False otherwise"
                    }
                },
              
                "purchase_product_directly": {
                    "desc": "purchase a product directly without adding to the cart",
                    "additional_required_arguments": {
                        "product_id (str)": "the id of the product to be added to the order",
                        "quantity (int)": "the quantity of the product to be added to the order"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is added to the order successfully, False otherwise"
                    }
                },
                "purchase_product_in_cart ": {
                    "desc": "purchas a product  from the cart",
                    "additional_required_arguments": {
                        "product_id (str)": "the id of the product to be added to the order from the cart",
                        "quantity (int)": "the quantity of the product to be added to the order from the cart"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is added to the order from the cart successfully, False otherwise"
                    }
                },
                "cancel_order": {
                    "desc": "cancel a product from the order",
                    "additional_required_arguments": {
                        "order_id (str)": "the id of the order to be deleted"
                    },
                    "optional_arguments": {},
                    "results_arguments": {
                        "result (bool)": "True if the product is deleted from the order successfully, False otherwise"
                    }
                },
                "check_order": {
                    "desc": "check the products in the order",
                    "additional_required_arguments": {}, # no need for base required arguments
                    "optional_arguments": {},
                    "results_arguments": {
                        "order (list)": "a list of products in the order"
                    }
                }
              
                
                
            }
        }
       
        self.user_name = user_name
        self.user_password = user_password
        if self.user_name is None or self.user_password is None:
            print(f"An error occurred: user name or password is not valid")
            return False
        else:
            # load other data from database according to user name and password
            current_directory = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
            file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
            success,data=read_json(file_path)
            success1,data1=read_json(file_path1)
            # print(json_file_path)
           # print(data)
            for user in data["users"]:
                # print(user)
                if user["username"] == user_name and user["password"] == user_password:
                    self.order = user['order']
                    self.cart = user['cart']
                return None
        pass
    def check_order(self):
        
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            print(user["order"])
            return user["order"]
        
    def purchase_product_in_cart(self, product_id, quantity):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        msg={}
        order_detail={}

        for user in data["users"]:
            for product in data1["products"]:
                if product_id == product["id"]:
                    if product["quantity"] >= quantity:
                        order_detail["id"]=product["id"]
                        order_detail["name"]=product["name"]
                        order_detail["price"]=product["price"]
                        order_detail["count"]=quantity
                        msg["order_id"]=len(user["order"])+1
                        time=datetime.now()
                        msg["order_time"]=time.strftime("%Y-%m-%d %H:%M:%S")
                        msg["order_detail"]=order_detail
                        product["quantity"] = product["quantity"] - quantity-1
                        print(msg)
                        user["order"].append({k: v for k, v in msg.items()})
                        save_json(file_path, data)
                        save_json(file_path1, data1)
                        self.delete_cart(product_id)
                        return True
                    else:
                        return False
                                
    def purchase_product_directly(self, product_id, quantity):
      
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        msg={}
        order_detail={}

        for user in data["users"]:
            for product in data1["products"]:
                if product_id == product["id"]:
                    if product["quantity"] >= quantity:
                        order_detail["id"]=product["id"]
                        order_detail["name"]=product["name"]
                        order_detail["price"]=product["price"]
                        order_detail["count"]=quantity
                        msg["order_id"]=len(user["order"])+1
                        time=datetime.now()
                        msg["order_time"]=time.strftime("%Y-%m-%d %H:%M:%S")
                        msg["order_detail"]=order_detail
                        product["quantity"] = product["quantity"] - quantity
                        print(msg)
                        user["order"].append({k: v for k, v in msg.items()})
                        save_json(file_path, data)
                        save_json(file_path1, data1)
                        return True
                    else:
                        return False


       
    def cancel_order(self,order_id):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        for user in data["users"]:
                for order in user["order"]:
                    if order_id == order["order_id"]:
                        for details in order["order_detail"]:
                                for  product in data1["products"]:
                                    if details["id"] == product["id"]:
                                        product["quantity"] = product["quantity"] + details["count"]
                                        user["order"].remove(order)
                                        save_json(file_path1, data1)
                                        save_json(file_path, data)
                                        return True
                 
        
       
    def serch_product(self , product_name):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        success1,data1=read_json(file_path1)
        for product in data1["products"]:
            if product_name in product["name"]:
                return product["id"],product["name"],product["price"],product["quantity"],product["description"]
        
    def add_cart(self, product_id, quantity):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        msg={}
        for product in data1["products"]:
            if product_id == product["id"]:
                msg["id"]=product["id"]
                msg["name"]=product["name"]
                msg["price"]=product["price"]
                msg["quantity"]=product["quantity"]
                
        
        print(msg)
        msg["quantity"]=quantity
      
        for user in data["users"]:
            for product in data1["products"]:
                if product_id == product["id"]:
                    if product["quantity"] >= quantity:
                        product["quantity"] = product["quantity"] - quantity
                        save_json(file_path1, data1)
                        user["cart"].append(msg)
                    save_json(file_path, data)
                    return True
    

        

    def modify_cart(self, product_id, quantity):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        index=0
        for user in data["users"]:
            for cart in user["cart"]:
                if product_id == cart["id"]:
                    for product in data1["products"]:
                        if product_id == product["id"]:
                            index=user["cart"].index(cart)
      
        for user in data["users"]:
            for product in data1["products"]:
                if product_id == product["id"]:
                    if product["quantity"] >= quantity:
                        if user["cart"] and isinstance(user["cart"], list) and user["cart"][index].get("count", 0) == 0:
                            return False
                        if quantity == 0:
                            self.delete_cart(product_id)
                        if quantity > user["cart"][index].get("count", 0):
                            product["quantity"] = product["quantity"] - (quantity - user["cart"][index].get("count", 0))
                            user["cart"][index]["count"] = quantity
                        if quantity < user["cart"][index ].get("count", 0):
                            product["quantity"] = product["quantity"] + (user["cart"][index].get("count", 0) - quantity)
                            user["cart"][index]["count"] = quantity
                    save_json(file_path1, data1)
                    save_json(file_path, data)
                    return True

        
        
    def delete_cart(self, product_id):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        file_path1 = os.path.join(current_directory, "..", "database", "taobao_product_data.json")
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        success,data=read_json(file_path)
        success1,data1=read_json(file_path1)
        for user in data["users"]:
            for product in data1["products"]:
                if product_id == product["id"]:
                    for cart in user["cart"]:
                        if product_id == cart["id"]:
                            product["quantity"] = product["quantity"] + cart["count"]
                            user["cart"].remove(cart)
                            save_json(file_path1, data1)
                            save_json(file_path, data)
                            return True
        
    def check_cart(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
 
        file_path = os.path.join(current_directory, "..", "database", "taobao_data.json")
        success,data=read_json(file_path)
        for user in data["users"]:
            print(user["cart"])
            return user["cart"]
       
        
 

if __name__ == "__main__":
    taobao = Taobao("xiyuanhao", "123")
   # print(taobao.serch_product("Huawei"))
    #taobao.check_cart()
   # taobao.add_cart("100001", 1)
   # taobao.delete_cart("100007")
   # taobao.check_order()
   # taobao.delete_order(2)
    #taobao.purchase_product_directly("100003", 1)
    #taobao.purchase_product_in_cart("100007", 1)
    #taobao.modify_cart("100006", 3)

 
   

from Implementation.ProductsImplementation import ProductsImplementation
from Implementation.VendorImplementation import VendorImplementation
from Models.VendorSessionModel import VendorSessionModel

if __name__ == '__main__':

    vendor = VendorImplementation()

    #Vendor Credentials
    u_name = input(f"Enter Vendor Username : ") 
    ps_wd  = input(f"Enter password : ")

    login_res = vendor.login(u_name, ps_wd)
    
    if login_res == False:
        print("Not Authorized Vendor")
    else:
        products = ProductsImplementation(u_name)
        print(f"Vendor \'{u_name}' adds below products and keeps as inventory")
        products.add_product("Lenovo Thinkpad", "Laptop", 40, 20000)
        products.add_product("Dell Inspiron", "Laptop", 40, 30000)
        products.add_product("Acer razor", "Laptop", 40, 25000)        
        products.add_product("Asus Tinker", "Laptop", 40, 20000)
        products.add_product("Lenovo Gaming", "Laptop", 40, 20000)
        print("")

        #Variable to search by product name
        product_name_to_search = input(f"Enter Product name to search : ")

        print(f"\nSearching product name : \'{product_name_to_search}'")
        search_product = products.search_product_by_name(product_name_to_search)
        
        if not search_product:
            print("No product exists by the name")
            
        
        all_products = products.get_all_products()
        print("\nOn vendor request retrieving all products...")
        if (all_products):            
            counter = 1         
            for p_model, p_detail in all_products.items():
                print(f"{counter}) {p_model}",end=': ')
                for p_key, p_value in p_detail.items():
                    print(f" {p_key.replace('_',' ').title()} - {p_value}", end= ', ')                          
                print("")
                counter += 1            
        else:
            print("No product is available to fetch.")
            
        vendor.logout(u_name)
        print("") 
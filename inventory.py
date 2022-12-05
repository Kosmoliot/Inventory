#========Imports========#
from tabulate import tabulate
import os


#========Global Variables========#
shoe_list = []
tot_val = []


#========Class========#
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return(self.cost)
    
    def get_quantity(self):
        return(self.quantity)

    def __str__(self):
        return(self.country, self.code, self.product, self.cost, self.quantity)


#========Functions outside the class========#
# Read data from 'inventory' file and append Shoe class instance to the list
def read_shoes_data():
    try:
        inv_txt = open('inventory.txt', 'r+')
        for line in inv_txt.readlines()[1:]:    # Skipping first line in the file
            line = line.strip('\n').split(',')
            shoe_list.append(Shoe(line[0], line[1], line[2], line[3], line[4]))
    except FileNotFoundError:                   # Error handling
        print("Inventory file not found!")
    finally:
        if inv_txt is not None:
            inv_txt.close()

# Taking user input and appending to the main 'shoe_list'
def capture_shoes():
    new_count = input("Plese type country: ")
    new_code = input("Plese type code: ")
    new_prod = input("Plese type product: ")
    new_cost = input("Plese type cost: ")
    new_qty = input("Plese type quantity: ")
    shoe_list.append(Shoe(new_count, new_code, new_prod, new_cost, new_qty))
    stock_ouput()       # Updating 'inventory.txt' file

# Using class method to get instance variables adn converting them
# to list so we could use 'tabulate' built-in module to display data on screen
def view_all():
    tab_list = []
    
    for obj in shoe_list:
        item = list(obj.__str__())
        tab_list.append(item)
    
    print(tabulate(
        tab_list, headers = ['Country', 'Code', 'Product', 'Cost','Qty'],
        tablefmt = "fancy_grid"))

# Using for loop to find smallest qty and calling two separate functions
# to request user input and write data to inventory.txt file
def re_stock():
    # Assigning qty of the first item in 'shoe_list' as default value
    low_qty = int(shoe_list[1].get_quantity())
    for count, shoe in enumerate(shoe_list):
        if low_qty > int(shoe.get_quantity()):
            low_qty = int(shoe.get_quantity())
            shoe_ind = count
    print("\nThe lowest quantity: {}, model: {}"
          .format(low_qty, shoe_list[shoe_ind].product))
    re_stock_input(shoe_ind)
    stock_ouput()

# User input function to change class instances variable
def re_stock_input(shoe_ind):
    user_choice = input("Would you like to re-stock this model (Y/N): ")
    if user_choice.upper() == "Y":
        new_qty = int(input("Please enter new quantity: "))
        shoe_list[shoe_ind].quantity = new_qty
        
# Writing to a file function, deleting inventory file beforehand so we could 
# add 'Header' and use 'for' loop to append each object's variables
def stock_ouput():
    os.remove("inventory.txt")
    
    inv_file = open("inventory.txt", 'a+')
    inv_file.write("Country,Code,Product,Cost,Quantity")
    for obj in shoe_list:
        inv_file.write("\n{},{},{},{},{}"
            .format(obj.country, obj.code, obj.product, obj.cost, obj.quantity))
    inv_file.close()

# Seraching for a shoe model by code and printing it to screen
def search_shoe():
    code_inp = input("\nPlease type shoe code: ")
    for obj in shoe_list:
        if obj.code == code_inp.upper():
            print(f"""\nCountry: {obj.country}, Code: {obj.code} 
Shoe model: {obj.product}, Cost: {obj.cost}, Qty: {obj.quantity}\n""")
        # else:
        #     print("\nIncorrect product code.")

# Calculating total value per item and printing results to the screen
def value_per_item():
    print("\nTotal value per item:\n")
    for obj in shoe_list:
        total_value = int(obj.cost) * int(obj.quantity)
        tot_val.append([obj.product, total_value])
            
    print(tabulate(list(tot_val), headers= ["Model", "Total value"],
                   tablefmt = "fancy_grid"))

# Using for loop to find largest qty and printing that shoe is on sale
def highest_qty():
    low_qty = 0
    for count, shoe in enumerate(shoe_list):
        if low_qty < int(shoe.get_quantity()):
            low_qty = int(shoe.get_quantity())
            shoe_ind = count
    print("_" * 70)
    print("\nThe model '{}' is on sale.\n".format(shoe_list[shoe_ind].product))
    print("-" * 70)


#========Main Menu========#
def main_menu():
    read_shoes_data()       # Updating 'shoe_list' to have accurate data
    while True:
        user_choice = input("""\nWhat would you like to do:
a\t-\tAdd a new model to inventory
v\t-\tView all models from inventory
s\t-\tSearch shoe by model
r\t-\tRe-stock shoes
t\t-\tTotal value per model
p\t-\tPromotions for high stock models
q\t-\tQuit
: """)
        
        if user_choice == "a":
            capture_shoes()
            
        elif user_choice == "v":
            view_all()
            
        elif user_choice == "s":
            search_shoe()
            
        elif user_choice == "r":
            re_stock()    
        
        elif user_choice == 't':
            value_per_item()
            
        elif user_choice == 'p':
            highest_qty()        
        
        elif user_choice == "q":
            print("\nGoodbye")
            break
        else:
            print("\nOops - incorrect input")


#========Init========#
main_menu()
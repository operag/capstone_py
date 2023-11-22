# Capsone Project Exam

# Import Section
from datetime import datetime
import math
# import os
# import platform

# Declare Variables
items = [{"code": "BB-DRUM-C-D-C","name":"BB DYE INK FOR CANON C 20 LITRE", "price": 100000, "qty": 10},
         {"code": "BB-INK-R800-R-250","name":"BB INK FOR R800 R 250ML", "price": 40000, "qty": 100},
         ]
carts = []
trans = []
favorite = []
numItems = 0
totRev = 0

# Function to draw limiter line
def clear_screen():
    print(padStr("", 145, "_"))

# Function for format currency
def format_currency(amount):
    formatted_amount = "{:,.2f}".format(amount).replace(',', 'temp').replace('.', ',').replace('temp', '.')
    return "Rp " + formatted_amount

# Function to pad string left or right
def padStr(x, length, char = " ", pos = "left") :
    return str(x).ljust(length, char) if pos == "right" else str(x).rjust(length, char);

# FUnction to get idx of list params based on code param
def getIdx(code, exclude = "", list = items) :
    idx = 0
    for i in list :
        if (i["code"].lower() == exclude.lower()) :
            continue
        if (i["code"].lower() == code.lower()) :
            return idx
        idx += 1
    return -1

# Function to calculate total carts items amount
def getTotalCarts() :
    total = 0
    for i in carts:
        total += (i["price"] * i["qty"])
    return total

# Function to calculate total qty of inventory
def getTotalInventory() :
    qty = 0
    for i in items:
        qty += i["qty"]
    return qty 

# Input int data but with validation min and max value
def inputInt(text, max = 9999999999, min = 1, opt = False):
    while(True):
        try:
            x = int(input(text))
            if opt == True :
                if (x < min) :
                    print(f"The option you entered is not valid")
                elif (x > max) :
                    print(f"The option you entered is not valid")
                else :
                    break
            else :
                if (x < min) :
                    print(f"Input minimum is {min}")
                elif (x > max) :
                    print(f"Input cannot exceed {max}")
                else :
                    break
        except:
            print("Input must be filled and should be number !")
            x = 0
    return x

# Input string data but with validation must be filled and max char
def inputMustBeFilled(text, lists = None, maxchar = 9999):
    while(True):
        x = input(text)
        if (x == "") :
            print("Field harus diisi !")
        elif (len(x) > maxchar) :
            print(f"Field length must not exceed {maxchar} !")
        elif (type(lists) == list and len(lists) > 0 and x.lower() not in lists) :
            print("Value must be one of these values: {}".format(", ".join(lists)))
        else:
            break
    return x

# Sort Method
def sortItems(column, itemList = items, mode = 1):
    global favorite
    for i in range(len(itemList)) :
        for j in range(i + 1, len(itemList)) :
            if mode == 1 :
                if type(itemList[i][column]) == datetime and itemList[i][column] > itemList[j][column] :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
                elif type(itemList[i][column]) == str and itemList[i][column].lower() > itemList[j][column].lower() :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
                elif type(itemList[i][column]) == int and itemList[i][column] > itemList[j][column] :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
            elif mode == 2:
                if type(itemList[i][column]) == datetime and itemList[i][column] < itemList[j][column] :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
                elif type(itemList[i][column]) == str and itemList[i][column].lower() < itemList[j][column].lower() :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
                elif type(itemList[i][column]) == int and itemList[i][column] < itemList[j][column] :
                    itemList[i], itemList[j] = itemList[j], itemList[i]
    
    
# Show Sort Menu Function
def showSortMenu():
    while(True) :
        clear_screen()
        print("=======================================================================")
        print("Store Management System > Check Inventory Data > Sort Inventory Data")
        print("=======================================================================")
        print("1. Sort Ascending")
        print("2. Sort Descending")
        print("3. Back")
        menu = inputInt("Choose sort type [1-3]: ", 3);
        if menu == 1 or menu == 2 :
            keys_list = list(items[0].keys())
            names_list = list(map(lambda x:x.capitalize(), items[0].keys()))
            column = inputMustBeFilled("Choose properties to be sorted [{columns}]: ".format(columns = "|".join(names_list)), keys_list)
            sortItems(column=column.lower(), mode=menu)
            print("Items has been sorted by {columns} {modes}".format(columns = column, modes = "Ascending" if menu == 1 else "Descending"))
            showInventory()
        elif menu == 3 :
            break

# Show Inventory Menu Function
def showInventoryMenu():
    if (len(items) > 0):
        while(True) :
            clear_screen()
            print("===================================================")
            print("Store Management System > Check Inventory Data")
            print("===================================================")
            print("1. Show Inventory Data")
            print("2. Search Inventory Data")
            print("3. Sort Inventory Data")
            print("4. Back")
            menu = inputInt("Choose menu [1-4]: ", 4, 1, True);
            clear_screen()
            if menu == 1 :
                showInventory()
            elif menu == 2 :
                keyword = inputMustBeFilled("Input item code or name to be searched: ");
                showInventory(keyword)
                print("Press Enter to continue")
                input("")
            elif menu == 3 :
                showSortMenu()
            elif menu == 4 :
                break
    else:
        print("Data does not exists")
        print("Press Enter to continue...")
        input()

# View Trans Report Data Function
def viewTransReport(keyword = ""):
    global trans;
    global numItems;
    global totRev;
    numItems = 0
    totRev = 0
    if (len(trans) > 0) :
        showColHeader("trans")
        no = 1
        for i in trans:
            if i["transcode"].find(keyword) != -1 or i["name"].find(keyword) != -1 :
                print(padStr(no, 5), "|", padStr(i["transcode"], 10), "|", padStr(i["date"].strftime("%Y-%m-%d %H:%M"), 15), "|", padStr(i["code"], 20), "|", padStr(i["name"], 40), "|", padStr(i["qty"], 10), "|", padStr(format_currency(i["qty"] * i["price"]), 21),"|")
                no += 1
                numItems += i["qty"]
                totRev += (i["qty"] * i["price"])
                
        print(padStr("", 142, "="))
    else:
        print("There is no transaction data found !")

# Show Recaps Menu Function
def showRecapsMenu():
    while(True) :
        clear_screen()
        print("===========================================================")
        print("Store Management System > View Report > Transaction Recaps")
        print("===========================================================")
        viewTransReport()
        print("There are {rows} transaction data rows found with total of {nums} sold ! Revenue: {revenue}".format(rows=len(trans), nums=numItems, revenue=totRev))
        print("1. Search Recaps")
        print("2. Back")
        menu = inputInt("Choose menu [1-2]: ", 2, 1, True);
        if menu == 1 :
            keyword = inputMustBeFilled("Input transaction code or item name to be searched(contains): ")
            viewTransReport(keyword)
            print("Press Enter to continue")
            input("")
        elif menu == 2 :
            break

# Show Favorite Items Function
def showFavoriteItems():
    global favorite
    if (len(trans) > 0) :
        favorite = []
        for i in trans:
            idx = getIdx(code=i["code"], exclude="", list=favorite)
            if idx <= -1:
                b = i.copy()
                del b["transcode"]
                del b["date"]
                favorite.extend([b])
            else:
                favorite[idx]["qty"] += i["qty"]

        sortItems(column="qty", itemList=favorite, mode=2)
        showColHeader("favorite items")
        no = 1
        for i in favorite:
            print(padStr(no, 5), "|", padStr(i["code"], 20), "|", padStr(i["name"], 40), "|", padStr(format_currency(i["price"]), 20), "|", padStr(i["qty"], 10),"|")
            no += 1
        print(padStr("", 109, "="))
    else:
        print("There is no favorite items found !")

# Show Report Menu Function
def showReportMenu():
    global trans
    if (len(trans) > 0):
        while(True) :
            clear_screen()
            print("===================================================")
            print("Store Management System > View Report")
            print("===================================================")
            print("1. Show Transaction Recaps")
            print("2. Show Most to Least Favorite Items (Based on Qty sold)")
            print("3. Back")
            menu = inputInt("Choose menu [1-3]: ", 3, 1, True);
            if menu == 1 :
                sortItems(column="date", itemList=trans, mode=1)
                showRecapsMenu()
            elif menu == 2 :
                showFavoriteItems()
            elif menu == 3 :
                break
    else:
        print("There is no transaction data found !")
        print("Press enter to continue...")
        input("")


# Show Main Menu Function
def showMenu() :
    while(True) :
        clear_screen()
        print("===================================================")
        date = datetime.now()
        print("Store Management System - Today:", date.strftime("%Y-%m-%d"))
        print("===================================================")
        print("1. Check Inventory Data")
        print("2. Add New Inventory")
        print("3. Update Inventory Data")
        print("4. Remove Inventory Data")
        print("5. Order Items")
        print("6. View Report")
        print("7. Exit")
        menu = inputInt("Choose menu [1-7]: ", 7, 1, True);
        
        if menu == 1:
            showInventoryMenu()
        elif menu == 2:
            inputInventory()
        elif menu == 3:
            updateInventory()
        elif menu == 4:
            removeInventory()
        elif menu == 5:
            orderItems()
        elif menu == 6:
            showReportMenu()
        elif menu == 7:
            break

# Show Column Header Function
def showColHeader(cart = "inventory") :
    if (cart == "inventory" or cart == "favorite items") :
        print(padStr("", 109, "="))
        print(padStr(cart.upper() + " DATA", 60),padStr("|", 48))
        print(padStr("", 109, "="))
        print(padStr("No", 5), "|", padStr("Item Code", 20), "|", padStr("Item name", 40), "|", padStr("Price", 20), "|", padStr("Qty", 10),"|")
        print(padStr("", 109, "="))
    elif (cart == "cart") :
        print(padStr("", 136, "="))
        print(padStr(cart.upper() + " DATA", 68),padStr("|", 67))
        print(padStr("", 136, "="))
        print(padStr("No", 5), "|", padStr("Item Code", 20), "|", padStr("Item name", 40), "|", padStr("Price", 20), "|", padStr("Qty", 10),"|", padStr("Subtotal", 24),"|")
        print(padStr("", 136, "="))
    elif (cart == "trans") :
        print(padStr("", 142, "="))
        print(padStr("TRANSACTION DATA", 71),padStr("|", 70))
        print(padStr("", 142, "="))
        print(padStr("No", 5), "|", padStr("Trans Code", 10), "|", padStr("Trans Date", 16), "|", padStr("Item Code", 20), "|", padStr("Item name", 40),"|", padStr("Qty", 10),"|", padStr("Subtotal", 21),"|")
        print(padStr("", 142, "="))

# Show Inventory Function
def showInventory(keyword = "", sort = False, sortby = "") :
    global items;
    if (len(items) > 0) :
        showColHeader()
        no = 1
        for i in items:
            if i["code"].find(keyword) != -1 or i["name"].find(keyword) != -1 :
                print(padStr(no, 5), "|", padStr(i["code"], 20), "|", padStr(i["name"], 40), "|", padStr(format_currency(i["price"]), 20), "|", padStr(i["qty"], 10),"|")
            no += 1
        print(padStr("", 109, "="))
    else:
        print("There is no items found in inventory !")

# Show Carts Data Function
def showCarts() :
    global carts;
    if (len(carts) > 0) :
        showColHeader("cart")
        no = 1
        total = 0
        for i in carts:
            print(padStr(no, 5), "|", padStr(i["code"], 20), "|", padStr(i["name"], 40), "|", padStr(format_currency(i["price"]), 20), "|", padStr(i["qty"], 10),"|", padStr(str(format_currency(i["qty"] * i["price"])), 24),"|")
            no += 1
            total += (i["price"] * i["qty"])
        print(padStr("", 136, "="))
        print(f"Total Cost to be paid: {format_currency(total)}")
    else:
        print("There is no items found in cart !")

# Input Inventory Form
def showInputForm(idx = -1):
    while(True):
        code = inputMustBeFilled(text="Item Code [max 20 chars]: ", maxchar=20)
        if idx == -1:
            if getIdx(code) == -1:
                break
            else:
                print("Item code has been taken, use another item code !")
        elif idx > -1:
            if getIdx(code, items[idx]["code"]) == -1:
                break
            else:
                print("Item code has been taken by other item, use another item code !")
        else:
            break
    name = inputMustBeFilled(text="Item Name [max 40 chars]: ", maxchar=40)
    price = inputInt(text="Price: ", min=0)
    qty = inputInt(text="Qty: ", min=0)
    return {"code": code,"name":name, "price": price, "qty": qty}
 

# Input or Update Inventory Function
def inputInventory(idx = -1) :
    global items
    while(True):
        item = showInputForm(idx)
        if idx < 0 :
            items.append(item)
            print("Data successfully saved")
            print("Press enter to continue..")
            input("")
            break
        else :
            items[idx] = item
            print("Data successfully updated")
            print("Press enter to continue..")
            input("") 
            break

# Input data and Return index of list data function
def inputItemIdx(text, type = "inventory") :
    index = -1
    while (True) :
        menu = inputMustBeFilled(text);
        # l = list(filter(lambda x:x["code"].lower() == menu.lower(), items))
        if (type == "inventory"):
            index = getIdx(code=menu)
        elif (type == "cart"):
            index = getIdx(code=menu, exclude="", list=carts)
        if index == -1 :
            print(f"Data you are looking for does not exists !");
            # continue
        break
    return index
    
# Update Inventory Data Function
def updateInventory():
    global items;
    if len(items) > 0 :
        showInventory()
        idx = inputItemIdx("Input item Code to be updated: ")
        if (idx > -1):
            inputInventory(idx)
        else:
            print("The data you are looking for does not exists")
            print("Press enter to continue..")
            input("")
    else :
        print("The data you are looking for does not exists")
        print("Press enter to continue..")
        input("")

# Remove Inventory Data Function
def removeInventory() :
    global items;
    if len(items) > 0 :
        showInventory()
        idx = inputItemIdx("Input item Code to be removed: ")
        if (idx > -1):
            items.pop(idx)
            print("Data successfully deleted")
        else:
            print("The data you are looking for does not exists")
        print("Press enter to continue..")
        input("")
    else :
        print("The data you are looking for does not exists")
        print("Press enter to continue..")
        input("")

# Add Trans Data Function when Checkout 
def addTransRecap(cartList) :
    global trans;
    lastidx = len(trans) + 1
    transcode = "T-" + padStr(x=lastidx, length=5, char="0", pos="left")
    for c in cartList:
        trans.extend([{"transcode":transcode, "code": c["code"], "name": c["name"], "price": c["price"], "qty": c["qty"],"date":datetime.now()}])
    print(f"Transaction data ({len(carts)}) items saved successfully !")

# Rollback Stock Function
def rollbackStock(code, cartItem) :
    global items;
    idx  = getIdx(code)
    if idx <= -1:
        it = cartItem.copy()
        items.extend([it])
        return len(items) - 1
    else:
        items[idx]["qty"] += cartItem["qty"]
        return idx


# Order Items Menu Function
def orderItems() :
    global items
    global carts
    if len(items) > 0:
        while(True) :
            clear_screen()
            print("===================================================")
            print("Store Management System > Order Items")
            print("===================================================")
            showCarts()
            print("1. Add Cart Items")
            print("2. Update Qty Cart")
            print("3. Remove Cart Items")
            print("4. Checkout")
            print("5. Back")
            menu = inputInt("Choose menu [1-5]: ", 5, 1, True);
            if menu == 1:
                if getTotalInventory() > 0 :
                    showInventory()
                    idx = inputItemIdx("Input item Code to be ordered: ")
                    if idx > -1 :
                        qty = inputInt("Input qty of items: ", items[idx]["qty"])
                        c = items[idx].copy()
                        c["qty"] = qty
                        if qty > 0:
                            items[idx]["qty"] -= qty
                            cidx = getIdx(code=c["code"], list=carts)
                            if cidx == -1:
                                carts.append(c)
                            else:
                                carts[cidx]["qty"] += qty
                            print("Item {name} successfully added to cart".format(name=items[idx]["name"]))
                else :
                    print("There is no stock with qty left in the inventory! Please refill items.")
                    print("Press enter to continue..")
                    input("")
            elif menu == 2:
                showCarts()
                idx = inputItemIdx(text="Input item Code in cart to be updated: ", type="cart")
                if idx > -1 :
                    iidx = rollbackStock(carts[idx]["code"], carts[idx])
                    qty = inputInt("Input qty of items: ", items[iidx]["qty"] )
                    if qty > 0:
                        items[iidx]["qty"] -= qty
                        carts[idx]["qty"] = qty
                        print("Item {name} in cart successfully removed".format(name=carts[idx]["name"]))
            elif menu == 3:
                showCarts()
                idx = inputItemIdx(text="Input item Code in cart to be removed: ", type="cart")
                if idx > -1:
                    rollbackStock(carts[idx]["code"], carts[idx])
                    print("Item {name} in cart successfully removed".format(name=carts[idx]["name"]))
                    carts.pop(idx)
            elif menu == 4:
                pay = inputInt("Input your payment: ")
                total = getTotalCarts()
                if (pay >= total) :
                    addTransRecap(carts)
                    carts = []
                    if (pay - total > 0):
                        print("Change: {change}".format(change=format_currency(pay-total)))
                    print("Thank you for your purchase ! Come back anytime !")
                    print("Press Enter to continue...")
                    input("")
                    break
                else :
                    print("Your payment is insufficient, please commit payment again with correct amount !")
                    print("Press Enter to continue...")
                    input("")
            elif menu == 5 :
                break
    else:
        print("There is no items in inventory !")
        print("Press enter to continue...")
        input("")


# Call Show Main Menu Function
showMenu()

    


      

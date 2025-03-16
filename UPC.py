import os

def loadData(filename):
    """
    Load data from a file and return a dictionary of UPC codes and their corresponding products and prices.
    
    Parameters:
    -----------
    filename : str
        The name of the file to load data from.
    
    Returns:
    --------
    products : dict
        A dictionary of UPC codes and their corresponding products and prices.
    """
    
    products = {}

    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split(", ")
            products[data[0]] = [data[1], float(data[2])] #Adds the data to the products dictionary

    return products


def checkUPC(code):
    """
    Check if a UPC code is valid.
    
    Parameters:
    -----------
    code : str
        The UPC code to check.
    
    Returns:
    --------
    bool
        True if the UPC code is valid, False otherwise.
    """
    
    if len(code) != 12 or not code.isdigit(): #If code is not 12 digits long or if it is not all digits, it is invalid
        return False
    
    if (3*int(code[0]) + int(code[1]) + 3*int(code[2]) + int(code[3]) + 3*int(code[4]) + int(code[5]) + 3*int(code[6]) + int(code[7]) + 3*int(code[8]) + int(code[9]) + 3*int(code[10]) + int(code[11])) % 10 == 0:
        return True
    
    return False


def addProductToDataBase(upcCode, database):
    """
    Add a product to the database and write it to the file
    
    Parameters:
    -----------
    upcCode : str
        The UPC code of the product to add.
    database : dict
        The dictionary of products.
    
    Returns:
    --------
    None
    """

    while True:
        try:
            product = input("\nEnter Product Name: ")
            price = float(input("Enter Price: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid price.")

    database[upcCode] = [product, price] #Update the database with the new upcCode, product, and price
    
    with open("UPC_Codes.txt", 'a') as file: #open the file and add it there too
        file.write(f"{upcCode}, {product}, {price}\n")


def outputCart(cart, database):
    """
    Output the current cart and total due.
    
    Parameters:
    -----------
    cart : list
        The list of UPC codes in the cart.
    database : dict
        The dictionary of products.
    
    Returns:
    --------
    Uses return to break out of the function if the cart is empty.
    """
    
    if len(cart) == 0: #If the cart is empty, just say it's empty and break. Nothing to output
        print("Your cart is empty.")
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\nCurrently Scanned Items:")
    print("-" * 55)

    total = 0

    for upc in cart:
        if upc in database: #If the UPC is in the store, then print the product and price to the recipt
            product, price = database[upc]
            print(f"{product:<45s} ${price:>6.2f}")
            total += price
    
    print("-" * 55)
    print(f"{'Total Due':<45s} ${total:>6.2f}\n\n")


def checkOut():
    """
    Check out the customer and process their payment.
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    bool
        True if the customer wants to continue shopping, False otherwise.
    """
    
    while True:
        card = input("Enter Credit Card Number: ").replace(" ", "") #Strip doesn't work because that only does the ends and beggining spaces
        print()

        if len(card) == 16 and card.isdigit():
            first15 = card[:15]
            evensum = 0
            oddsum = 0
            oddgreater = 0 

            for i in range(1, 15, 2): #Add all the even index numbers
                evensum += int(first15[i])

            for i in range(0, 15, 2): #Add all the odd index numbers
                oddsum += int(first15[i])
                if int(first15[i]) > 4: #If the number is greater than 4, add 1 to the oddgreater
                    oddgreater += 1

            oddsum *= 2
            total = evensum + oddsum + oddgreater + int(card[15])

            if total % 10 == 0:
                print("Payment Accepted!")
                print("Thank you for shopping at Abheek's Abundance!\n")
                
                playagain = 'x'
                while playagain not in ['y', 'n']:
                    playagain = input("Next Customer! (y/n): ")
            
                if playagain == 'y':
                    return True
                return False
            
            else:
                print("Invalid Credit Card Number!\n\n")
                continue
        else:
            print("Invalid Credit Card Number!\n\n")
            continue


def main():
    """
    The Main Function, where all the action happens
    
    Parameters:
    -----------
    None
    
    Returns:
    --------
    None
    """
    
    database = loadData("UPC_Codes.txt")
    cart = []
    os.system('cls' if os.name == 'nt' else 'clear') #Clears the screen for both macs and windows  in the beggining

    while True:
        code = input("Enter UPC (or 'x' to checkout): ").replace(" ", "")

        if code.lower() == 'x':
            
            if len(cart) == 0:
                print("\nThank you for shopping at Abheek's Abundance!")
                break
            else:
                playagain = checkOut()

                if playagain:
                    database = loadData("UPC_Codes.txt")
                    cart = []
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                else:
                    break
    
        if not checkUPC(code): #If the code is invalid, then print that it is invalid and continue so it asks again
            print("Invalid UPC!\n\n")
            continue

        if code in database:
            cart.append(code)
        else: #if the code isn't in the store, but works, ask if they want to add it
            print("This code is not in our database.")
            if input("Would you like to add it? (y/n): ").lower() == 'y':
                addProductToDataBase(code, database)
                cart.append(code)
        
        outputCart(cart, database)
    
    print("Thanks for shopping at Abheek's Abundance!")
    
main()
from os import system, name
from vending.dbAdapter import DatabaseAdapter
from vending.models import ProductCrud, StockCrud, InvoiceCrud

product_crud = ProductCrud()
stock_crud = StockCrud()
invoice_crud = InvoiceCrud()


def clear():

    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def vending_title():
    print('''
          ************************************
          *========VENDING MACHINE===========*
          ************************************
          ''')

def create_new_item():
    clear()
    print("CREATE NEW ITEM")
    product_crud.create(input('Product name: '), float(input('Product Price: ')))


def increase_stock():
    clear()
    print("CHOOSE PRODUCT NUMBER TO INCREASE STOCK")
    print('\tP No\tP NAME\tP QUANTITY')
    print('\t-----\t------\t-------')
    p_nos = []
    for value in stock_crud.product_stock():
        print(f'\t{value[2]}\t{value[0]}\t{value[3]}')
        p_nos.append(value[2])
    try:
        p_no = int(input('Enter product number: '))
        if p_no in p_nos:
            stock_crud.increase_stock(input('Add quantity: '), p_no)
            clear()
    except Exception as e:
        print('Invalid input')

def do_purchase():
    clear()
    items = []
    print('\t***********************')
    print('\t*-AVAILABLE PRODUCT---*')
    print('\t***********************\n')
    print('P No\t\tP Name\t\tAV. QTY\t\tP Price')
    p_nos = []
    my_items = {}
    products = stock_crud.product_stock()
    for value in products:
        print(f'{value[2]}\t\t{value[0]}\t\t{value[3]}\t\t{value[4]}')
        p_nos.append(value[2])
        my_items[value[2]] = value
    i = 0
    keep_add = True
    
    while keep_add:
        p_no = int(input('Enter product number to add to chart: '))
        if p_no in p_nos:
            items.append(p_no)
            i = i + 1

        print(items)
        net_price = 0
        clear()
        print('\t***********************')
        print('\t*Current items in cart*')
        print('\t***********************\n')
        for value in items:
            print(f'[product number: {my_items[value][2]}]{my_items[value][0]} ->  {my_items[value][4]}')
            net_price += my_items[value][4]
        print('Total price: ',net_price)
        print()
        if input('Do realy want to remove an item type (y): ') == 'y':
            p = int(input('Enter Product number: '))
            if p in items:
                items.remove(p)
        print()
        keep_add = True if input('Type (y) and add a item: ') == 'y' else False
        if keep_add:
            for value in products:
                print(f'{value[2]}\t\t{value[0]}\t\t{value[3]}\t\t{value[4]}')
    
    if input("CONFIRM ORDER!!! Type (y): ") == 'y':
        clear()
        print('\n\n\t\t***********************')
        print('\t\t**ORDER CONFIRMATION***')
        print('\t\t***********************')
        print('\t\t***********************')
        print('\t\t*++++++++ Invoice+++++*')
        print('\t\t***********************\n')
        net_price = 0
        for value in items:
            print(f'{my_items[value][0]} ->  {my_items[value][4]}')
            net_price += my_items[value][4]
        print('Total price: ',net_price)
        print()
        invoice_crud.create(items)
        print('Thank u for buying with us!!!')
    else:
        print('Order cancelled!!! C u next time')
    
    # invoice_crud.create(items)


def home():
    while True:
        vending_title()
        print('CUSTOMER PRESS (1)\nSTOCK MANAGER PRESS (2)')
        choice = input('MAKE CHOICE: ')
        if choice == '1':
            do_purchase()
        if choice == '2':
            ch = input('\tINCREASE STOCK (1)\n\tNEW ITEM(2)\n\tMake choice: ')
            if ch == '1':
                increase_stock()
            elif ch == '2':
                create_new_item()
        else:
            break


def main():
    home()


if __name__ == '__main__':
    main()

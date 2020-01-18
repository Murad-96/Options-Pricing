'''
Author: Murad Magdiyev
Date: 1/16/2020
This program can price European style options using Binomial Asset Pricing method.
'''

from Classes.Option import *

def main():
    myStockOption = BinomialEuropeanOption(100, 105, 0.02, 0, 0.1, 2, 4)

    # test the pricing function
    print 'Call option price: {}'.format(round(myStockOption.price(), 2))
    myStockOption.switch_type()
    print 'Put option price: {}'.format(round(myStockOption.price(), 2))



if __name__ == '__main__':
    main()

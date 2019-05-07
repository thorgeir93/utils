from __future__ import print_function
import json
import requests

TRANSACTION_DATE = "12.4.2019"
WIGGLE_PAY = 58755 # isl.kr.
ICETRANSPORT_PAY = 16443 # isl.kr.

VIRDISAUKASKATTUR = 0.24

def get_euro_currency_from(date):
    res = requests.post(
        'https://www.landsbankinn.is/Services/MethodProxy.asmx/Execute',
        json={
            "methodName":"ExchangeRateFrontPage.PopulateCurrencyTable",
            "args": ["Sedla", date]
        }
    )
    result = res.json()

    print(json.dumps(res.json(), indent=3, default=str))
    for currency in result['d']:
        if currency['Mynt'] == 'EUR':
            print(currency)
            return currency

    return res.json()

class Item(object):
    def __init__(self, product, price, quantity, buyer):
        self.product = product
        self.price = price
        self.quantity = quantity
        self.buyer = buyer

    def __repr__(self):
        return u"{0} euro ({1}x{2})".format(self.price, self.quantity, self.product)

class Basket(object):

    #one_euro_in_isl = get_euro_currency_from(TRANSACTION_DATE) #135.61 # 2019 04 12
    #one_euro_in_isl = 129.61 # 2019 04 12
    #one_euro_in_isl = 135.2 # 2019 04 12
    one_euro_in_isl = 139.95 # 2019 04 12

    def __init__(self):
        self.basket = []

    def add_item(self, **item):
        self.basket.append(Item(**item)) 

    def euro_to_isl(self, value):
        return (value * self.one_euro_in_isl)

    def virdisaukaskattur(self, value):
        return (value * VIRDISAUKASKATTUR)
    
    def summary(self):
        sum_price = sum([item.price * item.quantity for item in self.basket])
        print( "total price: {0}".format(sum_price) )
        print('---------------')

        overview = {}
        for item in self.basket:
            if not item.buyer in overview:
                overview[item.buyer] = {'total_euro': 0, 'items': [], 'price_isl': 0}

            overview[item.buyer]['total_euro'] += (item.price * item.quantity)
            overview[item.buyer]['items'].append(item)
            
            #overview[item.buyer]['price_isl'] = self.euro_to_isl(overview[item.buyer]['total_euro'])
            overview[item.buyer]['price_isl'] += self.euro_to_isl((item.price * item.quantity))
            overview[item.buyer]['skattur'] = self.virdisaukaskattur(overview[item.buyer]['price_isl'])

        #for buyer, view in overview.items():
        #    view['percent'] = view['total_euro'] / sum_price

        print('---------------')
        print('SUNDURLIDUN')
        print('---------------')
        print('Total Price:', end='')
        total_price = sum([view['price_isl'] for _,view in overview.items()])
        print(total_price)
        mismatch = WIGGLE_PAY - total_price

        if mismatch:
            print('Found mismatch which will be added to flutningskostad:', end='')
            print(mismatch)

        print('Total Skattur:', end='')
        total_skattur = sum([view['skattur'] for _,view in overview.items()])
        print(total_skattur)

        print('Total flutningskostadur:', end='')
        flutningskostnadur = (ICETRANSPORT_PAY - total_skattur) + mismatch
        print(flutningskostnadur)
       
        for _,view in overview.items():
            view['flutningskostnadur'] = flutningskostnadur / len(overview.items())
            view['SKULDA_THORGEIRI_ISL_KR'] = round(view['flutningskostnadur'] + view['price_isl'] + view['skattur'])
        #overview[item.buyer]['flutningskostnadur'] = self.virdisaukaskattur(overview[item.buyer]['price_isl'])


        total = 0
        for _,view in overview.items():
            total += view['SKULDA_THORGEIRI_ISL_KR']

        print(json.dumps(overview, indent=3, default=str))
        #print(total)
        #print(WIGGLE_PAY + ICETRANSPORT_PAY)

#thorgeir = Buyer(name="thorgeir")

basket = Basket()

basket.add_item(
    product="Continental Quality Road Inner Tube Black - Presta 42mm 700 x 20-25 Race 28",
    price=4.22,
    quantity=2,
    buyer="saevar"
)
basket.add_item(
    product="LifeLine Essential One-Piece Gloss Plastic Bottle Cage Black",
    price=4.93,
    quantity=2,
    buyer="joi"
)
basket.add_item(
    product="Lezyne Zecto Drive Rear 80 Silver",
    price=22.99,
    quantity=1,
    buyer="joi"
)
basket.add_item(
    product="Cateye Volt 800 RC Front Light Black",
    price=99.94,
    quantity=1,
    buyer="joi"
)
basket.add_item(
    product="Continental Quality Road Inner Tube Black - Presta 42mm 700 x 28-37 Tour 28",
    price=4.45,
    quantity=2,
    buyer="thorgeir"
)
basket.add_item(
    product="Continental Grand Prix 5000 Tire 25c 700c",
    price=37.07,
    quantity=2,
    buyer="thorgeir"
)
basket.add_item(
    product="Mini Dual Pump With Gauge Black - Silver Presta / Sch / Dun",
    price=15.17,
    quantity=1,
    buyer="thorgeir"
)
basket.add_item(
    product="Shimano SPD SL Cleats Blue Front Pivot Floating - SH12",
    price=11.57,
    quantity=1,
    buyer="saevar"
)
basket.add_item(
    product="Castelli Diluvio C Overshoes 16 Black 2XL",
    price=29.58,
    quantity=1,
    buyer="thorgeir"
)
basket.add_item(
    product="Oakley Jawbreaker Retina Burn w/ Prizm Road Yellow/Purple",
    price=111.13,
    quantity=1,
    buyer="thorgeir"
)
basket.add_item(
    product="Castelli Thermoflex Arm Warmers Black L",
    price=19.39,
    quantity=1,
    buyer="thorgeir"
)
basket.add_item(
    product="Shimano SPD SL Cleats Yellow Floating - SH11",
    price=13.41,
    quantity=1,
    buyer="thorgeir"
)

basket.summary()

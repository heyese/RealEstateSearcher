import os.path
import csv
import statistics

def main():
    print_header('Real Estate App')

    # Load CVS file and parse into a list of Purchase objects,
    # where all fields are easily accessible as attributes.
    csv_file = os.path.join(os.path.dirname(__file__), 'data', 'SacramentoRealEstateTransactions2008.csv')
    print('Loading real estate CSV data from: {}'.format(csv_file))
    purchases = load_csv_file(csv_file)

    # Most expensive and least expensive houses
    purchases.sort(key=lambda p: p.price)
    for level, purchase in [('Most', purchases[-1]), ('Least', purchases[0])]:
        print('{} expensive home:\nNum beds: {}\nNum bathrooms: {}\n'
              'Square feet: {}\nPrice: {}\n\n'.format(
                level, purchase.beds, purchase.baths, purchase.sq__ft, purchase.price))

    # Average priced house
    m = statistics.mean((p.price for p in purchases))
    print('Average house price is {:,}\n'.format(round(m)))

    # General mean values for 2 bed homes
    # Say we only want to deal with a subset of data.
    # The way to do that is to define a generator to give me the data, and then only pull out what I need
    two_beds = (p for p in purchases if p.beds == 2)
    two_beds_first_20 = []
    for i, p in enumerate(two_beds):
        two_beds_first_20.append(p)
        if i == 20:
            break

    two_beds = two_beds_first_20
    avg_num_baths = statistics.mean((p.beds for p in two_beds))
    avg_sq_ft = statistics.mean((p.sq__ft for p in two_beds))
    avg_price = statistics.mean((p.price for p in two_beds))
    print('Averages for 2 bed houses are:\nPrice: {}\nNumber of baths: {}\nSquare Feet: {}\n'
          .format(avg_price, avg_num_baths, avg_sq_ft))

def print_header(name):
    print('{0:-<{w}}\n{1:^{w}}\n{0:-<{w}}\n'.format('', name, w=2 * len(name)))


def load_csv_file(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        # When you want to do further parsing of data,
        # it can be simpler to create a class
        data = [Purchase.create_from_dict(d) for d in reader]
    return data


class Purchase:
    # Rather than passing __init__ a dict, it is better for people
    # to be able to clearly see what is needed
    # So I can make it explicit in __init__, but have a separate
    # class static_method which takes a dict, unpacks it and calls
    # init to create an instance
    def __init__(self, street, city, zip, state, beds, baths, sq__ft,
                 type, sale_date, price, latitude, longitude):
        self.street = street
        self.city = city
        self.zip = zip
        self.state = state
        self.beds = beds
        self.baths = baths
        self.sq__ft = sq__ft
        self.type = type
        self.sale_date = sale_date
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    # I don't need an instance method as I'm not referencing self,
    # but I am referencing the class.  (It's a factory method - to
    # create instances of classes.)  So if I use a static method, I need
    # to explicitly use the name of the class in the method.  This could
    # break if this class was ever subclassed.  So this is really a
    # 'class method', which gets a reference 'cls' to the class.
    @classmethod
    def create_from_dict(cls, d):
        return cls(
            d['street'],
            d['city'],
            d['zip'],
            d['state'],
            int(d['beds']),
            int(d['baths']),
            int(d['sq__ft']),
            d['type'],
            d['sale_date'],
            float(d['price']),
            float(d['latitude']),
            float(d['longitude'])
        )


if __name__ == '__main__':
    main()

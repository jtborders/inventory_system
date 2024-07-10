from typing import List
import csv

#define classes

class Vehicle:
    def __init__(self, brand, model, year, color, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.color = color
        self.price = price

class Motorcycle(Vehicle):
    def __init__(self, brand, model, year, color, price):
        super().__init__(brand, model, year, color, price)
    def __eq__(self, other):
        if isinstance(other, Car):
            return False
        elif not isinstance(other, Motorcycle):
            return NotImplemented
        return (self.brand == other.brand and
                self.model == other.model and
                self.year == other.year and
                self.color == other.color and
                self.price == other.price)
    def __repr__(self):
        return f"Motorcycle\t{self.brand}\t{self.model}\t{self.year}\t{self.color}\t{self.price}\tn/a"
        
class Car(Vehicle):
    def __init__(self, brand, model, year, color, price, doors):
        super().__init__(brand, model, year, color, price)
        self.doors = doors
    def __eq__(self, other):
        if isinstance(other, Motorcycle):
            return False
        elif not isinstance(other, Car):
            return NotImplemented
        return (self.brand == other.brand and
                self.model == other.model and
                self.year == other.year and
                self.color == other.color and
                self.price == other.price and
                self.doors == other.doors)   
    def __repr__(self):
        return f"Car\t{self.brand}\t{self.model}\t{self.year}\t{self.color}\t{self.price}\t{self.doors}"
        

class Inventory:
    data: List[Vehicle] = []
    
    def __init__(self, file):
        self.file = file
        self.__load(self.file)

    def __load(self, file):
        with open(file, "r") as inventory_file:
            rd = csv.DictReader(inventory_file, delimiter="\t")
            for row in rd:
                if row['type'] == "Car":
                    self.data.append(Car(row['brand'], row['model'], row['year'], row['color'], row['price'], row['doors']))
                elif row['type'] == "Motorcycle":
                    self.data.append(Motorcycle(row['brand'], row['model'], row['year'], row['color'], row['price']))
    
    def addItem(self, vehicle):
        with open(self.file, 'a') as inventory_file:
            inventory_file.write('\n'+str(vehicle))
        self.data.append(vehicle)
        
    def search(self, vehicle):
        for pos, v in enumerate(self.data):
            if v == vehicle:
                return pos
        return -1
    
    def search_attribute(self, **attributes):
        out=[]
        
        for v in self.data:
            if 'type' in attributes.keys():
                # if attributes['type'] != Car and attributes['type'] != Motorcycle:
                #     return []
                if not isinstance(v, attributes['type']):
                    continue
            if 'brand' in attributes.keys():
                if not v.brand == attributes['brand']:
                    continue
            if 'model' in attributes.keys():
                if not v.model == attributes['model']:
                    continue
            if 'year' in attributes.keys():
                if not v.year == attributes['year']:
                    continue
            if 'color' in attributes.keys():
                if not v.color == attributes['color']:
                    continue
            if 'price' in attributes.keys():
                if not v.price == attributes['price']:
                    continue
            if 'doors' in attributes.keys():
                if isinstance(v, Car):
                    if not v.doors == attributes['doors']:
                        continue
                if isinstance(v, Motorcycle):
                    continue
            
            out.append(v)
        
        return out
    
    def removeItem(self, vehicle):
        if self.search(vehicle) != -1:
            self.data.remove(vehicle)
            with open(self.file, "w") as f:
                f.write(self.__repr__())


    def __repr__(self):
        return stringify_vehicles(self.data)
        
def stringify_vehicles(vehicles):
    output = ''
    output += 'type\tbrand\tmodel\tyear\tcolor\tprice\tdoors'
    for vehicle in vehicles:
        output += '\n' + str(vehicle)
    return output

inventory = Inventory("inventory.tsv")
print('''Welcome to your vehicle inventory...
You may add, remove or search for cars or motorcycles.
''')   


ask = input('Would you like to view your inventory, add, remove, search for a vehicle. \n')

if ask == 'add':
    type = input('Type: ')
    brand = input('Brand: ')
    model = input('Model: ')
    year = input('Year: ')
    color = input('Color: ')
    price = input('Price: ')
    if type == 'car' or 'Car':
        doors = input('Doors: ')
        inventory.addItem(Car(brand, model, year, color, price, doors))
    elif type == 'motorcycle' or 'Motorcycle':
        inventory.addItem(Motorcycle(brand, model, year, color, price, 'n/a'))
        
if ask == 'remove':
    type = input('Type: ')
    brand = input('Brand: ')
    model = input('Model: ')
    year = input('Year: ')
    color = input('Color: ')
    price = input('Price: ')
    if type == 'car' or 'Car':
        doors = input('Doors: ')
        inventory.removeItem(Car(brand, model, year, color, price, doors))
    elif type == 'motorcycle' or 'Motorcycle':
        inventory.removeItem(Motorcycle(brand, model, year, color, price, 'n/a'))
    
if ask == 'search':
    attributes = {}
    print('Leave blank if the attribute is unknown')
    Type = input('Type: ')
    if Type != '':
        if Type == 'Car':
            attributes['type'] = Car
        elif Type == 'Motorcycle':
            attributes['type'] = Motorcycle
    Brand = input('Brand: ')
    if Brand != '':
        attributes['brand'] = Brand
    Model = input('Model: ')
    if Model != '':
        attributes['model'] = Model
    Year = input('Year: ')
    if Year != '':
        attributes['year'] = Year
    Color = input('Color: ')
    if Color != '':
        attributes['color'] = Color
    Price = input('Price: ')
    if Price != '':
        attributes['price'] = Price
    Doors = input('Doors: ')
    if Doors != '':
        attributes['doors'] = Doors
    results = inventory.search_attribute(**attributes)
    print(stringify_vehicles(results))
    
if ask == 'view':
    print(inventory)
    

    

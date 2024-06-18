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
    
    def add(self, vehicle):
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
    
    def remove(self, vehicle):
        if self.search(vehicle) != -1:
            self.data.remove(vehicle)
            with open(self.file, "w") as f:
                f.write(self.__repr__())


    def __repr__(self):
        output = ''
        output += 'type\tbrand\tmodel\tyear\tcolor\tprice\tdoors'
        for row in self.data:
            output += '\n' + str(row)
        return output
            
inventory = Inventory('inventory.tsv')
print(inventory.search_attribute(type=Car, doors='2', color='Black'))




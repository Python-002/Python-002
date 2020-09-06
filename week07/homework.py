from abc import ABCMeta,abstractclassmethod

class Animal(metaclass=ABCMeta):
    kind = None        #类型
    shape = None       #体型
    character = None   #性格
    fierce = None      #是否凶猛

    @abstractclassmethod
    def is_fierce(self):
        shape_dict = {"大" : 3, "中" : 2,"小" : 1}
        if self.shape_dict[shape] >= 2 and self.kind == "食肉" and self.character == "凶猛":
            return True
        return False

class Cat(Animal):
    voice = "喵"

    def __init__(self, name, kind, shape, character):
        self.name = name
        self.kind = kind
        self.shape = shape
        self.character = character
    
    @property
    def is_fierce(self):
        shape_dict = {"大" : 3, "中" : 2,"小" : 1}
        if shape_dict[self.shape] >= 2 and self.kind == "食肉" and self.character == "凶猛":
            return True
        else:
            return False

    @property
    def is_pet(self):
        return not self.is_fierce

class Dog(Animal):
    voice = "汪"

    def __init__(self, name, kind, shape, character):
        self.name = name
        self.kind = kind
        self.shape = shape
        self.character = character
    
    @property
    def is_fierce(self):
        shape_dict = {"大" : 3, "中" : 2,"小" : 1}
        if shape_dict[self.shape] >= 2 and self.kind == "食肉" and self.character == "凶猛":
            return True
        else:
            return False

    @property
    def is_pet(self):
        return not self.is_fierce

class Zoo():
    def __init__(self,name):
        self.name = name
        self.animals = []

    def add_animal(self,animal):
        if animal not in self.animals:
            setattr(self, animal.__class__.__name__, True)
            self.animals.append(animal)
        else:
            raise Exception("重复添加")
        
if __name__ == '__main__':
    #实例化动物园
    z = Zoo("时间动物园")
    # print(z.__dict__) # {'name': '时间动物园', 'animals': []}
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # print(z.__dict__) #{'name': '时间动物园', 'animals': [<__main__.Cat object at 0x7fd07d9fbc70>], 'Cat': True}
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
    # print(have_cat)
    # 实例化一只适合当宠物的狗，属性包括名字、类型、体型、性格
    dog1 = Dog('泰迪', '食肉', '小', '温顺')
    # 增加泰迪到动物园
    z.add_animal(dog1)
    # 实例化一只不适合当宠物的狗属性包括名字、类型、体型、性格
    dog2 = Dog('藏獒', '食肉', '大', '凶猛')
    # 增加藏獒到动物园
    z.add_animal(dog2)
    print("大花猫是凶猛动物吗？:",cat1.is_fierce) #大花猫是凶猛动物吗？: False
    print("大花猫是适合当宠物吗？:",cat1.is_pet) #大花猫是适合当宠物吗？: True
    print("藏獒是凶猛动物吗？:",dog2.is_fierce) #藏獒是凶猛动物吗？: True
    print("藏獒是适合当宠物吗？:",dog2.is_pet) #藏獒是适合当宠物吗？: False
    #添加同一只动物
    z.add_animal(dog1)#Exception: 重复添加
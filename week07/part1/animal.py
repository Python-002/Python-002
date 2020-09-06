class Animal:
    """
    动物类
    """
    body_type_mapping = {
        '小型': 1,
        '中等': 2,
        '大型': 3,
        '巨兽': 4
    }

    def __init__(self, animal_type, body_type, character):
        self.animal_type = animal_type
        self.body_type = body_type
        self.character = character
        self.is_ferocious = False

        if (
            animal_type == '食肉'
            and self.body_type_mapping[body_type] >= 2
            and character == '凶猛'
        ):
            self.is_ferocious = True
            print('这是一只凶猛动物')

    def __getattr__(self, item):
        return '略略略'

    @classmethod
    def get_braking(cls):
        return cls.barking


class Zoo:
    """
    动物园类
    """

    def __init__(self, zoo_name):
        self.zoo_name = zoo_name
        zoo_animal_dict[zoo_name] = []

    def add_animal(self, animal_obj):
        zoo_animal_list = zoo_animal_dict[self.zoo_name]

        if not self.check_exist(animal_obj.name, zoo_animal_list):
            zoo_animal_list.append(animal_obj)
        else:
            print(f'【{animal_obj.name}】已经在{self.zoo_name}中了')

    def show_animal(self):
        print('----------------------- 动物介绍 -----------------------------')
        zoo_animal_list = zoo_animal_dict[self.zoo_name]

        for animal in zoo_animal_list:
            print(f'【{animal.name}】是一只生活在{self.zoo_name}的{animal.animal_type}小可爱,喜欢{animal.barking}的'
                  f'它体型{animal.body_type},性格{animal.character},{animal.is_fit_pet}作为宠物呢,'
                  # test __getattr__
                  f'它来自{animal.come_from},'
                  # test classmethod
                  f'它继承了{animal.get_braking}')

    @staticmethod
    def check_exist(check_val, check_list):
        for item in check_list:
            if check_val == item.name:
                return True

        return False


class Cat(Animal):
    """
    猫咪类，继承自动物类
    """
    barking = '喵喵叫'

    def __init__(self, name, animal_type, body_type, character):
        self.name = name
        super().__init__(animal_type, body_type, character)
        # is_fit_pet 适合抽到父类，但是为了符合作业要求放在这里
        self.is_fit_pet = '适合' if not self.is_ferocious else '不适合'

    def __getattr__(self, item):
        if item == 'come_from':
            return '猫星'
        else:
            return super().__getattr__(item)


class Dog(Animal):
    """
    狗狗类，继承自动物类
    """
    barking = '汪汪汪'

    def __init__(self, name, animal_type, body_type, character):
        self.name = name
        super().__init__(animal_type, body_type, character)
        self.is_fit_pet = '适合' if not self.is_ferocious else '不适合'


if __name__ == '__main__':

    zoo_animal_dict = {}
    z = Zoo('吞金兽动物园')

    cat1 = Cat('薯薯', '食肉', '小型', '胆小')
    z.add_animal(cat1)

    cat2 = Cat('毛毛', '杂食', '小型', '凶巴巴')
    z.add_animal(cat2)

    big_dog1 = Dog('旺财', '食肉', '大型', '凶猛')
    z.add_animal(big_dog1)

    # test same animal
    big_dog2 = Dog('旺财', '食肉', '大型', '凶猛')
    z.add_animal(big_dog2)

    z.show_animal()

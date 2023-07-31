import pprint
import sqlite3 as sq
import os
from datetime import datetime


class Meal:
    path_db = os.path.join(os.getcwd(), 'database', 'menu_week.db')

    def __init__(self):
        self.create_database()
        self.create_table_history()

    @classmethod
    def create_database(cls):
        with sq.connect(cls.path_db) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS recipes(
            id_type_food INTEGER,
            name_recipe TEXT NOT NULL DEFAULT recipe,
            type_of_food TEXT,
            date_added TEXT,
            ingredients TEXT,
            description_of_actions TEXT
            )""")

    @classmethod
    def create_table_history(cls):
        with sq.connect(cls.path_db) as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS history_of_cooking(
                    name_recipe TEXT NOT NULL DEFAULT recipe,
                    type_of_food TEXT,
                    date_cooking TEXT
                    )""")

    @classmethod
    def convert_type_food(cls, type_recipes):
        if type_recipes == 'Гарнир':
            return 1
        elif type_recipes == 'Суп':
            return 2
        elif type_recipes == 'Завтрак':
            return 3
        elif type_recipes == 'Ужин':
            return 4

    def added_recipes(self):
        name = input('Название рецепта: ').capitalize()
        type_food = input('Тип блюда: ').capitalize()
        id_type_food = self.convert_type_food(type_food)
        ingredients = ";".join(map(str, input('Ингредиенты: ').split(',')))
        actions = ";".join(map(str, input('Действия: ').split(',')))
        date = str(datetime.now())
        data_input = {'id': id_type_food, 'name': name, 'type_food': type_food, 'date': date[:10],
                      'ingredients': ingredients, 'actions': actions}
        with sq.connect(self.path_db) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO recipes(id_type_food, name_recipe, type_of_food, date_added, ingredients, "
                        "description_of_actions)"
                        "VALUES(:id, :name, :type_food, :date, :ingredients, :actions)", data_input)
        print('Рецепт добавлен')

    def set_recipes(self, type_recipe):
        recipe_dict = []
        with sq.connect(self.path_db) as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM recipes WHERE type_of_food IN(:type)", {'type': type_recipe})
            result = cur.fetchall()
            for i in result:
                name_recipe = i[1]
                type_food = i[2]
                ingredients = i[4].split(';')
                recipe_dict.append({'name': name_recipe, 'type': type_food, 'ingredients': ingredients})
        return recipe_dict


if __name__ == '__main__':

    create_db = Meal()
    # create_db.added_recipes()
    pprint.pprint(create_db.set_recipes('Суп'))


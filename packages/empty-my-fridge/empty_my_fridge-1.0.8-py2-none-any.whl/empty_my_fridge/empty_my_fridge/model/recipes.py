
class Recipes:
    def __init__(self):
        self.recipe_list = None
        self.pos = 0
        self.liked = False
        self.searched = False
        self.recipe_name_to_find = None
        self.recipes_current_page = "1"
        self.db = None
        self.m_user = None
        self.food_network = None
        self.visited_pages = ""
        self.scraped = False
        self.filter_list = None
        self.sorting_type = "name_A"
        self.fridge_recipes = None
        self.is_fridge = False
        self.fridge_sorting_type = "name_A"

        

    def __init__(self, db, m_user, food_network):
        self.recipe_list = None
        self.pos = 0
        self.liked = False
        self.searched = False
        self.recipe_name_to_find = None
        self.recipes_current_page = "1"
        self.db = db
        self.m_user = m_user
        self.food_network = food_network
        self.visited_pages = ""
        self.scraped = False
        self.sorting_type = "name_A"
        self.filter_list = None
        self.fridge_recipes = None
        self.is_fridge = False
        self.fridge_sorting_type = "name_A"

    def get_fridge_recipes(self):
        return self.fridge_recipes

    def set_fridge_recipes(self, fridge_recipes):
        self.fridge_recipes = fridge_recipes

    def get_is_fridge(self):
        return self.is_fridge

    def set_is_fridge(self, is_fridge):
        self.is_fridge = is_fridge

    def get_sorting_type(self):
        return self.sorting_type

    def set_sorting_type(self, type):
        self.sorting_type = type

    def get_fridge_sorting_type(self):
        return self.fridge_sorting_type

    def set_fridge_sorting_type(self, type):
        self.fridge_sorting_type = type
    
    def set_scraped(self, scraped):
        self.scraped = scraped

    def get_scraped(self):
        return self.scraped

    def set_visited_pages(self, page):
        self.visited_pages += "," + page

    def get_visited_pages(self, page):
        return self.visited_pages.find(page)

    def get_all_recipes(self):
        return self.recipe_list

    def set_all_recipes(self, recipe_list):
        self.recipe_list = recipe_list

    def set_recipe_list_position(self, pos):
        self.pos = pos

    def get_recipe_list_position(self):
        return self.pos

    def set_is_recipe_liked(self, liked):
        self.liked = liked

    def get_is_recipe_liked(self):
        return self.liked

    def set_is_searched_for_recipes(self, searched):
        self.searched = searched

    def get_is_searched_for_recipes(self):
        return self.searched

    def set_recipe_name_to_find(self, word):
        self.recipe_name_to_find = word

    def get_recipe_name_to_find(self):
        return self.recipe_name_to_find

    def set_recipes_current_page(self, page):
        self.recipes_current_page = page

    def get_recipes_current_page(self):
        return self.recipes_current_page

    def set_recipe_liked(self, key):
        for recipe in self.recipe_list:
            if recipe["recipe_id"] == key:
                recipe["user_saved"] = True
                recipe["likes"] = recipe["likes"] + 1
                break

    def set_recipe_unLiked(self, key):
        for recipe in self.recipe_list:
            if recipe["recipe_id"] == key:
                recipe["user_saved"] = False
                recipe["likes"] = recipe["likes"] - 1
                break                                     

    def get_all_likes(self, uid, page):
        page_num = int(page)
        start = (page_num - 1) * 48
        favorite = False
        
        while start < len(self.recipe_list):
            recipe = self.recipe_list[start]
            recipe["no_user_signed_in"] = True
            if start == len(self.recipe_list) or start == page_num * 48:
                break
            try:
                key = recipe["recipe_id"]
                if uid:
                    recipe["no_user_signed_in"] = False
                    favorite = recipe["stars"][uid] != None
                    recipe["user_saved"] = favorite
            except KeyError:
                pass
            start+=1
             
    # get all recipes
    def _get_all_recipes_(self):
        #self.db.child('all_ingredients').remove()
        #self.food_network.food_network(self.db)
        all_recipes = self.db.child("recipe").get()

        recipe_list = []
        if all_recipes.each() != None:
            for recipe in all_recipes.each():
                key = str(recipe.key())
                try:
                    name = recipe.val()["recipe_name"]
                    _recipe_ = self.get_recipe(dict(recipe.val()), key, self.m_user._getUser_Id_())
                    recipe_list.append(_recipe_)
                except KeyError:
                    self.db.child("recipe").child(key).remove()
                    continue


        self.recipe_list = recipe_list  

    # get individual recipe as Json
    def get_recipe(self, recipe, key, uid):
        num_of_stars = 0
        favorite = False
        recipe["recipe_id"] = key
        recipe["no_user_signed_in"] = True
        try:
            if uid:
                recipe["no_user_signed_in"] = False
                favorite = recipe["stars"][uid] != None
            recipe["user_saved"] = favorite
        except KeyError:
            recipe["user_saved"] = False
            pass
        try:
            num_of_stars = len(recipe["stars"].items())
            recipe["likes"] = num_of_stars
        except KeyError:
            recipe["likes"] = 0
            pass    

        return recipe
    
    def set_filter_list(self, filters):
        if not filters:
            self.filter_list = None
        elif len(filters) == 0:
            self.filter_list = None
        else:
            self.filter_list = filters

    def get_filter_list(self):
        return self.filter_list
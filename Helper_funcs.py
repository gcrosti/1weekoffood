

#GLUTEN-FREE FILTER
def gf_filter(meals,gf):
    meals1 = meals
    if gf == 'y':
        meals1 = meals[meals['Gluten-free?']=='y']
    return meals1

#VEGETARIAN FILTER
def veg_filter(meals,veg):
    meals1 = meals
    if veg == 'y':
        meals1 = meals[meals['Vegetarian?']=='y'] 
    return meals1

#

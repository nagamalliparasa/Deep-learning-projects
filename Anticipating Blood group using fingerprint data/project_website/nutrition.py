nutritions={'B+':[''' Meat,Mutton,Dairy
products,Beans.''','''
  Wheat,Olives,Tomatoes
&Corn.'''],
'B-':[''' Meat,Mutton,Dairy
products,Beans.''','''
  Wheat,Olives,Tomatoes
&Corn.'''],
'A-':[''' including plant based 
diet,Like Vegetables,Fruits,Beans,
Legumes &Limited fish.''','''
  Wheat,Meat,Diary.
'''],
'A+':[''' including plant based 
diet,Like Vegetables,Fruits,Beans,
Legumes &Limited fish.''','''
  Wheat,Meat,Diary.
'''],
'O-':[''' Emphasize high protien 
diets including Fish,Poultry,Fruits & Veggies.''','''
  Limiting starches & omit 
grains,Beans,Legumes & Dairy products.
'''],
'O+':[''' Emphasize high protien 
diets including Fish,Poultry,Fruits & Veggies.''','''
  Limiting starches & omit 
grains,Beans,Legumes & Dairy products.
'''],
'AB+':[''' Meat,Mutton,Dairy
products,Beans,including plant based 
diet,Like Vegetables,Fruits,Beans,
Legumes &Limited fish.''','''
  Wheat,Olives,Tomatoes
&Corn.'''],
'AB-':[''' Meat,Mutton,Dairy
products,Beans,including plant based 
diet,Like Vegetables,Fruits,Beans,
Legumes &Limited fish.''','''
  Wheat,Olives,Tomatoes
&Corn.''']

}

def nutritions_recommend(blood_group):
    if blood_group is None:
        return None
    blood_group=blood_group.upper()
    return nutritions[blood_group]
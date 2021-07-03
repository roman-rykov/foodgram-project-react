import json

with open('ingredients.json') as file:
    data = json.load(file)

fixtures = []
for obj in data:
    fixtures.append({
        'model': 'recipes.ingredient',
        'fields': {
            'name': obj['title'],
            'measurement_unit': obj['dimension'],
        }
    })

with open('fixtures.json', 'w') as new_file:
    json.dump(fixtures, new_file)

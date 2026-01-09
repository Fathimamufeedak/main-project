import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicinal_plant_project.settings')

import django
django.setup()

from plants.models import Plant, Remedy

SAMPLES = [
    {
        'plant_name': 'Aloe Vera',
        'description': 'Succulent plant known for soothing skin.',
        'medicinal_uses': 'Skin burns, wound healing, digestive aid.',
        'safety_guidelines': 'For external use; test for allergies.'
    },
    {
        'plant_name': 'Turmeric',
        'description': 'Yellow spice with anti-inflammatory properties.',
        'medicinal_uses': 'Digestive issues, joint pain, antiseptic.',
        'safety_guidelines': 'Avoid high doses during pregnancy.'
    },
    {
        'plant_name': 'Neem',
        'description': 'Bitter tree used in traditional medicine.',
        'medicinal_uses': 'Skin conditions, anti-parasitic, oral hygiene.',
        'safety_guidelines': 'Not for prolonged internal use.'
    },
]

def run():
    created = 0
    for s in SAMPLES:
        p, ok = Plant.objects.get_or_create(plant_name=s['plant_name'], defaults={
            'description': s['description'],
            'medicinal_uses': s['medicinal_uses'],
            'safety_guidelines': s['safety_guidelines'],
        })
        if ok:
            created += 1
            # create a placeholder remedy
            Remedy.objects.create(plant=p, remedy_description=f"General remedy for {p.plant_name}: follow standard Ayurvedic guidance.")
    print(f"Seed complete. Plants created: {created}. Total plants: {Plant.objects.count()}")

if __name__ == '__main__':
    run()

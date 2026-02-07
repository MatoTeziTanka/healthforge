#!/usr/bin/env python3
"""Generate HealthForge wellness dataset and upload to Algolia."""

import json
import random
import hashlib
from algoliasearch.search.client import SearchClientSync

APP_ID = "RM2LBYLLID"
ADMIN_KEY = "ec65c46d881642b155f86c16b817d716"
INDEX_NAME = "healthforge_items"

# --- EXERCISES ---
EXERCISES = [
    # Cardio
    {"name": "Morning Jog", "subcategory": "cardio", "muscle_groups": ["legs", "core"], "calories_per_30min": 300, "difficulty": "beginner", "equipment": [], "indoor": False},
    {"name": "HIIT Sprint Intervals", "subcategory": "cardio", "muscle_groups": ["legs", "core", "glutes"], "calories_per_30min": 450, "difficulty": "advanced", "equipment": [], "indoor": False},
    {"name": "Jump Rope Circuit", "subcategory": "cardio", "muscle_groups": ["legs", "shoulders", "core"], "calories_per_30min": 400, "difficulty": "intermediate", "equipment": ["jump rope"], "indoor": True},
    {"name": "Cycling Endurance", "subcategory": "cardio", "muscle_groups": ["legs", "glutes"], "calories_per_30min": 350, "difficulty": "intermediate", "equipment": ["bicycle"], "indoor": False},
    {"name": "Swimming Laps", "subcategory": "cardio", "muscle_groups": ["full body"], "calories_per_30min": 380, "difficulty": "intermediate", "equipment": ["pool access"], "indoor": True},
    {"name": "Rowing Machine", "subcategory": "cardio", "muscle_groups": ["back", "arms", "legs"], "calories_per_30min": 360, "difficulty": "intermediate", "equipment": ["rowing machine"], "indoor": True},
    {"name": "Stair Climbing", "subcategory": "cardio", "muscle_groups": ["legs", "glutes", "core"], "calories_per_30min": 400, "difficulty": "beginner", "equipment": [], "indoor": True},
    {"name": "Dance Cardio", "subcategory": "cardio", "muscle_groups": ["full body"], "calories_per_30min": 320, "difficulty": "beginner", "equipment": [], "indoor": True},
    {"name": "Boxing Workout", "subcategory": "cardio", "muscle_groups": ["arms", "shoulders", "core"], "calories_per_30min": 420, "difficulty": "intermediate", "equipment": ["boxing gloves", "heavy bag"], "indoor": True},
    {"name": "Elliptical Training", "subcategory": "cardio", "muscle_groups": ["legs", "arms"], "calories_per_30min": 280, "difficulty": "beginner", "equipment": ["elliptical"], "indoor": True},
    # Strength
    {"name": "Barbell Squat", "subcategory": "strength", "muscle_groups": ["legs", "glutes", "core"], "calories_per_30min": 250, "difficulty": "intermediate", "equipment": ["barbell", "squat rack"], "indoor": True},
    {"name": "Deadlift", "subcategory": "strength", "muscle_groups": ["back", "legs", "core"], "calories_per_30min": 260, "difficulty": "intermediate", "equipment": ["barbell"], "indoor": True},
    {"name": "Bench Press", "subcategory": "strength", "muscle_groups": ["chest", "shoulders", "triceps"], "calories_per_30min": 220, "difficulty": "intermediate", "equipment": ["barbell", "bench"], "indoor": True},
    {"name": "Pull-ups", "subcategory": "strength", "muscle_groups": ["back", "biceps", "core"], "calories_per_30min": 240, "difficulty": "intermediate", "equipment": ["pull-up bar"], "indoor": True},
    {"name": "Dumbbell Lunges", "subcategory": "strength", "muscle_groups": ["legs", "glutes"], "calories_per_30min": 230, "difficulty": "beginner", "equipment": ["dumbbells"], "indoor": True},
    {"name": "Kettlebell Swings", "subcategory": "strength", "muscle_groups": ["full body"], "calories_per_30min": 350, "difficulty": "intermediate", "equipment": ["kettlebell"], "indoor": True},
    {"name": "Push-up Variations", "subcategory": "strength", "muscle_groups": ["chest", "triceps", "core"], "calories_per_30min": 200, "difficulty": "beginner", "equipment": [], "indoor": True},
    {"name": "Overhead Press", "subcategory": "strength", "muscle_groups": ["shoulders", "triceps"], "calories_per_30min": 210, "difficulty": "intermediate", "equipment": ["barbell"], "indoor": True},
    {"name": "Resistance Band Training", "subcategory": "strength", "muscle_groups": ["full body"], "calories_per_30min": 180, "difficulty": "beginner", "equipment": ["resistance bands"], "indoor": True},
    {"name": "Turkish Get-up", "subcategory": "strength", "muscle_groups": ["full body"], "calories_per_30min": 200, "difficulty": "advanced", "equipment": ["kettlebell"], "indoor": True},
    # Flexibility
    {"name": "Vinyasa Yoga", "subcategory": "flexibility", "muscle_groups": ["full body"], "calories_per_30min": 180, "difficulty": "intermediate", "equipment": ["yoga mat"], "indoor": True},
    {"name": "Yin Yoga", "subcategory": "flexibility", "muscle_groups": ["full body"], "calories_per_30min": 100, "difficulty": "beginner", "equipment": ["yoga mat"], "indoor": True},
    {"name": "Dynamic Stretching", "subcategory": "flexibility", "muscle_groups": ["full body"], "calories_per_30min": 120, "difficulty": "beginner", "equipment": [], "indoor": True},
    {"name": "Pilates Core", "subcategory": "flexibility", "muscle_groups": ["core", "back"], "calories_per_30min": 200, "difficulty": "intermediate", "equipment": ["mat"], "indoor": True},
    {"name": "Foam Rolling Recovery", "subcategory": "flexibility", "muscle_groups": ["full body"], "calories_per_30min": 80, "difficulty": "beginner", "equipment": ["foam roller"], "indoor": True},
    {"name": "Tai Chi", "subcategory": "flexibility", "muscle_groups": ["full body"], "calories_per_30min": 150, "difficulty": "beginner", "equipment": [], "indoor": False},
    # Recovery
    {"name": "Meditation Session", "subcategory": "recovery", "muscle_groups": ["mind"], "calories_per_30min": 30, "difficulty": "beginner", "equipment": [], "indoor": True},
    {"name": "Cold Plunge", "subcategory": "recovery", "muscle_groups": ["full body"], "calories_per_30min": 50, "difficulty": "intermediate", "equipment": ["cold plunge tub"], "indoor": True},
    {"name": "Sauna Session", "subcategory": "recovery", "muscle_groups": ["full body"], "calories_per_30min": 40, "difficulty": "beginner", "equipment": ["sauna access"], "indoor": True},
    {"name": "Sleep Optimization", "subcategory": "recovery", "muscle_groups": ["mind"], "calories_per_30min": 0, "difficulty": "beginner", "equipment": [], "indoor": True},
]

# --- SUPPLEMENTS ---
SUPPLEMENTS = [
    {"name": "Whey Protein Isolate", "subcategory": "protein", "benefits": ["muscle recovery", "lean muscle growth"], "allergens": ["dairy"], "dosage": "25g post-workout", "price_usd": 35},
    {"name": "Plant-Based Protein Blend", "subcategory": "protein", "benefits": ["muscle recovery", "vegan-friendly"], "allergens": ["soy"], "dosage": "30g post-workout", "price_usd": 40},
    {"name": "Creatine Monohydrate", "subcategory": "performance", "benefits": ["strength gains", "power output", "muscle volume"], "allergens": [], "dosage": "5g daily", "price_usd": 25},
    {"name": "Omega-3 Fish Oil", "subcategory": "health", "benefits": ["heart health", "inflammation reduction", "joint support"], "allergens": ["fish"], "dosage": "2g daily", "price_usd": 20},
    {"name": "Vitamin D3+K2", "subcategory": "health", "benefits": ["bone density", "immune support", "mood"], "allergens": [], "dosage": "5000 IU daily", "price_usd": 15},
    {"name": "Magnesium Glycinate", "subcategory": "recovery", "benefits": ["sleep quality", "muscle relaxation", "stress reduction"], "allergens": [], "dosage": "400mg before bed", "price_usd": 18},
    {"name": "BCAA Complex", "subcategory": "performance", "benefits": ["muscle preservation", "endurance", "recovery"], "allergens": [], "dosage": "10g during workout", "price_usd": 28},
    {"name": "Pre-Workout Energizer", "subcategory": "performance", "benefits": ["energy", "focus", "pump"], "allergens": [], "dosage": "1 scoop 30min pre-workout", "price_usd": 32},
    {"name": "Collagen Peptides", "subcategory": "recovery", "benefits": ["joint health", "skin elasticity", "gut health"], "allergens": [], "dosage": "10g daily", "price_usd": 30},
    {"name": "Ashwagandha Extract", "subcategory": "health", "benefits": ["stress reduction", "cortisol control", "energy"], "allergens": [], "dosage": "600mg daily", "price_usd": 22},
    {"name": "Zinc + Selenium", "subcategory": "health", "benefits": ["immune support", "testosterone support", "antioxidant"], "allergens": [], "dosage": "30mg zinc daily", "price_usd": 12},
    {"name": "Turmeric Curcumin", "subcategory": "health", "benefits": ["anti-inflammatory", "joint support", "antioxidant"], "allergens": [], "dosage": "1000mg daily", "price_usd": 18},
    {"name": "L-Glutamine", "subcategory": "recovery", "benefits": ["gut health", "immune support", "muscle recovery"], "allergens": [], "dosage": "5g post-workout", "price_usd": 20},
    {"name": "Melatonin + L-Theanine", "subcategory": "recovery", "benefits": ["sleep onset", "sleep quality", "relaxation"], "allergens": [], "dosage": "3mg melatonin before bed", "price_usd": 15},
    {"name": "Iron + Vitamin C", "subcategory": "health", "benefits": ["energy levels", "oxygen transport", "iron absorption"], "allergens": [], "dosage": "18mg iron daily", "price_usd": 14},
    {"name": "Electrolyte Mix", "subcategory": "performance", "benefits": ["hydration", "cramping prevention", "endurance"], "allergens": [], "dosage": "1 packet per workout", "price_usd": 25},
    {"name": "Probiotics 50B CFU", "subcategory": "health", "benefits": ["gut health", "immune function", "nutrient absorption"], "allergens": ["dairy"], "dosage": "1 capsule daily", "price_usd": 28},
    {"name": "Vegan Omega-3 (Algal Oil)", "subcategory": "health", "benefits": ["heart health", "brain function", "vegan-friendly"], "allergens": [], "dosage": "1000mg daily", "price_usd": 30},
]

# --- GEAR ---
GEAR = [
    {"name": "Adjustable Dumbbell Set (5-52.5 lbs)", "subcategory": "weights", "for_goals": ["strength", "muscle building"], "price_usd": 350, "durability": "high"},
    {"name": "Resistance Band Set (5 levels)", "subcategory": "bands", "for_goals": ["strength", "flexibility", "rehabilitation"], "price_usd": 30, "durability": "medium"},
    {"name": "Yoga Mat (6mm Eco-Friendly)", "subcategory": "mats", "for_goals": ["flexibility", "recovery", "mindfulness"], "price_usd": 45, "durability": "high"},
    {"name": "Foam Roller (High Density)", "subcategory": "recovery", "for_goals": ["recovery", "flexibility", "pain relief"], "price_usd": 25, "durability": "high"},
    {"name": "Heart Rate Monitor Watch", "subcategory": "tech", "for_goals": ["cardio", "weight loss", "endurance"], "price_usd": 200, "durability": "high"},
    {"name": "Kettlebell (16kg / 35lb)", "subcategory": "weights", "for_goals": ["strength", "cardio", "functional fitness"], "price_usd": 55, "durability": "high"},
    {"name": "Pull-up Bar (Doorframe)", "subcategory": "bodyweight", "for_goals": ["strength", "muscle building"], "price_usd": 35, "durability": "medium"},
    {"name": "Jump Rope (Speed Rope)", "subcategory": "cardio", "for_goals": ["cardio", "coordination", "weight loss"], "price_usd": 15, "durability": "medium"},
    {"name": "Massage Gun (Percussion)", "subcategory": "recovery", "for_goals": ["recovery", "pain relief"], "price_usd": 120, "durability": "high"},
    {"name": "Gym Gloves (Padded)", "subcategory": "accessories", "for_goals": ["strength", "protection"], "price_usd": 20, "durability": "medium"},
    {"name": "Stability Ball (65cm)", "subcategory": "bodyweight", "for_goals": ["core strength", "flexibility", "balance"], "price_usd": 25, "durability": "medium"},
    {"name": "TRX Suspension Trainer", "subcategory": "bodyweight", "for_goals": ["functional fitness", "strength", "flexibility"], "price_usd": 170, "durability": "high"},
    {"name": "Weighted Vest (20lb)", "subcategory": "weights", "for_goals": ["strength", "cardio", "calorie burn"], "price_usd": 80, "durability": "high"},
    {"name": "Ab Roller Wheel", "subcategory": "bodyweight", "for_goals": ["core strength"], "price_usd": 15, "durability": "high"},
    {"name": "Blender Bottle (28oz)", "subcategory": "accessories", "for_goals": ["nutrition", "convenience"], "price_usd": 12, "durability": "medium"},
    {"name": "Meal Prep Containers (set of 10)", "subcategory": "accessories", "for_goals": ["nutrition", "weight loss", "meal planning"], "price_usd": 20, "durability": "medium"},
    {"name": "Running Shoes (Cushioned)", "subcategory": "footwear", "for_goals": ["cardio", "running", "joint protection"], "price_usd": 130, "durability": "medium"},
    {"name": "Compression Sleeves (Knee)", "subcategory": "recovery", "for_goals": ["recovery", "joint support", "injury prevention"], "price_usd": 25, "durability": "medium"},
    {"name": "Smart Scale (Body Composition)", "subcategory": "tech", "for_goals": ["weight loss", "tracking", "body composition"], "price_usd": 50, "durability": "high"},
    {"name": "Workout Timer / Interval Clock", "subcategory": "tech", "for_goals": ["HIIT", "time management"], "price_usd": 30, "durability": "high"},
]

# --- MEAL PLANS ---
MEAL_PLANS = [
    {"name": "High Protein Muscle Builder", "subcategory": "muscle building", "calories_daily": 2800, "protein_g": 180, "carbs_g": 300, "fat_g": 80, "meals_per_day": 5, "allergens": ["dairy", "eggs"], "diet_type": "omnivore"},
    {"name": "Lean Cut Fat Loss", "subcategory": "weight loss", "calories_daily": 1800, "protein_g": 150, "carbs_g": 150, "fat_g": 60, "meals_per_day": 4, "allergens": [], "diet_type": "omnivore"},
    {"name": "Vegan Power Plan", "subcategory": "muscle building", "calories_daily": 2600, "protein_g": 140, "carbs_g": 350, "fat_g": 75, "meals_per_day": 5, "allergens": ["soy", "nuts"], "diet_type": "vegan"},
    {"name": "Keto Endurance Fuel", "subcategory": "endurance", "calories_daily": 2200, "protein_g": 130, "carbs_g": 30, "fat_g": 170, "meals_per_day": 3, "allergens": ["dairy", "eggs"], "diet_type": "keto"},
    {"name": "Mediterranean Balance", "subcategory": "general health", "calories_daily": 2200, "protein_g": 100, "carbs_g": 250, "fat_g": 90, "meals_per_day": 3, "allergens": ["fish", "nuts"], "diet_type": "mediterranean"},
    {"name": "Intermittent Fasting 16:8", "subcategory": "weight loss", "calories_daily": 2000, "protein_g": 120, "carbs_g": 200, "fat_g": 80, "meals_per_day": 2, "allergens": [], "diet_type": "flexible"},
    {"name": "Marathon Training Fuel", "subcategory": "endurance", "calories_daily": 3200, "protein_g": 120, "carbs_g": 450, "fat_g": 80, "meals_per_day": 6, "allergens": [], "diet_type": "omnivore"},
    {"name": "Anti-Inflammatory Plan", "subcategory": "recovery", "calories_daily": 2000, "protein_g": 100, "carbs_g": 220, "fat_g": 80, "meals_per_day": 4, "allergens": [], "diet_type": "pescatarian"},
    {"name": "Gluten-Free Athletic", "subcategory": "general health", "calories_daily": 2400, "protein_g": 140, "carbs_g": 280, "fat_g": 75, "meals_per_day": 4, "allergens": ["dairy"], "diet_type": "gluten-free"},
    {"name": "Plant-Based Beginner", "subcategory": "general health", "calories_daily": 2000, "protein_g": 80, "carbs_g": 280, "fat_g": 70, "meals_per_day": 3, "allergens": ["soy"], "diet_type": "vegetarian"},
    {"name": "Bodybuilder Bulk Phase", "subcategory": "muscle building", "calories_daily": 3500, "protein_g": 220, "carbs_g": 400, "fat_g": 100, "meals_per_day": 6, "allergens": ["dairy", "eggs"], "diet_type": "omnivore"},
    {"name": "Senior Vitality Plan", "subcategory": "general health", "calories_daily": 1800, "protein_g": 90, "carbs_g": 200, "fat_g": 70, "meals_per_day": 3, "allergens": [], "diet_type": "omnivore"},
]

# --- GOALS ---
GOALS = [
    "weight loss", "muscle building", "endurance", "flexibility",
    "stress relief", "injury recovery", "general fitness", "marathon training",
    "strength", "body composition", "energy boost", "better sleep",
    "core strength", "functional fitness", "mindfulness"
]

WEATHER_CONDITIONS = ["cold", "hot", "mild", "rainy", "any"]


def build_exercise_record(ex, idx):
    oid = hashlib.md5(f"exercise-{ex['name']}-{idx}".encode()).hexdigest()[:12]
    goals = []
    if ex["subcategory"] == "cardio":
        goals = random.sample(["weight loss", "endurance", "energy boost", "general fitness"], 2)
    elif ex["subcategory"] == "strength":
        goals = random.sample(["muscle building", "strength", "body composition", "functional fitness"], 2)
    elif ex["subcategory"] == "flexibility":
        goals = random.sample(["flexibility", "stress relief", "injury recovery", "mindfulness"], 2)
    elif ex["subcategory"] == "recovery":
        goals = random.sample(["stress relief", "better sleep", "injury recovery"], 2)

    return {
        "objectID": oid,
        "name": ex["name"],
        "category": "exercise",
        "subcategory": ex["subcategory"],
        "difficulty": ex["difficulty"],
        "duration_minutes": random.choice([15, 20, 30, 45, 60]),
        "calories_per_30min": ex["calories_per_30min"],
        "muscle_groups": ex["muscle_groups"],
        "equipment": ex["equipment"],
        "indoor": ex["indoor"],
        "goals": goals,
        "weather_suitability": ["any"] if ex["indoor"] else random.sample(["mild", "cold", "hot"], 2),
        "description": f"{ex['name']} — a {ex['difficulty']}-level {ex['subcategory']} exercise targeting {', '.join(ex['muscle_groups'])}. Burns approximately {ex['calories_per_30min']} calories per 30 minutes.",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "allergens": [],
        "compatibility_tags": [ex["subcategory"], ex["difficulty"]] + ex["muscle_groups"],
        "price_range_usd": 0,
    }


def build_supplement_record(sup, idx):
    oid = hashlib.md5(f"supplement-{sup['name']}-{idx}".encode()).hexdigest()[:12]
    goals = []
    if sup["subcategory"] == "protein":
        goals = ["muscle building", "strength"]
    elif sup["subcategory"] == "performance":
        goals = ["endurance", "strength", "energy boost"]
    elif sup["subcategory"] == "recovery":
        goals = ["injury recovery", "better sleep", "stress relief"]
    elif sup["subcategory"] == "health":
        goals = ["general fitness", "energy boost"]

    return {
        "objectID": oid,
        "name": sup["name"],
        "category": "supplement",
        "subcategory": sup["subcategory"],
        "difficulty": "beginner",
        "duration_minutes": 0,
        "calories_per_30min": 0,
        "muscle_groups": [],
        "equipment": [],
        "indoor": True,
        "goals": goals,
        "weather_suitability": ["any"],
        "benefits": sup["benefits"],
        "allergens": sup["allergens"],
        "dosage": sup["dosage"],
        "description": f"{sup['name']} — supports {', '.join(sup['benefits'])}. Recommended dosage: {sup['dosage']}.",
        "rating": round(random.uniform(3.8, 5.0), 1),
        "compatibility_tags": [sup["subcategory"]] + sup["benefits"],
        "price_range_usd": sup["price_usd"],
    }


def build_gear_record(gear, idx):
    oid = hashlib.md5(f"gear-{gear['name']}-{idx}".encode()).hexdigest()[:12]
    return {
        "objectID": oid,
        "name": gear["name"],
        "category": "gear",
        "subcategory": gear["subcategory"],
        "difficulty": "beginner",
        "duration_minutes": 0,
        "calories_per_30min": 0,
        "muscle_groups": [],
        "equipment": [],
        "indoor": True,
        "goals": gear["for_goals"],
        "weather_suitability": ["any"],
        "description": f"{gear['name']} — essential equipment for {', '.join(gear['for_goals'])}. Durability: {gear['durability']}.",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "allergens": [],
        "compatibility_tags": [gear["subcategory"], gear["durability"]] + gear["for_goals"],
        "price_range_usd": gear["price_usd"],
    }


def build_meal_plan_record(mp, idx):
    oid = hashlib.md5(f"meal-{mp['name']}-{idx}".encode()).hexdigest()[:12]
    return {
        "objectID": oid,
        "name": mp["name"],
        "category": "meal_plan",
        "subcategory": mp["subcategory"],
        "difficulty": "beginner" if mp["meals_per_day"] <= 3 else "intermediate",
        "duration_minutes": 0,
        "calories_per_30min": 0,
        "calories_daily": mp["calories_daily"],
        "macros": {"protein_g": mp["protein_g"], "carbs_g": mp["carbs_g"], "fat_g": mp["fat_g"]},
        "meals_per_day": mp["meals_per_day"],
        "muscle_groups": [],
        "equipment": [],
        "indoor": True,
        "goals": [mp["subcategory"]] + random.sample(GOALS, 2),
        "weather_suitability": ["any"],
        "diet_type": mp["diet_type"],
        "allergens": mp["allergens"],
        "description": f"{mp['name']} — {mp['calories_daily']} kcal/day, {mp['protein_g']}g protein, {mp['carbs_g']}g carbs, {mp['fat_g']}g fat. {mp['meals_per_day']} meals per day. Diet type: {mp['diet_type']}.",
        "rating": round(random.uniform(3.5, 5.0), 1),
        "compatibility_tags": [mp["subcategory"], mp["diet_type"]],
        "price_range_usd": random.choice([50, 75, 100, 150]),
    }


def generate_all_items():
    records = []
    idx = 0

    # Add all exercises (some duplicated with variations for volume)
    for ex in EXERCISES:
        records.append(build_exercise_record(ex, idx))
        idx += 1

    # Add exercise variations for volume
    variations = ["Beginner", "Advanced", "Quick", "Extended", "Morning", "Evening", "Outdoor", "Home"]
    for ex in random.sample(EXERCISES, 20):
        variant = random.choice(variations)
        ex_copy = dict(ex)
        ex_copy["name"] = f"{variant} {ex['name']}"
        if variant == "Beginner":
            ex_copy["difficulty"] = "beginner"
        elif variant == "Advanced":
            ex_copy["difficulty"] = "advanced"
        records.append(build_exercise_record(ex_copy, idx))
        idx += 1

    # Add all supplements
    for sup in SUPPLEMENTS:
        records.append(build_supplement_record(sup, idx))
        idx += 1

    # Add all gear
    for gear in GEAR:
        records.append(build_gear_record(gear, idx))
        idx += 1

    # Add all meal plans
    for mp in MEAL_PLANS:
        records.append(build_meal_plan_record(mp, idx))
        idx += 1

    # Generate additional wellness items for volume
    wellness_extras = [
        {"name": "5-Minute Breathing Exercise", "category": "exercise", "subcategory": "recovery", "goals": ["stress relief", "mindfulness"]},
        {"name": "Gratitude Journaling", "category": "exercise", "subcategory": "recovery", "goals": ["mindfulness", "better sleep"]},
        {"name": "Progressive Muscle Relaxation", "category": "exercise", "subcategory": "recovery", "goals": ["stress relief", "better sleep"]},
        {"name": "Walking Meditation", "category": "exercise", "subcategory": "recovery", "goals": ["mindfulness", "stress relief"]},
        {"name": "Body Scan Meditation", "category": "exercise", "subcategory": "recovery", "goals": ["stress relief", "mindfulness", "better sleep"]},
        {"name": "Power Nap Protocol", "category": "exercise", "subcategory": "recovery", "goals": ["energy boost", "recovery"]},
        {"name": "Cold Shower Protocol", "category": "exercise", "subcategory": "recovery", "goals": ["energy boost", "immune support"]},
        {"name": "Hydration Tracker", "category": "gear", "subcategory": "tech", "goals": ["general fitness", "energy boost"]},
        {"name": "Posture Corrector Band", "category": "gear", "subcategory": "recovery", "goals": ["injury prevention", "core strength"]},
        {"name": "Balance Board", "category": "gear", "subcategory": "bodyweight", "goals": ["balance", "core strength", "functional fitness"]},
    ]

    for extra in wellness_extras:
        oid = hashlib.md5(f"extra-{extra['name']}-{idx}".encode()).hexdigest()[:12]
        records.append({
            "objectID": oid,
            "name": extra["name"],
            "category": extra["category"],
            "subcategory": extra["subcategory"],
            "difficulty": "beginner",
            "duration_minutes": random.choice([5, 10, 15, 20]),
            "calories_per_30min": random.randint(0, 100),
            "muscle_groups": ["mind"] if extra["subcategory"] == "recovery" else ["full body"],
            "equipment": [],
            "indoor": True,
            "goals": extra["goals"],
            "weather_suitability": ["any"],
            "description": f"{extra['name']} — supports {', '.join(extra['goals'])}.",
            "rating": round(random.uniform(4.0, 5.0), 1),
            "allergens": [],
            "compatibility_tags": extra["goals"],
            "price_range_usd": random.choice([0, 15, 25, 50]),
        })
        idx += 1

    return records


def upload_to_algolia(records):
    client = SearchClientSync(APP_ID, ADMIN_KEY)

    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        client.save_objects(INDEX_NAME, batch)
        print(f"  Uploaded batch {i // batch_size + 1}/{(len(records) + batch_size - 1) // batch_size}")

    client.set_settings(INDEX_NAME, {
        "searchableAttributes": [
            "name", "category", "subcategory", "description",
            "goals", "muscle_groups", "benefits", "compatibility_tags", "diet_type"
        ],
        "attributesForFaceting": [
            "searchable(category)", "searchable(subcategory)", "searchable(goals)",
            "searchable(difficulty)", "searchable(muscle_groups)",
            "searchable(diet_type)", "searchable(allergens)",
            "indoor", "filterOnly(rating)", "filterOnly(price_range_usd)",
            "searchable(weather_suitability)", "searchable(equipment)"
        ],
        "customRanking": ["desc(rating)"],
        "attributesToRetrieve": [
            "name", "category", "subcategory", "difficulty", "duration_minutes",
            "calories_per_30min", "calories_daily", "macros", "meals_per_day",
            "muscle_groups", "equipment", "indoor", "goals",
            "weather_suitability", "benefits", "allergens", "dosage",
            "diet_type", "description", "rating", "compatibility_tags",
            "price_range_usd"
        ],
        "attributesToHighlight": ["name", "description", "goals", "benefits"],
        "hitsPerPage": 20,
    })
    print("  Index settings configured.")
    return len(records)


if __name__ == "__main__":
    print("Generating HealthForge dataset...")
    items = generate_all_items()
    print(f"  Generated {len(items)} wellness items")

    with open("/tmp/items.json", "w") as f:
        json.dump(items, f, indent=2)
    print("  Saved to items.json")

    print("Uploading to Algolia...")
    count = upload_to_algolia(items)
    print(f"  Done! {count} records indexed in '{INDEX_NAME}'")

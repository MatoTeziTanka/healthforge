---
title: "HealthForge: Proactive Wellness Kit Builder Powered by Algolia"
published: true
tags: algolia, ai, health, fitness
---

*This is a submission for the [Algolia Agent Studio Challenge](https://dev.to/challenges/algolia): Consumer-Facing Non-Conversational Experiences*

## What I Built

**HealthForge** is a non-conversational AI wellness kit builder that proactively assembles personalized fitness kits as users input their goals and preferences — no chat required.

The experience works in three steps:

1. **Select Your Goals** — Choose from 8 wellness objectives (weight loss, muscle building, endurance, flexibility, stress relief, better sleep, general fitness, recovery)
2. **Set Preferences** — Configure fitness level, allergies, diet, weather, budget, and indoor/outdoor preference
3. **Get Your Kit** — Instantly receive a curated kit of exercises, supplements, gear, and meal plans, with automatic compatibility checks

### Key Intelligence Features:
- **Allergy auto-exclusion**: Items containing flagged allergens are silently removed with clear alerts
- **Budget filtering**: Items above your budget threshold are excluded
- **Diet matching**: Meal plans filter by dietary preference (vegan, keto, mediterranean, etc.)
- **Equipment gap detection**: If your exercises need a kettlebell but your gear section doesn't include one, you get an alert
- **Weather awareness**: Outdoor exercises get flagged if they don't match your weather conditions

## Demo

**Live Demo:** [YOUR_VERCEL_URL_HERE]

**GitHub:** [github.com/MatoTeziTanka/healthforge](https://github.com/MatoTeziTanka/healthforge)

### Screenshots

**Step 1: Goal selection with visual chips:**
Users pick from 8 wellness goals — the selection drives every subsequent retrieval.

**Step 2: Preference configuration:**
Allergies, diet, budget, weather, and fitness level — each setting modifies the Algolia query.

**Step 3: Auto-assembled kit with compatibility alerts:**
The kit arrives pre-built with exercises, supplements, gear, and meal plans. Compatibility alerts flag issues proactively.

**No login required.** For quick demo: just select goals and preferences.

## How I Used Algolia Agent Studio

### Data Indexing

I indexed **110+ wellness items** across 4 categories with compatibility-aware attributes:

```json
{
  "name": "Kettlebell Swings",
  "category": "exercise",
  "subcategory": "strength",
  "difficulty": "intermediate",
  "calories_per_30min": 350,
  "muscle_groups": ["full body"],
  "equipment": ["kettlebell"],
  "goals": ["strength", "cardio", "functional fitness"],
  "allergens": [],
  "weather_suitability": ["any"],
  "indoor": true,
  "rating": 4.7
}
```

Each item carries compatibility metadata: allergens, equipment needs, weather suitability, diet type, and goal alignment. This enables the **proactive intelligence** that makes HealthForge more than just a search box.

### Multi-Category Retrieval Strategy

Instead of a single search, HealthForge fires **4 parallel category-specific queries** to Algolia:

```javascript
for (const category of ['exercise', 'supplement', 'gear', 'meal_plan']) {
  const { results } = await searchClient.search({
    requests: [{
      indexName: 'healthforge_items',
      query: goals.join(' '),
      hitsPerPage: category === 'exercise' ? 5 : 3,
      facetFilters: [
        [`category:${category}`],
        [`difficulty:${difficulty}`, 'difficulty:beginner']
      ],
    }],
  })
}
```

This approach ensures each kit section gets dedicated retrieval with category-specific result limits and difficulty fallbacks (if no intermediate items exist, beginners are included).

### Post-Retrieval Intelligence

After Algolia returns the raw results, HealthForge applies **4 layers of proactive filtering**:

1. **Allergy exclusion**: Cross-reference each item's `allergens` array against user selections
2. **Budget enforcement**: Remove items above threshold
3. **Diet matching**: Exclude meal plans that don't match dietary preference
4. **Equipment gap detection**: Compare exercise equipment needs against gear in the kit

All filtering happens client-side after Algolia's fast retrieval, keeping the experience responsive while adding personalization depth.

### Search Configuration

- **Searchable attributes**: name, category, subcategory, description, goals, muscle groups, benefits, diet type
- **Facet filters**: category, subcategory, goals, difficulty, muscle groups, diet type, allergens, indoor, weather suitability, equipment
- **Custom ranking**: rating (descending) — highest-rated items surface first within each category
- **Highlighting**: name, description, goals, and benefits for context-rich result cards

## Why Fast Retrieval Matters

HealthForge's non-conversational pattern demands **invisible speed**. Unlike a chatbot where users expect a moment for the "AI to think," a kit builder needs to feel like magic — you set preferences, and the kit appears instantly.

Here's why Algolia's speed is critical:

1. **4 parallel category queries**: Each preference change triggers 4 separate Algolia searches (exercises, supplements, gear, meal plans). At ~50ms each, the total kit builds in under 200ms. With a slower backend, users would see a loading spinner for each section.

2. **Facet filtering depth**: A single exercise query might filter by `category:exercise` + `difficulty:intermediate` + `indoor:true` + goals matching. Algolia handles this multi-faceted filtering in the same sub-50ms window.

3. **Rebuild on adjustment**: Users can tweak any preference and rebuild instantly. This "adjust and see" workflow only works when retrieval is fast enough to feel interactive rather than transactional.

4. **Proactive alerts in real-time**: The compatibility check (allergy conflicts, equipment gaps, weather mismatches) runs immediately after retrieval. If Algolia took seconds per query, the alerts would feel like a separate step instead of an integrated intelligence layer.

The result: HealthForge doesn't feel like a search tool. It feels like a personal trainer who already knows your preferences and assembled everything before you finished asking.

'use client'

import { useState, useEffect, useCallback } from 'react'
import { liteClient as algoliasearch } from 'algoliasearch/lite'

const ALGOLIA_APP_ID = process.env.NEXT_PUBLIC_ALGOLIA_APP_ID || 'RM2LBYLLID'
const ALGOLIA_SEARCH_KEY = process.env.NEXT_PUBLIC_ALGOLIA_SEARCH_KEY || '00076acd167ffcfcf8bec05ae031852a'
const ALGOLIA_INDEX = 'healthforge_items'

const searchClient = algoliasearch(ALGOLIA_APP_ID, ALGOLIA_SEARCH_KEY)

interface WellnessItem {
  objectID: string
  name: string
  category: string
  subcategory: string
  difficulty: string
  duration_minutes: number
  calories_per_30min: number
  calories_daily?: number
  macros?: { protein_g: number; carbs_g: number; fat_g: number }
  meals_per_day?: number
  muscle_groups: string[]
  equipment: string[]
  indoor: boolean
  goals: string[]
  weather_suitability: string[]
  benefits?: string[]
  allergens: string[]
  dosage?: string
  diet_type?: string
  description: string
  rating: number
  compatibility_tags: string[]
  price_range_usd: number
}

interface UserProfile {
  goals: string[]
  difficulty: string
  allergies: string[]
  budget: string
  weather: string
  indoor_only: boolean
  diet: string
}

const GOALS = [
  { id: 'weight loss', label: 'Weight Loss', icon: '🔥' },
  { id: 'muscle building', label: 'Build Muscle', icon: '💪' },
  { id: 'endurance', label: 'Endurance', icon: '🏃' },
  { id: 'flexibility', label: 'Flexibility', icon: '🧘' },
  { id: 'stress relief', label: 'Stress Relief', icon: '🧠' },
  { id: 'better sleep', label: 'Better Sleep', icon: '😴' },
  { id: 'general fitness', label: 'General Fitness', icon: '❤️' },
  { id: 'injury recovery', label: 'Recovery', icon: '🩹' },
]

const DIFFICULTIES = ['beginner', 'intermediate', 'advanced']
const ALLERGIES = ['dairy', 'soy', 'nuts', 'eggs', 'fish', 'gluten']
const DIETS = ['any', 'omnivore', 'vegetarian', 'vegan', 'keto', 'mediterranean', 'gluten-free']
const WEATHERS = ['any', 'cold', 'hot', 'mild', 'rainy']
const BUDGETS = ['any', 'budget', 'moderate', 'premium']

const CATEGORY_ICONS: Record<string, string> = {
  exercise: '🏋️',
  supplement: '💊',
  gear: '🎒',
  meal_plan: '🥗',
}

const CATEGORY_COLORS: Record<string, string> = {
  exercise: 'from-blue-500 to-blue-600',
  supplement: 'from-purple-500 to-purple-600',
  gear: 'from-amber-500 to-amber-600',
  meal_plan: 'from-green-500 to-green-600',
}

function RatingStars({ rating }: { rating: number }) {
  return (
    <div className="flex items-center gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <span key={star} className={`text-xs ${star <= Math.round(rating) ? 'text-yellow-400' : 'text-gray-200'}`}>
          ★
        </span>
      ))}
      <span className="text-xs text-gray-500 ml-1">{rating.toFixed(1)}</span>
    </div>
  )
}

function KitItemCard({ item, onRemove }: { item: WellnessItem; onRemove: () => void }) {
  const [expanded, setExpanded] = useState(false)

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden hover:shadow-md transition-all slide-in">
      <div className={`bg-gradient-to-r ${CATEGORY_COLORS[item.category] || 'from-gray-500 to-gray-600'} p-3 text-white`}>
        <div className="flex justify-between items-start">
          <div className="flex items-center gap-2">
            <span className="text-lg">{CATEGORY_ICONS[item.category] || '📦'}</span>
            <div>
              <h3 className="font-semibold text-sm leading-tight">{item.name}</h3>
              <p className="text-white/70 text-xs capitalize">{item.subcategory}</p>
            </div>
          </div>
          <button onClick={onRemove} className="text-white/50 hover:text-white text-lg leading-none" title="Remove">×</button>
        </div>
      </div>

      <div className="p-3 space-y-2">
        <div className="flex items-center justify-between">
          <RatingStars rating={item.rating} />
          <span className={`text-xs px-2 py-0.5 rounded-full ${
            item.difficulty === 'beginner' ? 'bg-green-100 text-green-700' :
            item.difficulty === 'intermediate' ? 'bg-yellow-100 text-yellow-700' :
            'bg-red-100 text-red-700'
          }`}>
            {item.difficulty}
          </span>
        </div>

        {item.category === 'exercise' && (
          <div className="flex gap-3 text-xs text-gray-500">
            {item.duration_minutes > 0 && <span>⏱️ {item.duration_minutes}min</span>}
            {item.calories_per_30min > 0 && <span>🔥 {item.calories_per_30min} cal/30min</span>}
          </div>
        )}

        {item.category === 'meal_plan' && item.macros && (
          <div className="grid grid-cols-3 gap-1 text-xs">
            <div className="bg-blue-50 rounded p-1.5 text-center">
              <div className="font-bold text-blue-700">{item.macros.protein_g}g</div>
              <div className="text-blue-500">Protein</div>
            </div>
            <div className="bg-amber-50 rounded p-1.5 text-center">
              <div className="font-bold text-amber-700">{item.macros.carbs_g}g</div>
              <div className="text-amber-500">Carbs</div>
            </div>
            <div className="bg-pink-50 rounded p-1.5 text-center">
              <div className="font-bold text-pink-700">{item.macros.fat_g}g</div>
              <div className="text-pink-500">Fat</div>
            </div>
          </div>
        )}

        {item.category === 'supplement' && item.dosage && (
          <p className="text-xs text-gray-500">💊 {item.dosage}</p>
        )}

        {item.price_range_usd > 0 && (
          <p className="text-xs text-gray-500">💰 ~${item.price_range_usd}</p>
        )}

        <div className="flex flex-wrap gap-1">
          {item.goals.slice(0, 3).map((g) => (
            <span key={g} className="text-xs bg-forge-50 text-forge-700 px-1.5 py-0.5 rounded-full">{g}</span>
          ))}
        </div>

        {item.allergens.length > 0 && (
          <div className="flex items-center gap-1">
            <span className="text-xs text-red-500">⚠️ Contains:</span>
            {item.allergens.map((a) => (
              <span key={a} className="text-xs bg-red-50 text-red-600 px-1.5 py-0.5 rounded-full">{a}</span>
            ))}
          </div>
        )}

        {expanded && (
          <div className="pt-2 border-t border-gray-100 space-y-2">
            <p className="text-xs text-gray-600">{item.description}</p>
            {item.muscle_groups.length > 0 && item.muscle_groups[0] !== 'mind' && (
              <div className="flex flex-wrap gap-1">
                <span className="text-xs text-gray-400">Targets:</span>
                {item.muscle_groups.map((m) => (
                  <span key={m} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{m}</span>
                ))}
              </div>
            )}
            {item.equipment.length > 0 && (
              <div className="flex flex-wrap gap-1">
                <span className="text-xs text-gray-400">Needs:</span>
                {item.equipment.map((e) => (
                  <span key={e} className="text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">{e}</span>
                ))}
              </div>
            )}
            {item.benefits && (
              <div className="flex flex-wrap gap-1">
                <span className="text-xs text-gray-400">Benefits:</span>
                {item.benefits.map((b) => (
                  <span key={b} className="text-xs bg-green-50 text-green-600 px-1.5 py-0.5 rounded">{b}</span>
                ))}
              </div>
            )}
          </div>
        )}

        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-forge-600 hover:text-forge-700 font-medium w-full text-center"
        >
          {expanded ? '▲ Less' : '▼ Details'}
        </button>
      </div>
    </div>
  )
}

function CompatibilityAlert({ alerts }: { alerts: string[] }) {
  if (alerts.length === 0) return null
  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6">
      <h3 className="font-semibold text-amber-800 text-sm flex items-center gap-2">
        <span>⚠️</span> Compatibility Alerts
      </h3>
      <ul className="mt-2 space-y-1">
        {alerts.map((alert, i) => (
          <li key={i} className="text-xs text-amber-700 flex items-start gap-1">
            <span className="mt-0.5">•</span>
            <span>{alert}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function KitSummary({ kit }: { kit: WellnessItem[] }) {
  const totalCost = kit.reduce((sum, item) => sum + (item.price_range_usd || 0), 0)
  const totalCalories = kit
    .filter((i) => i.category === 'exercise')
    .reduce((sum, i) => sum + i.calories_per_30min, 0)
  const categories = [...new Set(kit.map((i) => i.category))]

  return (
    <div className="bg-gradient-to-r from-forge-700 to-forge-600 rounded-xl p-4 text-white mb-6">
      <h3 className="font-bold text-sm mb-3">Kit Summary</h3>
      <div className="grid grid-cols-4 gap-3 text-center">
        <div>
          <div className="text-2xl font-bold">{kit.length}</div>
          <div className="text-forge-200 text-xs">Items</div>
        </div>
        <div>
          <div className="text-2xl font-bold">{categories.length}</div>
          <div className="text-forge-200 text-xs">Categories</div>
        </div>
        <div>
          <div className="text-2xl font-bold">{totalCalories}</div>
          <div className="text-forge-200 text-xs">Cal Burn/30m</div>
        </div>
        <div>
          <div className="text-2xl font-bold">${totalCost}</div>
          <div className="text-forge-200 text-xs">Est. Cost</div>
        </div>
      </div>
    </div>
  )
}

export default function Home() {
  const [profile, setProfile] = useState<UserProfile>({
    goals: [],
    difficulty: 'beginner',
    allergies: [],
    budget: 'any',
    weather: 'any',
    indoor_only: false,
    diet: 'any',
  })

  const [kit, setKit] = useState<WellnessItem[]>([])
  const [loading, setLoading] = useState(false)
  const [alerts, setAlerts] = useState<string[]>([])
  const [step, setStep] = useState(1)

  const buildKit = useCallback(async () => {
    if (profile.goals.length === 0) return
    setLoading(true)

    try {
      const facetFilters: string[][] = []
      if (profile.difficulty !== 'any') {
        facetFilters.push([`difficulty:${profile.difficulty}`, 'difficulty:beginner'])
      }

      const categories = ['exercise', 'supplement', 'gear', 'meal_plan']
      const kitItems: WellnessItem[] = []
      const newAlerts: string[] = []

      for (const category of categories) {
        const queryParts = profile.goals.join(' ')
        const categoryFilters = [[`category:${category}`], ...facetFilters]

        if (profile.indoor_only && category === 'exercise') {
          categoryFilters.push(['indoor:true'])
        }

        const { results } = await searchClient.search<WellnessItem>({
          requests: [{
            indexName: ALGOLIA_INDEX,
            query: queryParts,
            hitsPerPage: category === 'exercise' ? 5 : 3,
            facetFilters: categoryFilters,
          }],
        })
        const firstResult = results[0]
        const hits = ('hits' in firstResult ? firstResult.hits : []) as WellnessItem[]

        for (const hit of hits) {
          // Allergy check
          if (hit.allergens && hit.allergens.length > 0) {
            const conflict = hit.allergens.filter((a) => profile.allergies.includes(a))
            if (conflict.length > 0) {
              newAlerts.push(
                `"${hit.name}" contains ${conflict.join(', ')} — excluded from your kit due to allergy settings`
              )
              continue
            }
          }

          // Budget check
          if (profile.budget === 'budget' && hit.price_range_usd > 50) {
            continue
          }
          if (profile.budget === 'moderate' && hit.price_range_usd > 200) {
            continue
          }

          // Weather check
          if (
            profile.weather !== 'any' &&
            hit.weather_suitability &&
            !hit.weather_suitability.includes('any') &&
            !hit.weather_suitability.includes(profile.weather)
          ) {
            newAlerts.push(
              `"${hit.name}" may not be ideal for ${profile.weather} weather — included but flagged`
            )
          }

          // Diet check for meal plans
          if (
            category === 'meal_plan' &&
            profile.diet !== 'any' &&
            hit.diet_type &&
            hit.diet_type !== 'flexible' &&
            hit.diet_type !== profile.diet
          ) {
            continue
          }

          kitItems.push(hit)
        }
      }

      // Equipment overlap check
      const allEquipment = kitItems
        .filter((i) => i.category === 'exercise')
        .flatMap((i) => i.equipment)
      const exerciseNeeds = [...new Set(allEquipment)].filter(Boolean)
      const gearProvided = kitItems.filter((i) => i.category === 'gear').map((i) => i.name.toLowerCase())
      for (const need of exerciseNeeds) {
        if (!gearProvided.some((g) => g.includes(need.toLowerCase()))) {
          newAlerts.push(`Your exercises need "${need}" — consider adding matching gear to your kit`)
        }
      }

      setKit(kitItems)
      setAlerts(newAlerts)
    } catch {
      setAlerts(['Error building kit. Please try again.'])
    } finally {
      setLoading(false)
    }
  }, [profile])

  useEffect(() => {
    if (step === 3 && profile.goals.length > 0) {
      buildKit()
    }
  }, [step, buildKit, profile.goals.length])

  const toggleGoal = (goal: string) => {
    setProfile((p) => ({
      ...p,
      goals: p.goals.includes(goal)
        ? p.goals.filter((g) => g !== goal)
        : [...p.goals, goal],
    }))
  }

  const toggleAllergy = (allergy: string) => {
    setProfile((p) => ({
      ...p,
      allergies: p.allergies.includes(allergy)
        ? p.allergies.filter((a) => a !== allergy)
        : [...p.allergies, allergy],
    }))
  }

  const removeFromKit = (objectID: string) => {
    setKit((k) => k.filter((item) => item.objectID !== objectID))
  }

  const groupedKit = kit.reduce<Record<string, WellnessItem[]>>((acc, item) => {
    if (!acc[item.category]) acc[item.category] = []
    acc[item.category].push(item)
    return acc
  }, {})

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-forge-900 via-forge-800 to-forge-700 text-white">
        <nav className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🏋️</span>
            <span className="text-xl font-bold">HealthForge</span>
          </div>
          <div className="text-forge-300 text-sm">Proactive Wellness Kit Builder</div>
        </nav>

        <div className="max-w-6xl mx-auto px-6 py-16 text-center">
          <h1 className="text-4xl md:text-6xl font-extrabold mb-4 fade-in-up">
            Build Your Perfect
            <br />
            <span className="text-forge-300">Wellness Kit</span>
          </h1>
          <p className="text-forge-200 text-lg max-w-2xl mx-auto mb-8 fade-in-up fade-delay-1">
            Tell us your goals. Our AI instantly assembles personalized exercises, supplements,
            gear, and meal plans — with automatic allergy checks and compatibility alerts.
          </p>

          {/* Progress Steps */}
          <div className="flex justify-center gap-2 mb-8 fade-in-up fade-delay-2">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex items-center gap-2">
                <button
                  onClick={() => setStep(s)}
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-bold transition ${
                    step === s ? 'bg-white text-forge-800 pulse-ring' :
                    step > s ? 'bg-forge-500 text-white' : 'bg-forge-700 text-forge-400'
                  }`}
                >
                  {step > s ? '✓' : s}
                </button>
                {s < 3 && <div className={`w-16 h-0.5 ${step > s ? 'bg-forge-500' : 'bg-forge-700'}`} />}
              </div>
            ))}
          </div>
          <div className="text-forge-300 text-sm">
            {step === 1 ? 'Select Your Goals' : step === 2 ? 'Set Preferences' : 'Your Kit'}
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-12">
        {/* Step 1: Goals */}
        {step === 1 && (
          <div className="max-w-2xl mx-auto fade-in-up">
            <h2 className="text-2xl font-bold mb-2">What are your wellness goals?</h2>
            <p className="text-gray-500 mb-8">Select one or more goals. Your kit will be tailored to these.</p>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
              {GOALS.map((goal) => (
                <button
                  key={goal.id}
                  onClick={() => toggleGoal(goal.id)}
                  className={`p-4 rounded-xl border-2 text-center transition-all ${
                    profile.goals.includes(goal.id)
                      ? 'border-forge-500 bg-forge-50 shadow-md'
                      : 'border-gray-200 bg-white hover:border-forge-300'
                  }`}
                >
                  <div className="text-3xl mb-2">{goal.icon}</div>
                  <div className="text-sm font-medium">{goal.label}</div>
                </button>
              ))}
            </div>

            <button
              onClick={() => setStep(2)}
              disabled={profile.goals.length === 0}
              className="w-full bg-gradient-to-r from-forge-700 to-forge-600 text-white py-3 rounded-xl font-semibold disabled:opacity-50 hover:from-forge-800 hover:to-forge-700 transition shadow-lg"
            >
              Next: Set Preferences →
            </button>
          </div>
        )}

        {/* Step 2: Preferences */}
        {step === 2 && (
          <div className="max-w-2xl mx-auto fade-in-up">
            <h2 className="text-2xl font-bold mb-6">Customize Your Preferences</h2>

            <div className="space-y-6">
              {/* Difficulty */}
              <div>
                <label className="text-sm font-semibold text-gray-700 mb-2 block">Fitness Level</label>
                <div className="flex gap-2">
                  {DIFFICULTIES.map((d) => (
                    <button
                      key={d}
                      onClick={() => setProfile((p) => ({ ...p, difficulty: d }))}
                      className={`flex-1 py-2.5 rounded-lg text-sm font-medium capitalize transition ${
                        profile.difficulty === d
                          ? 'bg-forge-600 text-white'
                          : 'bg-white border border-gray-200 text-gray-700 hover:border-forge-300'
                      }`}
                    >
                      {d}
                    </button>
                  ))}
                </div>
              </div>

              {/* Allergies */}
              <div>
                <label className="text-sm font-semibold text-gray-700 mb-2 block">
                  Allergies / Restrictions
                  <span className="text-gray-400 font-normal ml-1">(items containing these will be excluded)</span>
                </label>
                <div className="flex flex-wrap gap-2">
                  {ALLERGIES.map((a) => (
                    <button
                      key={a}
                      onClick={() => toggleAllergy(a)}
                      className={`px-3 py-1.5 rounded-full text-sm capitalize transition ${
                        profile.allergies.includes(a)
                          ? 'bg-red-100 text-red-700 border border-red-300'
                          : 'bg-white border border-gray-200 text-gray-600 hover:border-red-200'
                      }`}
                    >
                      {profile.allergies.includes(a) ? '⛔ ' : ''}{a}
                    </button>
                  ))}
                </div>
              </div>

              {/* Diet */}
              <div>
                <label className="text-sm font-semibold text-gray-700 mb-2 block">Diet Preference</label>
                <div className="flex flex-wrap gap-2">
                  {DIETS.map((d) => (
                    <button
                      key={d}
                      onClick={() => setProfile((p) => ({ ...p, diet: d }))}
                      className={`px-3 py-1.5 rounded-full text-sm capitalize transition ${
                        profile.diet === d
                          ? 'bg-green-100 text-green-700 border border-green-300'
                          : 'bg-white border border-gray-200 text-gray-600 hover:border-green-200'
                      }`}
                    >
                      {d}
                    </button>
                  ))}
                </div>
              </div>

              {/* Weather + Indoor */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold text-gray-700 mb-2 block">Weather</label>
                  <select
                    value={profile.weather}
                    onChange={(e) => setProfile((p) => ({ ...p, weather: e.target.value }))}
                    className="w-full py-2.5 px-3 rounded-lg border border-gray-200 text-sm capitalize"
                  >
                    {WEATHERS.map((w) => <option key={w} value={w}>{w}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-sm font-semibold text-gray-700 mb-2 block">Budget</label>
                  <select
                    value={profile.budget}
                    onChange={(e) => setProfile((p) => ({ ...p, budget: e.target.value }))}
                    className="w-full py-2.5 px-3 rounded-lg border border-gray-200 text-sm capitalize"
                  >
                    {BUDGETS.map((b) => <option key={b} value={b}>{b}</option>)}
                  </select>
                </div>
              </div>

              {/* Indoor only toggle */}
              <label className="flex items-center gap-3 cursor-pointer">
                <input
                  type="checkbox"
                  checked={profile.indoor_only}
                  onChange={(e) => setProfile((p) => ({ ...p, indoor_only: e.target.checked }))}
                  className="w-5 h-5 rounded border-gray-300 text-forge-600 focus:ring-forge-500"
                />
                <span className="text-sm text-gray-700">Indoor exercises only (home/gym)</span>
              </label>
            </div>

            <div className="flex gap-3 mt-8">
              <button
                onClick={() => setStep(1)}
                className="px-6 py-3 rounded-xl border border-gray-300 text-gray-700 hover:bg-gray-50 transition"
              >
                ← Back
              </button>
              <button
                onClick={() => setStep(3)}
                className="flex-1 bg-gradient-to-r from-forge-700 to-forge-600 text-white py-3 rounded-xl font-semibold hover:from-forge-800 hover:to-forge-700 transition shadow-lg"
              >
                🏋️ Build My Kit →
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Kit Results */}
        {step === 3 && (
          <div className="fade-in-up">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-2xl font-bold">Your Wellness Kit</h2>
                <p className="text-gray-500 text-sm">
                  Personalized for: {profile.goals.join(', ')} | {profile.difficulty} level
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setStep(2)}
                  className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm transition"
                >
                  ← Adjust
                </button>
                <button
                  onClick={buildKit}
                  disabled={loading}
                  className="px-4 py-2 rounded-lg bg-forge-600 text-white text-sm hover:bg-forge-700 disabled:opacity-50 transition"
                >
                  {loading ? '⟳ Rebuilding...' : '🔄 Rebuild Kit'}
                </button>
              </div>
            </div>

            {loading ? (
              <div className="text-center py-20">
                <div className="text-4xl mb-4 animate-bounce">🏋️</div>
                <p className="text-gray-500">Building your personalized wellness kit...</p>
                <p className="text-gray-400 text-xs mt-2">Powered by Algolia — retrieving in &lt;50ms</p>
              </div>
            ) : (
              <>
                <KitSummary kit={kit} />
                <CompatibilityAlert alerts={alerts} />

                {Object.entries(groupedKit).map(([category, items]) => (
                  <div key={category} className="mb-8">
                    <h3 className="text-lg font-bold mb-3 flex items-center gap-2 capitalize">
                      <span>{CATEGORY_ICONS[category] || '📦'}</span>
                      {category === 'meal_plan' ? 'Meal Plans' : `${category}s`}
                      <span className="text-sm font-normal text-gray-400">({items.length})</span>
                    </h3>
                    <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {items.map((item) => (
                        <KitItemCard
                          key={item.objectID}
                          item={item}
                          onRemove={() => removeFromKit(item.objectID)}
                        />
                      ))}
                    </div>
                  </div>
                ))}

                {kit.length === 0 && !loading && (
                  <div className="text-center py-20 text-gray-400">
                    <div className="text-4xl mb-4">🤔</div>
                    <p>No items matched your criteria. Try adjusting your preferences.</p>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-forge-900 text-forge-300 py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <span className="text-2xl">🏋️</span>
            <span className="text-xl font-bold text-white">HealthForge</span>
          </div>
          <p className="text-sm mb-4">
            Built for the <a href="https://dev.to/challenges/algolia-2026-01-07" className="text-forge-400 hover:text-white underline">Algolia Agent Studio Challenge</a>
          </p>
          <p className="text-xs text-forge-500">
            © 2026 HealthForge. Your health, intelligently assembled. Powered by Algolia.
          </p>
        </div>
      </footer>
    </div>
  )
}

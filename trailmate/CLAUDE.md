# TrailMate — Road Trip & Overlanding App
## Claude Code Project Brief

You are building **TrailMate**, a mobile app for road trippers and 4x4 overlanders.
Think Strava × iOverlander × Google Maps — built specifically for off-road and long-distance travel.

Target: React Native (Expo) → iOS App Store + Google Play Store.

---

## Tech Stack

| Layer | Library | Notes |
|---|---|---|
| Framework | React Native + Expo SDK 51+ | Use Expo managed workflow |
| Language | TypeScript (strict) | No `any` types |
| Navigation | React Navigation v6 | Bottom tabs + stack |
| Maps | react-native-maps | Google Maps; consider Mapbox later for offline |
| GPS | expo-location | Background location tracking |
| Sensors | expo-sensors | Accelerometer for inclinometer |
| Storage | expo-sqlite + AsyncStorage | SQLite for trips, AsyncStorage for settings |
| State | Zustand | Keep stores small and focused |
| UI | react-native-paper | Material Design 3 |
| Geo utils | @turf/turf | Distance, bearing, elevation calculations |
| Date utils | date-fns | All date formatting |

---

## Design System

Colors are defined in `src/constants/index.ts`:
- Primary: `#E85D04` (burnt orange — rugged)
- Background: `#1A1A2E` (dark navy)
- Surface: `#16213E`
- Card: `#0F3460`
- Text: `#E0E0E0`
- Map track color: `#E85D04`

Dark theme throughout. Clean, minimal, data-forward. No clutter.

---

## App Structure

```
src/
  screens/
    TrackingScreen.tsx     ← PRIORITY 1: Live map + GPS HUD
    PlanScreen.tsx         ← PRIORITY 2: Plan a trip with waypoints
    ToolsScreen.tsx        ← PRIORITY 3: 4x4 tools (tyre, fuel, inclinometer)
    HistoryScreen.tsx      ← PRIORITY 4: Past trips list + playback
    ProfileScreen.tsx      ← Vehicle profile + gear checklists
  components/             ← Reusable components
  store/
    tripStore.ts           ← Active trip + history (Zustand)
    vehicleStore.ts        ← Vehicle profile + settings
    planStore.ts           ← Planned trips
  hooks/
    useLocationTracking.ts ← GPS tracking hook
    useInclinometer.ts     ← Accelerometer hook
    useFuelCalculator.ts   ← Fuel range calculations
  utils/
    distance.ts            ← Haversine / turf wrappers
    formatters.ts          ← Speed, distance, time display
    storage.ts             ← SQLite helpers
  types/
    index.ts               ← All TypeScript types (already defined)
  constants/
    index.ts               ← Colors, terrain labels, tyre guide, checklists
```

---

## Core Types (already in src/types/index.ts)

- `TripPoint` — single GPS sample (lat/lng/altitude/speed/timestamp)
- `Trip` — full recorded trip with points array + stats
- `TripPhoto` — photo with GPS coordinates
- `VehicleProfile` — vehicle details + terrain-specific fuel economy + tyre pressures
- `TerrainType` — `'tarmac' | 'gravel' | 'sand' | 'mud' | 'rock'`
- `Waypoint` — POI/stop with type + optional bookingUrl
- `PlannedTrip` — pre-planned trip with waypoints + dates

---

## Feature Priorities

### Phase 1 — Build These First

#### 1. TrackingScreen (most important)
- Full-screen map (react-native-maps, dark style)
- Start/Stop Trip button
- Real-time GPS route drawn as polyline on map
- HUD overlay showing:
  - Current speed (large, km/h)
  - Total distance (km)
  - Trip duration (HH:MM:SS)
  - Current altitude (m)
  - Max speed this trip
- Center-on-user button
- Trip name prompt on Start

#### 2. ToolsScreen — 4x4 Tools
Build as a scrollable list of tool cards:

**Tyre Pressure Calculator**
- User selects terrain type (tarmac/gravel/sand/mud/rock)
- App shows recommended PSI range from `TYRE_PRESSURE_GUIDE` constant
- If vehicle profile exists, show vehicle-specific pressures
- Show warning: "Remember to re-inflate before returning to tarmac"

**Fuel Range Calculator**
- Inputs: current fuel level (%), terrain type
- Uses vehicle profile fuel economy for that terrain
- Outputs: estimated km remaining, estimated km to empty
- Shows map search button: "Find fuel stations nearby"

**Inclinometer**
- Uses expo-sensors (Accelerometer)
- Shows side tilt angle (roll) and fore/aft angle (pitch) in degrees
- Visual level indicator (like a bubble level)
- Color warning: green < 15°, orange 15-30°, red > 30° (rollover risk)

**Recovery Gear Checklist**
- List from `RECOVERY_GEAR_CHECKLIST` constant
- Checkbox each item
- "Trip ready" indicator when all checked
- Persists per-trip

#### 3. PlanScreen
- Create a new planned trip (name + dates)
- Add waypoints to a map (tap to add)
- Waypoint types: fuel, camp, accommodation, viewpoint, mechanic, water, custom
- For accommodation waypoints: add a booking URL (Booking.com / Airbnb link)
- Show estimated total distance
- Fuel stop calculator: given vehicle profile, flag if distance between fuel stops exceeds range

#### 4. HistoryScreen
- List of completed trips (name, date, distance, duration)
- Tap to open trip detail:
  - Full route on map
  - Stats summary
  - Photo gallery (GPS-tagged)
  - Elevation profile chart (use Victory Native or react-native-svg)

### Phase 2 — After Phase 1 is solid

- **Accommodation search**: Integrate with a Places API (Google Places or Foursquare) to surface nearby hotels/campsites along route, show them as map pins, tap to deep-link to booking
- **Weather overlay**: OpenWeatherMap API, show forecast for waypoints
- **Offline maps**: Investigate Mapbox SDK swap for tile caching
- **Live location sharing**: Share a link that shows your real-time position to a contact
- **GPX export/import**: Export trip as .gpx, import community tracks
- **Community tracks**: Firebase backend, users submit/rate tracks

### Phase 3 — App Store Prep
- Push notifications (trip reminders, weather alerts)
- Onboarding flow
- App icon + splash screen (assets in `/assets/icons/`)
- Privacy policy (required for location permissions on both stores)
- In-app review prompt after 3rd completed trip

---

## Key Implementation Notes

### Location Tracking
```typescript
// Always request BACKGROUND location permission for tracking while screen is off
// Use expo-location's startLocationUpdatesAsync with a TaskManager background task
// Minimum accuracy: Accuracy.BestForNavigation
// Update interval: 3000ms (3 seconds) while moving, 10000ms when stationary
// Save points to tripStore AND batch-write to SQLite every 10 points
```

### Map Style
```typescript
// Use Google Maps with customMapStyle for dark theme
// Track polyline: color '#E85D04', strokeWidth 4
// User location: show default blue dot
// Animate camera to follow user during active tracking
// Show start pin (green) and any waypoints as custom markers
```

### Speed Display
```typescript
// GPS speed is in m/s — convert to km/h: speed * 3.6
// Smooth with a rolling average of last 3 readings to avoid jitter
// Show 0 if speed < 2 km/h (GPS noise at standstill)
```

### SQLite Schema
```sql
CREATE TABLE trips (
  id TEXT PRIMARY KEY,
  name TEXT,
  started_at INTEGER,
  ended_at INTEGER,
  total_distance_km REAL,
  max_speed_kmh REAL,
  avg_speed_kmh REAL,
  notes TEXT
);

CREATE TABLE trip_points (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  trip_id TEXT,
  latitude REAL,
  longitude REAL,
  altitude REAL,
  speed REAL,
  timestamp INTEGER,
  FOREIGN KEY (trip_id) REFERENCES trips(id)
);

CREATE TABLE trip_photos (
  id TEXT PRIMARY KEY,
  trip_id TEXT,
  uri TEXT,
  latitude REAL,
  longitude REAL,
  timestamp INTEGER,
  FOREIGN KEY (trip_id) REFERENCES trips(id)
);
```

### Navigation Structure
```
App
└── BottomTabNavigator
    ├── Track (TrackingScreen) — map icon
    ├── Plan (PlanScreen) — route icon
    ├── Tools (ToolsScreen) — wrench icon
    ├── History (HistoryScreen) — clock icon
    └── Profile (ProfileScreen) — person icon
```

---

## Permissions Required

**iOS (Info.plist):**
- `NSLocationWhenInUseUsageDescription` — "TrailMate tracks your route while the app is open"
- `NSLocationAlwaysAndWhenInUseUsageDescription` — "TrailMate tracks your route in the background so you don't miss any part of your journey"
- `NSCameraUsageDescription` — "Take photos along your route"
- `NSPhotoLibraryAddUsageDescription` — "Save trip photos to your photo library"

**Android (AndroidManifest.xml via app.json):**
- `ACCESS_FINE_LOCATION`
- `ACCESS_BACKGROUND_LOCATION`
- `CAMERA`
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE`

Configure these in `app.json` under `expo.ios.infoPlist` and `expo.android.permissions`.

---

## How to Run

```bash
cd ~/Desktop/trailmate
npx expo start          # Scan QR with Expo Go on phone
npx expo start --ios    # iOS Simulator (Mac only)
npx expo run:android    # Android emulator
```

## How to Build for App Store (later)

```bash
npm install -g eas-cli
eas login
eas build:configure
eas build --platform ios --profile preview    # Test build
eas build --platform ios --profile production # App Store build
eas submit --platform ios                     # Submit to App Store
```

---

## What NOT to do

- Do not build a backend yet — Phase 1 is 100% local/offline
- Do not add social features yet
- Do not integrate payments (booking is always via deep-link to external site)
- Do not use Redux — Zustand only
- Do not skip TypeScript types — every function and component must be typed
- Do not hardcode API keys — use environment variables via `expo-constants`

---

## Start Here

When starting a new Claude Code session on this project, begin with:

1. Read `CLAUDE.md` (this file) fully
2. Run `npx expo start` and confirm the app launches
3. The highest priority task is **TrackingScreen** — get the map showing with live GPS position first
4. Then wire up Start/Stop trip and drawing the route polyline
5. Then add the speed/distance HUD

Good luck — build something epic.

#!/bin/bash
# TrailMate — Road Trip & Overlanding App
# Run this once on your laptop to scaffold the full project.
# Usage: bash setup.sh

set -e

APP_NAME="trailmate"
DESKTOP="$HOME/Desktop"
DEST="$DESKTOP/$APP_NAME"

echo ""
echo "============================================"
echo "  TrailMate Setup Script"
echo "  Road Trip & Overlanding App"
echo "============================================"
echo ""

# --- Prereq checks ---
command -v node >/dev/null 2>&1 || { echo "ERROR: Node.js not found. Install from https://nodejs.org"; exit 1; }
command -v npm >/dev/null 2>&1  || { echo "ERROR: npm not found."; exit 1; }
command -v git >/dev/null 2>&1  || { echo "ERROR: git not found."; exit 1; }

NODE_VERSION=$(node -v | cut -d. -f1 | tr -d 'v')
if [ "$NODE_VERSION" -lt 18 ]; then
  echo "ERROR: Node.js 18+ required. Current: $(node -v)"
  exit 1
fi

echo "Node: $(node -v)  npm: $(npm -v)  git: $(git --version)"
echo ""

# --- Create project ---
if [ -d "$DEST" ]; then
  echo "Directory $DEST already exists. Skipping Expo init."
else
  echo "Creating Expo project at $DEST ..."
  npx create-expo-app@latest "$DEST" --template blank-typescript
fi

cd "$DEST"

echo ""
echo "Installing dependencies..."

# Navigation
npx expo install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack
npx expo install react-native-screens react-native-safe-area-context

# Maps & Location
npx expo install react-native-maps
npx expo install expo-location
npx expo install expo-sensors          # Inclinometer (accelerometer/gyroscope)

# Media
npx expo install expo-camera
npx expo install expo-media-library    # Save trip photos to gallery
npx expo install expo-file-system

# Storage & State
npx expo install @react-native-async-storage/async-storage
npx expo install expo-sqlite           # Local trip history DB
npm install zustand                    # State management

# UI & Utils
npm install react-native-paper         # Material UI components
npx expo install expo-status-bar
npx expo install expo-splash-screen
npm install date-fns                   # Date formatting
npm install @turf/turf                 # Geospatial calculations (distance, elevation, etc.)

echo ""
echo "Scaffolding folder structure..."

mkdir -p src/screens
mkdir -p src/components
mkdir -p src/store
mkdir -p src/hooks
mkdir -p src/utils
mkdir -p src/types
mkdir -p src/constants
mkdir -p assets/icons

# --- Create placeholder files so Claude Code knows the intended structure ---

cat > src/types/index.ts << 'EOF'
export interface TripPoint {
  latitude: number;
  longitude: number;
  altitude: number | null;
  speed: number | null;          // m/s
  timestamp: number;             // Unix ms
  accuracy: number | null;
}

export interface Trip {
  id: string;
  name: string;
  startedAt: number;
  endedAt: number | null;
  points: TripPoint[];
  totalDistanceKm: number;
  maxSpeedKmh: number;
  avgSpeedKmh: number;
  photos: TripPhoto[];
  notes: string;
}

export interface TripPhoto {
  id: string;
  uri: string;
  latitude: number;
  longitude: number;
  timestamp: number;
}

export interface VehicleProfile {
  id: string;
  name: string;
  make: string;
  model: string;
  year: number;
  fuelTankLitres: number;
  fuelEconomyTarmac: number;     // L/100km
  fuelEconomyGravel: number;
  fuelEconomySand: number;
  fuelEconomyMud: number;
  tyreSize: string;              // e.g. "265/70R17"
  tyrePressureTarmac: number;    // PSI
  tyrePressureGravel: number;
  tyrePressureSand: number;
  tyrePressureMud: number;
  tyrePressureRock: number;
}

export type TerrainType = 'tarmac' | 'gravel' | 'sand' | 'mud' | 'rock';

export interface Waypoint {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  type: 'fuel' | 'camp' | 'accommodation' | 'viewpoint' | 'mechanic' | 'water' | 'custom';
  notes?: string;
  bookingUrl?: string;           // Deep-link to Booking.com / Airbnb etc.
}

export interface PlannedTrip {
  id: string;
  name: string;
  startDate: string;
  endDate: string;
  waypoints: Waypoint[];
  notes: string;
  estimatedDistanceKm: number;
}
EOF

cat > src/constants/index.ts << 'EOF'
export const TERRAIN_LABELS: Record<string, string> = {
  tarmac: 'Tarmac / Highway',
  gravel: 'Gravel Road',
  sand: 'Sand / Beach',
  mud: 'Mud / Wet Track',
  rock: 'Rocky / Technical',
};

export const TYRE_PRESSURE_GUIDE = {
  tarmac: { min: 32, max: 38, note: 'Normal road pressure' },
  gravel: { min: 26, max: 30, note: 'Slightly lower for comfort' },
  sand:   { min: 16, max: 20, note: 'Significantly lower for floatation' },
  mud:    { min: 20, max: 24, note: 'Lower for grip' },
  rock:   { min: 18, max: 22, note: 'Lower for traction and sidewall flex' },
};

export const RECOVERY_GEAR_CHECKLIST = [
  'Hi-lift jack',
  'Snatch strap',
  'Shackles (x4)',
  'Kinetic recovery rope',
  'Traction boards (x2)',
  'Shovel',
  'Air compressor / ARB TRED',
  'Tree trunk protector',
  'Gloves',
  'First aid kit',
  'Fire extinguisher',
  'Spare tyre (full size)',
  'Tyre repair kit',
  'Jumper cables / jump pack',
  'Tow rope',
  'Basic tools',
];

export const COLORS = {
  primary: '#E85D04',     // Burnt orange — rugged, outdoorsy
  secondary: '#1A1A2E',   // Dark navy
  surface: '#16213E',
  card: '#0F3460',
  text: '#E0E0E0',
  textMuted: '#9E9E9E',
  success: '#4CAF50',
  warning: '#FF9800',
  danger: '#F44336',
  mapTrack: '#E85D04',
};
EOF

cat > src/store/tripStore.ts << 'EOF'
import { create } from 'zustand';
import { Trip, TripPoint } from '../types';

interface TripStore {
  activeTrip: Trip | null;
  tripHistory: Trip[];
  isTracking: boolean;

  startTrip: (name: string) => void;
  stopTrip: () => void;
  addPoint: (point: TripPoint) => void;
  loadHistory: () => Promise<void>;
}

export const useTripStore = create<TripStore>((set, get) => ({
  activeTrip: null,
  tripHistory: [],
  isTracking: false,

  startTrip: (name) => {
    const trip: Trip = {
      id: Date.now().toString(),
      name,
      startedAt: Date.now(),
      endedAt: null,
      points: [],
      totalDistanceKm: 0,
      maxSpeedKmh: 0,
      avgSpeedKmh: 0,
      photos: [],
      notes: '',
    };
    set({ activeTrip: trip, isTracking: true });
  },

  stopTrip: () => {
    const { activeTrip, tripHistory } = get();
    if (!activeTrip) return;
    const finished = { ...activeTrip, endedAt: Date.now() };
    set({ activeTrip: null, isTracking: false, tripHistory: [finished, ...tripHistory] });
    // TODO: persist to SQLite
  },

  addPoint: (point) => {
    const { activeTrip } = get();
    if (!activeTrip) return;
    const points = [...activeTrip.points, point];
    const speedKmh = point.speed ? point.speed * 3.6 : 0;
    set({
      activeTrip: {
        ...activeTrip,
        points,
        maxSpeedKmh: Math.max(activeTrip.maxSpeedKmh, speedKmh),
      },
    });
  },

  loadHistory: async () => {
    // TODO: load from SQLite
  },
}));
EOF

cat > src/screens/TrackingScreen.tsx << 'EOF'
// Live tracking screen — map + speed + stats HUD
// TODO: implement with expo-location + react-native-maps
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

export default function TrackingScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>Tracking Screen — Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  placeholder: { color: COLORS.text, fontSize: 18 },
});
EOF

cat > src/screens/PlanScreen.tsx << 'EOF'
// Trip planning screen — set waypoints, dates, estimate fuel
// TODO: implement
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

export default function PlanScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>Plan Screen — Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  placeholder: { color: COLORS.text, fontSize: 18 },
});
EOF

cat > src/screens/ToolsScreen.tsx << 'EOF'
// 4x4 tools — tyre pressure calc, fuel range, inclinometer, recovery checklist
// TODO: implement
import React from 'react';
import { View, Text, StyleSheet } from 'react_native';
import { COLORS } from '../constants';

export default function ToolsScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>4x4 Tools — Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  placeholder: { color: COLORS.text, fontSize: 18 },
});
EOF

cat > src/screens/HistoryScreen.tsx << 'EOF'
// Past trips list + individual trip playback
// TODO: implement
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

export default function HistoryScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>Trip History — Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  placeholder: { color: COLORS.text, fontSize: 18 },
});
EOF

cat > src/screens/ProfileScreen.tsx << 'EOF'
// Vehicle profile + gear checklists + settings
// TODO: implement
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

export default function ProfileScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.placeholder}>Profile & Vehicle — Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  placeholder: { color: COLORS.text, fontSize: 18 },
});
EOF

echo ""
echo "Setting up CLAUDE.md for Claude Code..."

cp "$(dirname "$0")/CLAUDE.md" "$DEST/CLAUDE.md" 2>/dev/null || echo "(CLAUDE.md not found alongside script — copy it manually from the repo)"

echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  Project location: $DEST"
echo ""
echo "  Next steps:"
echo "  1. cd ~/Desktop/trailmate"
echo "  2. Open in VS Code:  code ."
echo "  3. Start dev server: npx expo start"
echo "  4. Scan QR with Expo Go app on your phone"
echo "  5. Open Claude Code and start building!"
echo "============================================"
echo ""

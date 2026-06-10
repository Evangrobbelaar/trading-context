# TrailMate — Road Trip & Overlanding App
# Run in PowerShell: .\setup.ps1
# If you get a permissions error first run: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

$ErrorActionPreference = "Stop"

$APP_NAME = "trailmate"
$DESKTOP  = [Environment]::GetFolderPath("Desktop")
$DEST     = Join-Path $DESKTOP $APP_NAME

Write-Host ""
Write-Host "============================================"
Write-Host "  TrailMate Setup Script"
Write-Host "  Road Trip & Overlanding App"
Write-Host "============================================"
Write-Host ""

# --- Prereq checks ---
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Node.js not found. Install from https://nodejs.org" -ForegroundColor Red; exit 1
}
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: npm not found." -ForegroundColor Red; exit 1
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: git not found. Install from https://git-scm.com" -ForegroundColor Red; exit 1
}

$nodeVersion = (node -v) -replace 'v','' -split '\.' | Select-Object -First 1
if ([int]$nodeVersion -lt 18) {
    Write-Host "ERROR: Node.js 18+ required. Current: $(node -v)" -ForegroundColor Red; exit 1
}

Write-Host "Node: $(node -v)  npm: $(npm -v)" -ForegroundColor Green
Write-Host ""

# --- Create project ---
if (Test-Path $DEST) {
    Write-Host "Directory $DEST already exists. Skipping Expo init." -ForegroundColor Yellow
} else {
    Write-Host "Creating Expo project at $DEST ..."
    npx create-expo-app@latest $DEST --template blank-typescript
}

Set-Location $DEST

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Cyan

# Navigation
npx expo install @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack
npx expo install react-native-screens react-native-safe-area-context

# Maps & Location
npx expo install react-native-maps
npx expo install expo-location
npx expo install expo-sensors

# Media
npx expo install expo-camera
npx expo install expo-media-library
npx expo install expo-file-system

# Storage & State
npx expo install @react-native-async-storage/async-storage
npx expo install expo-sqlite
npm install zustand

# UI & Utils
npm install react-native-paper
npx expo install expo-status-bar
npx expo install expo-splash-screen
npm install date-fns
npm install @turf/turf

Write-Host ""
Write-Host "Scaffolding folder structure..." -ForegroundColor Cyan

$dirs = @(
    "src/screens",
    "src/components",
    "src/store",
    "src/hooks",
    "src/utils",
    "src/types",
    "src/constants",
    "assets/icons"
)
foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path (Join-Path $DEST $dir) | Out-Null
}

# --- Types ---
@'
export interface TripPoint {
  latitude: number;
  longitude: number;
  altitude: number | null;
  speed: number | null;
  timestamp: number;
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
  fuelEconomyTarmac: number;
  fuelEconomyGravel: number;
  fuelEconomySand: number;
  fuelEconomyMud: number;
  tyreSize: string;
  tyrePressureTarmac: number;
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
  bookingUrl?: string;
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
'@ | Set-Content (Join-Path $DEST "src/types/index.ts") -Encoding UTF8

# --- Constants ---
@'
export const TERRAIN_LABELS: Record<string, string> = {
  tarmac: "Tarmac / Highway",
  gravel: "Gravel Road",
  sand:   "Sand / Beach",
  mud:    "Mud / Wet Track",
  rock:   "Rocky / Technical",
};

export const TYRE_PRESSURE_GUIDE = {
  tarmac: { min: 32, max: 38, note: "Normal road pressure" },
  gravel: { min: 26, max: 30, note: "Slightly lower for comfort" },
  sand:   { min: 16, max: 20, note: "Significantly lower for floatation" },
  mud:    { min: 20, max: 24, note: "Lower for grip" },
  rock:   { min: 18, max: 22, note: "Lower for traction and sidewall flex" },
};

export const RECOVERY_GEAR_CHECKLIST = [
  "Hi-lift jack", "Snatch strap", "Shackles (x4)", "Kinetic recovery rope",
  "Traction boards (x2)", "Shovel", "Air compressor", "Tree trunk protector",
  "Gloves", "First aid kit", "Fire extinguisher", "Spare tyre (full size)",
  "Tyre repair kit", "Jumper cables / jump pack", "Tow rope", "Basic tools",
];

export const COLORS = {
  primary:   "#E85D04",
  secondary: "#1A1A2E",
  surface:   "#16213E",
  card:      "#0F3460",
  text:      "#E0E0E0",
  textMuted: "#9E9E9E",
  success:   "#4CAF50",
  warning:   "#FF9800",
  danger:    "#F44336",
  mapTrack:  "#E85D04",
};
'@ | Set-Content (Join-Path $DEST "src/constants/index.ts") -Encoding UTF8

# --- Zustand store ---
@'
import { create } from "zustand";
import { Trip, TripPoint } from "../types";

interface TripStore {
  activeTrip: Trip | null;
  tripHistory: Trip[];
  isTracking: boolean;
  startTrip: (name: string) => void;
  stopTrip: () => void;
  addPoint: (point: TripPoint) => void;
}

export const useTripStore = create<TripStore>((set, get) => ({
  activeTrip: null,
  tripHistory: [],
  isTracking: false,

  startTrip: (name) => {
    const trip: Trip = {
      id: Date.now().toString(), name,
      startedAt: Date.now(), endedAt: null,
      points: [], totalDistanceKm: 0,
      maxSpeedKmh: 0, avgSpeedKmh: 0,
      photos: [], notes: "",
    };
    set({ activeTrip: trip, isTracking: true });
  },

  stopTrip: () => {
    const { activeTrip, tripHistory } = get();
    if (!activeTrip) return;
    const finished = { ...activeTrip, endedAt: Date.now() };
    set({ activeTrip: null, isTracking: false, tripHistory: [finished, ...tripHistory] });
  },

  addPoint: (point) => {
    const { activeTrip } = get();
    if (!activeTrip) return;
    const points = [...activeTrip.points, point];
    const speedKmh = point.speed ? point.speed * 3.6 : 0;
    set({ activeTrip: { ...activeTrip, points, maxSpeedKmh: Math.max(activeTrip.maxSpeedKmh, speedKmh) } });
  },
}));
'@ | Set-Content (Join-Path $DEST "src/store/tripStore.ts") -Encoding UTF8

# --- Screen stubs ---
$screens = @("TrackingScreen","PlanScreen","ToolsScreen","HistoryScreen","ProfileScreen")
foreach ($screen in $screens) {
    @"
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS } from '../constants';

export default function ${screen}() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>${screen} - Coming Soon</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.secondary, justifyContent: 'center', alignItems: 'center' },
  text: { color: COLORS.text, fontSize: 18 },
});
"@ | Set-Content (Join-Path $DEST "src/screens/$screen.tsx") -Encoding UTF8
}

# --- Copy CLAUDE.md ---
$claudeMd = Join-Path $PSScriptRoot "CLAUDE.md"
if (Test-Path $claudeMd) {
    Copy-Item $claudeMd (Join-Path $DEST "CLAUDE.md")
    Write-Host "CLAUDE.md copied." -ForegroundColor Green
} else {
    Write-Host "Note: Copy CLAUDE.md from the repo into $DEST manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "  Project: $DEST"
Write-Host ""
Write-Host "  Next steps:"
Write-Host "  1. cd `"$DEST`""
Write-Host "  2. npx expo start"
Write-Host "  3. Scan QR with Expo Go on your phone"
Write-Host "  4. Open Claude Code and start building!"
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

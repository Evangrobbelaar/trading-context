# SA Touring Toolkit — How to Build the APK

## Option 1: EAS Build (Recommended — no local setup needed)

1. Create a free Expo account at https://expo.dev
2. Install EAS CLI:
   ```bash
   npm install -g eas-cli
   ```
3. Login:
   ```bash
   eas login
   ```
4. Inside the `sa-touring-app` folder, run:
   ```bash
   npm install
   eas build --platform android --profile preview
   ```
5. EAS will build the APK in the cloud (~10–15 minutes).
6. Download the `.apk` from the link provided in the terminal or from https://expo.dev/accounts/[your-account]/projects/sa-touring-toolkit/builds

## Option 2: Expo Go (Instant preview — no APK needed)

1. Install **Expo Go** from the Google Play Store on your Android device
2. Run on your computer:
   ```bash
   npm install
   npx expo start
   ```
3. Scan the QR code with Expo Go — the app runs instantly

## Option 3: GitHub Actions (automated)

1. Add your `EXPO_TOKEN` to GitHub repo Secrets (Settings → Secrets → Actions)
2. Push to `main` branch — the workflow in `.github/workflows/build-apk.yml` will trigger automatically
3. Monitor build at https://expo.dev and download the APK

---

## App Features

| Feature | Description |
|---------|-------------|
| 🗺️ Trip Planner | Create & save road trip itineraries with SA destination autocomplete |
| 🚙 4x4 Routes | 12 routes — Baviaanskloof, Sani Pass, Richtersveld, Kruger, Kgalagadi and more |
| ⛺ Campsites | 14 campsites with facilities, prices and direct booking links |
| 🌿 National Parks | 10 SANParks + KZN Wildlife parks with gates, fees and wildlife lists |
| 🏨 Accommodation | 15 booking platforms — SANParks, Lekkeslaap, Booking.com, Airbnb and more |
| 📍 Points of Interest | 13 must-see SA destinations with maps, hours and entry fees |
| 💡 Travel Tips | 100+ tips covering safety, health, wildlife, 4x4, camping, culture and photography |
| 🆘 Emergency | All SA emergency numbers, hospital directory, snakebite protocol |

## Tech Stack
- React Native (Expo SDK 50)
- React Navigation (Bottom Tabs + Native Stack)
- AsyncStorage (offline trip saving)
- expo-linking (URL and phone call handling)
- Ionicons (icon set)

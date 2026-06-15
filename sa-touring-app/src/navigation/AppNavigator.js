import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../theme';

import HomeScreen from '../screens/HomeScreen';
import RoutesScreen from '../screens/RoutesScreen';
import RouteDetailScreen from '../screens/RouteDetailScreen';
import CampsitesScreen from '../screens/CampsitesScreen';
import CampsiteDetailScreen from '../screens/CampsiteDetailScreen';
import ParksScreen from '../screens/ParksScreen';
import ParkDetailScreen from '../screens/ParkDetailScreen';
import AccommodationScreen from '../screens/AccommodationScreen';
import POIScreen from '../screens/POIScreen';
import EmergencyScreen from '../screens/EmergencyScreen';
import TripPlannerScreen from '../screens/TripPlannerScreen';
import TipsScreen from '../screens/TipsScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

const stackScreenOptions = {
  headerStyle: { backgroundColor: COLORS.surface },
  headerTintColor: COLORS.accent,
  headerTitleStyle: { color: COLORS.text, fontWeight: '700' },
  contentStyle: { backgroundColor: COLORS.background },
};

function RoutesStack() {
  return (
    <Stack.Navigator screenOptions={stackScreenOptions}>
      <Stack.Screen name="RoutesList" component={RoutesScreen} options={{ title: '4x4 Routes' }} />
      <Stack.Screen name="RouteDetail" component={RouteDetailScreen} options={{ title: 'Route Details' }} />
    </Stack.Navigator>
  );
}

function CampsitesStack() {
  return (
    <Stack.Navigator screenOptions={stackScreenOptions}>
      <Stack.Screen name="CampsitesList" component={CampsitesScreen} options={{ title: 'Campsites' }} />
      <Stack.Screen name="CampsiteDetail" component={CampsiteDetailScreen} options={{ title: 'Campsite' }} />
    </Stack.Navigator>
  );
}

function ParksStack() {
  return (
    <Stack.Navigator screenOptions={stackScreenOptions}>
      <Stack.Screen name="ParksList" component={ParksScreen} options={{ title: 'National Parks' }} />
      <Stack.Screen name="ParkDetail" component={ParkDetailScreen} options={{ title: 'Park Info' }} />
    </Stack.Navigator>
  );
}

function HomeStack() {
  return (
    <Stack.Navigator screenOptions={stackScreenOptions}>
      <Stack.Screen name="HomeMain" component={HomeScreen} options={{ headerShown: false }} />
      <Stack.Screen name="TripPlanner" component={TripPlannerScreen} options={{ title: 'Trip Planner' }} />
      <Stack.Screen name="Tips" component={TipsScreen} options={{ title: 'Travel Tips' }} />
      <Stack.Screen name="Accommodation" component={AccommodationScreen} options={{ title: 'Accommodation' }} />
      <Stack.Screen name="POI" component={POIScreen} options={{ title: 'Points of Interest' }} />
      <Stack.Screen name="Emergency" component={EmergencyScreen} options={{ title: '🆘 Emergency' }} />
    </Stack.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          const icons = {
            Home: focused ? 'home' : 'home-outline',
            Routes: focused ? 'navigate' : 'navigate-outline',
            Camps: focused ? 'bonfire' : 'bonfire-outline',
            Parks: focused ? 'leaf' : 'leaf-outline',
            SOS: focused ? 'alert-circle' : 'alert-circle-outline',
          };
          return <Ionicons name={icons[route.name] || 'ellipse'} size={size} color={color} />;
        },
        tabBarActiveTintColor: COLORS.accent,
        tabBarInactiveTintColor: COLORS.textSecondary,
        tabBarStyle: {
          backgroundColor: COLORS.surface,
          borderTopColor: COLORS.border,
          height: 60,
          paddingBottom: 8,
        },
        tabBarLabelStyle: { fontSize: 11, fontWeight: '600' },
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} />
      <Tab.Screen name="Routes" component={RoutesStack} />
      <Tab.Screen name="Camps" component={CampsitesStack} />
      <Tab.Screen name="Parks" component={ParksStack} />
      <Tab.Screen
        name="SOS"
        component={EmergencyScreen}
        options={{
          tabBarLabel: 'SOS',
          tabBarActiveTintColor: COLORS.danger,
          tabBarInactiveTintColor: COLORS.danger + '88',
        }}
      />
    </Tab.Navigator>
  );
}

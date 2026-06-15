import React from 'react';
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, StatusBar, ImageBackground,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS, SPACING, RADIUS } from '../theme';

const MENU_ITEMS = [
  { label: 'Trip Planner', icon: 'map', color: '#007A33', route: 'TripPlanner', subtitle: 'Plan your SA adventure' },
  { label: '4x4 Routes', icon: 'navigate', color: '#e67e22', route: null, tab: 'Routes', subtitle: '12 epic routes' },
  { label: 'Campsites', icon: 'bonfire', color: '#c0392b', route: null, tab: 'Camps', subtitle: '14 top campsites' },
  { label: 'National Parks', icon: 'leaf', color: '#27ae60', route: null, tab: 'Parks', subtitle: '10 parks covered' },
  { label: 'Accommodation', icon: 'bed', color: '#8e44ad', route: 'Accommodation', subtitle: '15 booking sites' },
  { label: 'Points of Interest', icon: 'location', color: '#2980b9', route: 'POI', subtitle: 'Must-see SA spots' },
  { label: 'Travel Tips', icon: 'bulb', color: '#f39c12', route: 'Tips', subtitle: 'Essential SA knowledge' },
  { label: '🆘 Emergency', icon: 'alert-circle', color: '#e74c3c', route: 'Emergency', subtitle: 'Numbers & protocols' },
];

const QUICK_FACTS = [
  { label: 'Capital', value: 'Pretoria / Cape Town / Bloemfontein' },
  { label: 'Currency', value: 'ZAR (Rand) — R1 ≈ $0.055' },
  { label: 'Drive on', value: 'LEFT side of road' },
  { label: 'Emergency', value: '112 (any network)' },
  { label: 'Voltage', value: '220V / Type M plug (3-round-pin)' },
  { label: 'Time zone', value: 'SAST — UTC+2 (no daylight saving)' },
];

export default function HomeScreen({ navigation }) {
  const handlePress = (item) => {
    if (item.tab) {
      navigation.getParent()?.navigate(item.tab);
    } else if (item.route) {
      navigation.navigate(item.route);
    }
  };

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.surface} />
      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.headerFlag}>🇿🇦</Text>
            <Text style={styles.headerTitle}>SA Touring Toolkit</Text>
            <Text style={styles.headerSubtitle}>Your all-in-one South Africa travel companion</Text>
          </View>
        </View>

        {/* Main Menu Grid */}
        <Text style={styles.sectionTitle}>Explore</Text>
        <View style={styles.grid}>
          {MENU_ITEMS.map((item) => (
            <TouchableOpacity
              key={item.label}
              style={styles.gridItem}
              onPress={() => handlePress(item)}
              activeOpacity={0.7}
            >
              <View style={[styles.iconWrap, { backgroundColor: item.color + '22' }]}>
                <Ionicons name={item.icon} size={28} color={item.color} />
              </View>
              <Text style={styles.gridLabel}>{item.label}</Text>
              <Text style={styles.gridSub}>{item.subtitle}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Quick Facts */}
        <Text style={styles.sectionTitle}>SA Quick Facts</Text>
        <View style={styles.factsCard}>
          {QUICK_FACTS.map((f) => (
            <View key={f.label} style={styles.factRow}>
              <Text style={styles.factLabel}>{f.label}</Text>
              <Text style={styles.factValue}>{f.value}</Text>
            </View>
          ))}
        </View>

        {/* SANParks Wild Card CTA */}
        <View style={styles.ctaCard}>
          <Ionicons name="card" size={24} color={COLORS.accent} />
          <View style={styles.ctaText}>
            <Text style={styles.ctaTitle}>Wild Card — Unlimited Parks Access</Text>
            <Text style={styles.ctaSub}>Annual pass for all 19 SANParks. Pays off after 3 visits.</Text>
          </View>
          <Ionicons name="chevron-forward" size={20} color={COLORS.accent} />
        </View>

        {/* SOS quick access */}
        <TouchableOpacity
          style={styles.sosButton}
          onPress={() => navigation.getParent()?.navigate('SOS')}
          activeOpacity={0.8}
        >
          <Ionicons name="alert-circle" size={22} color={COLORS.white} />
          <Text style={styles.sosText}>SOS — Emergency Numbers & Protocols</Text>
        </TouchableOpacity>

        <Text style={styles.footer}>
          Data is for guidance only. Always verify conditions and bookings before travel.{'\n'}
          Built for touring South Africa 🇿🇦
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  scroll: { paddingBottom: 32 },
  header: {
    backgroundColor: COLORS.surface,
    padding: SPACING.lg,
    paddingTop: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    marginBottom: SPACING.md,
  },
  headerFlag: { fontSize: 36, marginBottom: 4 },
  headerTitle: {
    fontSize: 26,
    fontWeight: '800',
    color: COLORS.accent,
    letterSpacing: 0.5,
  },
  headerSubtitle: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: COLORS.text,
    marginHorizontal: SPACING.md,
    marginBottom: SPACING.sm,
    marginTop: SPACING.md,
  },
  grid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    paddingHorizontal: SPACING.sm,
  },
  gridItem: {
    width: '48%',
    backgroundColor: COLORS.card,
    margin: '1%',
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  iconWrap: {
    width: 52,
    height: 52,
    borderRadius: RADIUS.md,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: SPACING.sm,
  },
  gridLabel: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.text,
    marginBottom: 2,
  },
  gridSub: {
    fontSize: 11,
    color: COLORS.textSecondary,
  },
  factsCard: {
    backgroundColor: COLORS.card,
    marginHorizontal: SPACING.md,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  factRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 7,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  factLabel: { fontSize: 13, color: COLORS.textSecondary, flex: 1 },
  factValue: { fontSize: 13, color: COLORS.text, fontWeight: '600', flex: 2, textAlign: 'right' },
  ctaCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.primary + '22',
    marginHorizontal: SPACING.md,
    marginTop: SPACING.md,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.primary,
  },
  ctaText: { flex: 1, marginLeft: SPACING.sm },
  ctaTitle: { fontSize: 13, fontWeight: '700', color: COLORS.accent },
  ctaSub: { fontSize: 11, color: COLORS.textSecondary, marginTop: 2 },
  sosButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.danger,
    marginHorizontal: SPACING.md,
    marginTop: SPACING.md,
    borderRadius: RADIUS.md,
    paddingVertical: 14,
    gap: 8,
  },
  sosText: { color: COLORS.white, fontWeight: '700', fontSize: 15 },
  footer: {
    textAlign: 'center',
    fontSize: 11,
    color: COLORS.textMuted,
    marginTop: SPACING.lg,
    paddingHorizontal: SPACING.lg,
    lineHeight: 16,
  },
});

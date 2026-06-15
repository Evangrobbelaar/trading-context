import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { FACILITY_ICONS } from '../data/campsites';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

function openUrl(url) {
  if (!url) return;
  Linking.canOpenURL(url).then((can) => {
    if (can) Linking.openURL(url);
    else Alert.alert('Cannot open URL');
  });
}

function callPhone(number) {
  Linking.openURL(`tel:${number}`);
}

function openMaps(coords, name) {
  Linking.openURL(`https://maps.google.com/?q=${coords.lat},${coords.lng}(${encodeURIComponent(name)})`);
}

export default function CampsiteDetailScreen({ route }) {
  const camp = route.params.campsite;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.name}>{camp.name}</Text>
        <Text style={styles.park}>{camp.park}</Text>
        <View style={styles.locationRow}>
          <Ionicons name="location" size={14} color={COLORS.textSecondary} />
          <Text style={styles.region}>{camp.region}</Text>
          <View style={styles.typeBadge}>
            <Text style={styles.typeText}>{camp.type}</Text>
          </View>
        </View>
      </View>

      {/* Price & Capacity */}
      <View style={styles.statsRow}>
        <View style={styles.statItem}>
          <Ionicons name="pricetag" size={20} color={COLORS.accent} />
          <Text style={styles.statLabel}>Price Range</Text>
          <Text style={styles.statValue}>{camp.priceRange}</Text>
        </View>
        <View style={styles.statItem}>
          <Ionicons name="people" size={20} color={COLORS.accent} />
          <Text style={styles.statLabel}>Capacity</Text>
          <Text style={styles.statValue}>{camp.capacity}</Text>
        </View>
        <View style={styles.statItem}>
          <Ionicons name="star" size={20} color={COLORS.accent} />
          <Text style={styles.statLabel}>Rating</Text>
          <Text style={styles.statValue}>{camp.rating}/5</Text>
        </View>
      </View>

      {/* Description */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <Text style={styles.description}>{camp.description}</Text>
      </View>

      {/* Facilities */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Facilities</Text>
        <View style={styles.facilityGrid}>
          {camp.facilities.map((f) => (
            <View key={f} style={styles.facilityItem}>
              <Ionicons
                name={(FACILITY_ICONS[f] || 'checkmark-circle')}
                size={20}
                color={COLORS.success}
              />
              <Text style={styles.facilityText}>{f}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Tags */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Tags</Text>
        <View style={styles.tags}>
          {camp.tags.map((t) => (
            <TagBadge key={t} label={t} />
          ))}
        </View>
      </View>

      {/* Actions */}
      <View style={styles.actions}>
        {camp.bookingUrl && (
          <TouchableOpacity style={styles.primaryBtn} onPress={() => openUrl(camp.bookingUrl)}>
            <Ionicons name="calendar" size={20} color={COLORS.black} />
            <Text style={styles.primaryBtnText}>Book This Campsite</Text>
          </TouchableOpacity>
        )}

        <View style={styles.secondaryActions}>
          {camp.coordinates && (
            <TouchableOpacity
              style={styles.secondaryBtn}
              onPress={() => openMaps(camp.coordinates, camp.name)}
            >
              <Ionicons name="navigate" size={18} color={COLORS.accent} />
              <Text style={styles.secondaryBtnText}>Open in Maps</Text>
            </TouchableOpacity>
          )}
          {camp.phone && (
            <TouchableOpacity
              style={styles.secondaryBtn}
              onPress={() => callPhone(camp.phone)}
            >
              <Ionicons name="call" size={18} color={COLORS.accent} />
              <Text style={styles.secondaryBtnText}>Call Camp</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      {camp.coordinates && (
        <View style={styles.coordBlock}>
          <Text style={styles.coordLabel}>GPS Coordinates</Text>
          <Text style={styles.coordText}>
            {camp.coordinates.lat.toFixed(4)}°S, {camp.coordinates.lng.toFixed(4)}°E
          </Text>
        </View>
      )}

      <Text style={styles.disclaimer}>
        Prices and facilities subject to change. Always confirm directly with the camp before visiting.
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  content: { padding: SPACING.md, paddingBottom: 40 },
  header: { marginBottom: SPACING.md },
  name: { fontSize: 22, fontWeight: '800', color: COLORS.text },
  park: { fontSize: 14, color: COLORS.primary, fontWeight: '600', marginTop: 4 },
  locationRow: { flexDirection: 'row', alignItems: 'center', marginTop: 6, gap: 6 },
  region: { fontSize: 13, color: COLORS.textSecondary, flex: 1 },
  typeBadge: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.full,
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  typeText: { fontSize: 11, color: COLORS.textSecondary },
  statsRow: {
    flexDirection: 'row',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.md,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
    padding: SPACING.sm,
    borderRightWidth: 1,
    borderRightColor: COLORS.border,
  },
  statLabel: { fontSize: 10, color: COLORS.textSecondary, marginTop: 4, textTransform: 'uppercase' },
  statValue: { fontSize: 12, color: COLORS.text, fontWeight: '600', marginTop: 2, textAlign: 'center' },
  section: { marginBottom: SPACING.md },
  sectionTitle: { fontSize: 13, fontWeight: '700', color: COLORS.accent, marginBottom: 8, textTransform: 'uppercase' },
  description: { fontSize: 14, color: COLORS.text, lineHeight: 22, backgroundColor: COLORS.card, borderRadius: RADIUS.md, padding: SPACING.md, borderWidth: 1, borderColor: COLORS.border },
  facilityGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  facilityItem: { flexDirection: 'row', alignItems: 'center', gap: 6, minWidth: '45%' },
  facilityText: { fontSize: 13, color: COLORS.text },
  tags: { flexDirection: 'row', flexWrap: 'wrap' },
  actions: { marginBottom: SPACING.md },
  primaryBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.accent,
    borderRadius: RADIUS.md,
    paddingVertical: 14,
    marginBottom: SPACING.sm,
    gap: 8,
  },
  primaryBtnText: { fontSize: 16, fontWeight: '700', color: COLORS.black },
  secondaryActions: { flexDirection: 'row', gap: 8 },
  secondaryBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    paddingVertical: 12,
    borderWidth: 1,
    borderColor: COLORS.accent,
    gap: 6,
  },
  secondaryBtnText: { fontSize: 13, color: COLORS.accent, fontWeight: '600' },
  coordBlock: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  coordLabel: { fontSize: 11, color: COLORS.textSecondary, textTransform: 'uppercase', marginBottom: 4 },
  coordText: { fontSize: 14, color: COLORS.text, fontWeight: '600', fontFamily: 'monospace' },
  disclaimer: { fontSize: 11, color: COLORS.textMuted, textAlign: 'center', lineHeight: 16 },
});

import React from 'react';
import {
  View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking, Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { DIFFICULTY_COLORS } from '../data/routes';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

function openUrl(url) {
  Linking.canOpenURL(url).then((can) => {
    if (can) Linking.openURL(url);
    else Alert.alert('Cannot open URL', url);
  });
}

function openMaps(lat, lng, label) {
  const url = `https://maps.google.com/?q=${lat},${lng}(${encodeURIComponent(label)})`;
  Linking.openURL(url);
}

export default function RouteDetailScreen({ route: navRoute }) {
  const route = navRoute.params.route;
  const diffColor = DIFFICULTY_COLORS[route.difficulty];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Title block */}
      <View style={styles.titleBlock}>
        <Text style={styles.title}>{route.name}</Text>
        <View style={styles.titleMeta}>
          <View style={[styles.diffBadge, { backgroundColor: diffColor + '33' }]}>
            <Text style={[styles.diffText, { color: diffColor }]}>{route.difficulty}</Text>
          </View>
          <Text style={styles.region}>
            <Ionicons name="location" size={13} color={COLORS.textSecondary} /> {route.region}
          </Text>
        </View>
      </View>

      {/* Stats */}
      <View style={styles.statsRow}>
        <StatItem icon="resize" label="Distance" value={route.distance} />
        <StatItem icon="time" label="Duration" value={route.duration} />
        <StatItem icon="sunny" label="Best Season" value={route.bestSeason} />
      </View>

      {/* Description */}
      <SectionCard title="About this Route">
        <Text style={styles.description}>{route.description}</Text>
      </SectionCard>

      {/* Highlights */}
      <SectionCard title="Highlights">
        {route.highlights.map((h, i) => (
          <View key={i} style={styles.bulletRow}>
            <Ionicons name="star" size={14} color={COLORS.accent} style={styles.bulletIcon} />
            <Text style={styles.bulletText}>{h}</Text>
          </View>
        ))}
      </SectionCard>

      {/* Terrain */}
      <SectionCard title="Terrain">
        <View style={styles.tags}>
          {route.terrain.map((t) => (
            <TagBadge key={t} label={t} color={COLORS.warning + '22'} textColor={COLORS.warning} />
          ))}
        </View>
      </SectionCard>

      {/* Warnings */}
      {route.warnings && route.warnings.length > 0 && (
        <SectionCard title="⚠️ Important Warnings">
          {route.warnings.map((w, i) => (
            <View key={i} style={styles.bulletRow}>
              <Ionicons name="warning" size={14} color={COLORS.danger} style={styles.bulletIcon} />
              <Text style={[styles.bulletText, { color: COLORS.text }]}>{w}</Text>
            </View>
          ))}
        </SectionCard>
      )}

      {/* Fuel Stops */}
      <SectionCard title="Fuel Stops">
        <View style={styles.tags}>
          {route.fuelStops.map((f) => (
            <TagBadge key={f} label={f} color={COLORS.info + '22'} textColor={COLORS.info} />
          ))}
        </View>
      </SectionCard>

      {/* GPS & Navigation */}
      <SectionCard title="GPS Start Point">
        <TouchableOpacity
          style={styles.gpsBtn}
          onPress={() => openMaps(route.gpsStart.lat, route.gpsStart.lng, route.gpsStart.label)}
        >
          <Ionicons name="navigate" size={18} color={COLORS.accent} />
          <View style={{ flex: 1, marginLeft: 10 }}>
            <Text style={styles.gpsBtnLabel}>{route.gpsStart.label}</Text>
            <Text style={styles.gpsCoords}>
              {route.gpsStart.lat.toFixed(4)}, {route.gpsStart.lng.toFixed(4)}
            </Text>
          </View>
          <Text style={styles.openMaps}>Open Maps →</Text>
        </TouchableOpacity>
      </SectionCard>

      {/* Permit */}
      {route.permitRequired && (
        <View style={styles.permitCard}>
          <Ionicons name="document-text" size={20} color={COLORS.accent} />
          <View style={{ flex: 1, marginLeft: 10 }}>
            <Text style={styles.permitTitle}>Permit Required</Text>
            <Text style={styles.permitSub}>A valid permit must be obtained before entering this route.</Text>
          </View>
          {route.permitUrl && (
            <TouchableOpacity onPress={() => openUrl(route.permitUrl)}>
              <Text style={styles.permitLink}>Get Permit →</Text>
            </TouchableOpacity>
          )}
        </View>
      )}

      {/* Tags */}
      <SectionCard title="Tags">
        <View style={styles.tags}>
          {route.tags.map((t) => (
            <TagBadge key={t} label={t} />
          ))}
        </View>
      </SectionCard>

      {/* Booking CTA */}
      {route.bookingUrl && (
        <TouchableOpacity style={styles.bookBtn} onPress={() => openUrl(route.bookingUrl)}>
          <Ionicons name="calendar" size={20} color={COLORS.black} />
          <Text style={styles.bookBtnText}>Book / Reserve Online</Text>
        </TouchableOpacity>
      )}

      <Text style={styles.disclaimer}>
        Always check current road conditions, weather and permits before departure. Information is for guidance only.
      </Text>
    </ScrollView>
  );
}

function SectionCard({ title, children }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionBody}>{children}</View>
    </View>
  );
}

function StatItem({ icon, label, value }) {
  return (
    <View style={styles.statItem}>
      <Ionicons name={icon} size={18} color={COLORS.accent} />
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={styles.statValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  content: { padding: SPACING.md, paddingBottom: 40 },
  titleBlock: { marginBottom: SPACING.md },
  title: { fontSize: 22, fontWeight: '800', color: COLORS.text, lineHeight: 28 },
  titleMeta: { flexDirection: 'row', alignItems: 'center', marginTop: 8, gap: 10 },
  diffBadge: { borderRadius: RADIUS.full, paddingHorizontal: 10, paddingVertical: 4 },
  diffText: { fontSize: 12, fontWeight: '700' },
  region: { fontSize: 13, color: COLORS.textSecondary },
  statsRow: {
    flexDirection: 'row',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.md,
    overflow: 'hidden',
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
  sectionTitle: { fontSize: 14, fontWeight: '700', color: COLORS.accent, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  sectionBody: { backgroundColor: COLORS.card, borderRadius: RADIUS.md, padding: SPACING.md, borderWidth: 1, borderColor: COLORS.border },
  description: { fontSize: 14, color: COLORS.text, lineHeight: 22 },
  bulletRow: { flexDirection: 'row', alignItems: 'flex-start', marginBottom: 6 },
  bulletIcon: { marginRight: 8, marginTop: 1 },
  bulletText: { fontSize: 13, color: COLORS.textSecondary, flex: 1, lineHeight: 19 },
  tags: { flexDirection: 'row', flexWrap: 'wrap' },
  gpsBtn: { flexDirection: 'row', alignItems: 'center' },
  gpsBtnLabel: { fontSize: 14, fontWeight: '600', color: COLORS.text },
  gpsCoords: { fontSize: 11, color: COLORS.textSecondary, marginTop: 2 },
  openMaps: { fontSize: 12, color: COLORS.accent, fontWeight: '600' },
  permitCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.accent + '15',
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.accent + '44',
  },
  permitTitle: { fontSize: 14, fontWeight: '700', color: COLORS.accent },
  permitSub: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  permitLink: { fontSize: 12, color: COLORS.accent, fontWeight: '700' },
  bookBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.accent,
    borderRadius: RADIUS.md,
    paddingVertical: 14,
    marginBottom: SPACING.md,
    gap: 8,
  },
  bookBtnText: { fontSize: 16, fontWeight: '700', color: COLORS.black },
  disclaimer: { fontSize: 11, color: COLORS.textMuted, textAlign: 'center', lineHeight: 16 },
});

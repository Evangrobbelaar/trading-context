import React from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity, Linking } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

function openUrl(url) {
  Linking.openURL(url);
}

function openMaps(gps, name) {
  Linking.openURL(`https://maps.google.com/?q=${gps.lat},${gps.lng}(${encodeURIComponent(name)})`);
}

function callPhone(number) {
  Linking.openURL(`tel:${number}`);
}

export default function ParkDetailScreen({ route }) {
  const park = route.params.park;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.name}>{park.name}</Text>
        <View style={styles.headerMeta}>
          <Text style={styles.type}>{park.type}</Text>
          <Text style={styles.bullet}>·</Text>
          <Text style={styles.region}>{park.region}</Text>
        </View>
        {park.malariaRisk && (
          <View style={styles.malariaBanner}>
            <Ionicons name="warning" size={16} color={COLORS.white} />
            <Text style={styles.malariaText}>⚠️ Malaria Zone — take prophylactics before visiting</Text>
          </View>
        )}
      </View>

      {/* Stats row */}
      <View style={styles.statsRow}>
        <StatBox icon="resize" label="Size" value={park.size} />
        <StatBox icon="calendar" label="Established" value={String(park.established)} />
        <StatBox icon="shield-checkmark" label="Malaria" value={park.malariaRisk ? 'Yes ⚠️' : 'No ✓'} valueColor={park.malariaRisk ? COLORS.danger : COLORS.success} />
      </View>

      {/* About */}
      <Section title="About">
        <Text style={styles.description}>{park.description}</Text>
      </Section>

      {/* Wildlife */}
      <Section title="Key Wildlife">
        <View style={styles.tags}>
          {park.wildlife.map((w) => (
            <TagBadge key={w} label={w} color={COLORS.success + '22'} textColor={COLORS.success} />
          ))}
        </View>
      </Section>

      {/* Activities */}
      <Section title="Activities">
        <View style={styles.tags}>
          {park.activities.map((a) => (
            <TagBadge key={a} label={a} color={COLORS.info + '22'} textColor={COLORS.info} />
          ))}
        </View>
      </Section>

      {/* Gates */}
      <Section title="Park Gates & Hours">
        {park.gates.map((g, i) => (
          <View key={i} style={styles.gateRow}>
            <Ionicons name="enter" size={14} color={COLORS.accent} />
            <View style={{ flex: 1, marginLeft: 8 }}>
              <Text style={styles.gateName}>{g.name}</Text>
              <Text style={styles.gateHours}>{g.hours}</Text>
            </View>
          </View>
        ))}
      </Section>

      {/* Fees */}
      <Section title="Entry Fees">
        <Text style={styles.fees}>{park.fees}</Text>
        <Text style={styles.feesNote}>Wild Card holders: free entry to all SANParks</Text>
      </Section>

      {/* Tags */}
      <Section title="Tags">
        <View style={styles.tags}>
          {park.tags.map((t) => (
            <TagBadge key={t} label={t} />
          ))}
        </View>
      </Section>

      {/* Action buttons */}
      <View style={styles.actions}>
        <TouchableOpacity style={styles.primaryBtn} onPress={() => openUrl(park.bookingUrl)}>
          <Ionicons name="calendar" size={20} color={COLORS.black} />
          <Text style={styles.primaryBtnText}>Book Accommodation</Text>
        </TouchableOpacity>

        <View style={styles.secondaryRow}>
          <TouchableOpacity style={styles.secondaryBtn} onPress={() => openMaps(park.gps, park.name)}>
            <Ionicons name="navigate" size={18} color={COLORS.accent} />
            <Text style={styles.secondaryBtnText}>Open in Maps</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.secondaryBtn} onPress={() => openUrl(park.websiteUrl)}>
            <Ionicons name="globe" size={18} color={COLORS.accent} />
            <Text style={styles.secondaryBtnText}>Website</Text>
          </TouchableOpacity>
          {park.phone && (
            <TouchableOpacity style={styles.secondaryBtn} onPress={() => callPhone(park.phone)}>
              <Ionicons name="call" size={18} color={COLORS.accent} />
              <Text style={styles.secondaryBtnText}>Call</Text>
            </TouchableOpacity>
          )}
        </View>
      </View>

      <Text style={styles.disclaimer}>
        Entry fees and hours subject to change. Check sanparks.org or kznwildlife.com for latest information.
      </Text>
    </ScrollView>
  );
}

function StatBox({ icon, label, value, valueColor }) {
  return (
    <View style={styles.statBox}>
      <Ionicons name={icon} size={18} color={COLORS.accent} />
      <Text style={styles.statLabel}>{label}</Text>
      <Text style={[styles.statValue, valueColor && { color: valueColor }]}>{value}</Text>
    </View>
  );
}

function Section({ title, children }) {
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionBody}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  content: { padding: SPACING.md, paddingBottom: 40 },
  header: { marginBottom: SPACING.md },
  name: { fontSize: 22, fontWeight: '800', color: COLORS.text, lineHeight: 28 },
  headerMeta: { flexDirection: 'row', alignItems: 'center', marginTop: 6, gap: 6 },
  type: { fontSize: 13, color: COLORS.primary, fontWeight: '600' },
  bullet: { color: COLORS.textMuted },
  region: { fontSize: 13, color: COLORS.textSecondary },
  malariaBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.danger,
    borderRadius: RADIUS.sm,
    padding: SPACING.sm,
    marginTop: SPACING.sm,
    gap: 6,
  },
  malariaText: { color: COLORS.white, fontSize: 12, fontWeight: '600', flex: 1 },
  statsRow: {
    flexDirection: 'row',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.md,
  },
  statBox: {
    flex: 1,
    alignItems: 'center',
    padding: SPACING.sm,
    borderRightWidth: 1,
    borderRightColor: COLORS.border,
  },
  statLabel: { fontSize: 10, color: COLORS.textSecondary, marginTop: 4, textTransform: 'uppercase' },
  statValue: { fontSize: 12, color: COLORS.text, fontWeight: '700', marginTop: 2, textAlign: 'center' },
  section: { marginBottom: SPACING.md },
  sectionTitle: { fontSize: 13, fontWeight: '700', color: COLORS.accent, marginBottom: 8, textTransform: 'uppercase', letterSpacing: 0.5 },
  sectionBody: { backgroundColor: COLORS.card, borderRadius: RADIUS.md, padding: SPACING.md, borderWidth: 1, borderColor: COLORS.border },
  description: { fontSize: 14, color: COLORS.text, lineHeight: 22 },
  tags: { flexDirection: 'row', flexWrap: 'wrap' },
  gateRow: { flexDirection: 'row', alignItems: 'flex-start', paddingVertical: 6, borderBottomWidth: 1, borderBottomColor: COLORS.border },
  gateName: { fontSize: 13, color: COLORS.text, fontWeight: '600' },
  gateHours: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  fees: { fontSize: 14, color: COLORS.text, fontWeight: '600', marginBottom: 4 },
  feesNote: { fontSize: 12, color: COLORS.primary, fontStyle: 'italic' },
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
  secondaryRow: { flexDirection: 'row', gap: 8 },
  secondaryBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    paddingVertical: 10,
    borderWidth: 1,
    borderColor: COLORS.accent,
    gap: 4,
  },
  secondaryBtnText: { fontSize: 12, color: COLORS.accent, fontWeight: '600' },
  disclaimer: { fontSize: 11, color: COLORS.textMuted, textAlign: 'center', lineHeight: 16 },
});

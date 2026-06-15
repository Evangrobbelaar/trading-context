import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet, Linking, Alert, ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { EMERGENCY_CONTACTS, SNAKE_BITE_PROTOCOL, EMERGENCY_CATEGORIES } from '../data/emergency';
import { COLORS, SPACING, RADIUS } from '../theme';

function callNumber(number) {
  const cleaned = number.replace(/[^0-9+]/g, '');
  Linking.openURL(`tel:${cleaned}`);
}

export default function EmergencyScreen() {
  const [category, setCategory] = useState('All');
  const [showSnake, setShowSnake] = useState(false);

  const filtered = EMERGENCY_CONTACTS.filter(
    (e) => category === 'All' || e.category === category,
  );
  const important = filtered.filter((e) => e.important);
  const rest = filtered.filter((e) => !e.important);
  const sorted = [...important, ...rest];

  const renderContact = ({ item }) => (
    <TouchableOpacity
      style={[styles.card, item.important && styles.cardImportant]}
      onPress={() => callNumber(item.number)}
      activeOpacity={0.75}
    >
      <View style={[styles.iconCircle, { backgroundColor: item.color + '22' }]}>
        <Ionicons name={item.icon} size={22} color={item.color} />
      </View>
      <View style={styles.cardInfo}>
        <Text style={styles.contactName}>{item.name}</Text>
        <Text style={styles.contactNumber}>{item.number}</Text>
        <Text style={styles.contactDesc}>{item.description}</Text>
        <Text style={styles.categoryLabel}>{item.category}</Text>
      </View>
      <View style={styles.callBtn}>
        <Ionicons name="call" size={22} color={COLORS.success} />
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['top', 'bottom']}>
      {/* SOS Header */}
      <View style={styles.sosHeader}>
        <Ionicons name="alert-circle" size={28} color={COLORS.danger} />
        <View style={{ flex: 1, marginLeft: 10 }}>
          <Text style={styles.sosTitle}>Emergency Contacts</Text>
          <Text style={styles.sosSub}>Tap any card to call. Works even with no airtime on 112.</Text>
        </View>
      </View>

      {/* 112 Big Button */}
      <TouchableOpacity style={styles.bigSosBtn} onPress={() => callNumber('112')}>
        <Ionicons name="call" size={24} color={COLORS.white} />
        <Text style={styles.bigSosText}>CALL 112 — NATIONAL EMERGENCY</Text>
        <Text style={styles.bigSosSub}>Works on any network, even without credit</Text>
      </TouchableOpacity>

      {/* Category filters */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
        <View style={styles.filters}>
          {EMERGENCY_CATEGORIES.map((c) => (
            <TouchableOpacity
              key={c}
              style={[styles.filterBtn, category === c && styles.filterBtnActive]}
              onPress={() => setCategory(c)}
            >
              <Text style={[styles.filterText, category === c && styles.filterTextActive]}>{c}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      <FlatList
        data={sorted}
        keyExtractor={(item) => item.id}
        renderItem={renderContact}
        contentContainerStyle={styles.list}
        ListFooterComponent={
          <View>
            {/* Snake Bite Protocol */}
            <TouchableOpacity
              style={styles.protocolHeader}
              onPress={() => setShowSnake(!showSnake)}
            >
              <Ionicons name="bug" size={20} color={COLORS.warning} />
              <Text style={styles.protocolTitle}>Snakebite Emergency Protocol</Text>
              <Ionicons name={showSnake ? 'chevron-up' : 'chevron-down'} size={18} color={COLORS.textSecondary} />
            </TouchableOpacity>
            {showSnake && (
              <View style={styles.protocolBody}>
                {SNAKE_BITE_PROTOCOL.map((step, i) => (
                  <View key={i} style={styles.protocolStep}>
                    <View style={styles.stepNum}>
                      <Text style={styles.stepNumText}>{i + 1}</Text>
                    </View>
                    <Text style={styles.stepText}>{step}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  sosHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.danger + '18',
    padding: SPACING.md,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.danger + '44',
  },
  sosTitle: { fontSize: 18, fontWeight: '800', color: COLORS.danger },
  sosSub: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  bigSosBtn: {
    backgroundColor: COLORS.danger,
    margin: SPACING.md,
    borderRadius: RADIUS.md,
    paddingVertical: 16,
    alignItems: 'center',
    gap: 4,
  },
  bigSosText: { fontSize: 16, fontWeight: '800', color: COLORS.white, letterSpacing: 0.5 },
  bigSosSub: { fontSize: 11, color: COLORS.white + 'bb' },
  filterScroll: { maxHeight: 48 },
  filters: { flexDirection: 'row', paddingHorizontal: SPACING.md, gap: 8, paddingBottom: 8 },
  filterBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: RADIUS.full,
    backgroundColor: COLORS.card,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterBtnActive: { backgroundColor: COLORS.danger, borderColor: COLORS.danger },
  filterText: { fontSize: 12, color: COLORS.textSecondary, fontWeight: '600' },
  filterTextActive: { color: COLORS.white },
  list: { padding: SPACING.md, gap: 10 },
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardImportant: { borderColor: COLORS.danger + '55', borderWidth: 1.5 },
  iconCircle: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  cardInfo: { flex: 1, marginLeft: 12 },
  contactName: { fontSize: 14, fontWeight: '700', color: COLORS.text },
  contactNumber: { fontSize: 16, fontWeight: '800', color: COLORS.accent, marginTop: 2 },
  contactDesc: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2, lineHeight: 16 },
  categoryLabel: { fontSize: 10, color: COLORS.textMuted, marginTop: 4, textTransform: 'uppercase' },
  callBtn: { width: 44, height: 44, justifyContent: 'center', alignItems: 'center' },
  protocolHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.warning + '18',
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    borderWidth: 1,
    borderColor: COLORS.warning + '44',
    gap: 10,
  },
  protocolTitle: { flex: 1, fontSize: 14, fontWeight: '700', color: COLORS.warning },
  protocolBody: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.md,
    gap: 8,
  },
  protocolStep: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  stepNum: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: COLORS.warning,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 1,
  },
  stepNumText: { fontSize: 11, fontWeight: '800', color: COLORS.black },
  stepText: { flex: 1, fontSize: 13, color: COLORS.text, lineHeight: 18 },
});

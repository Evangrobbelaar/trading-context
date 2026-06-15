import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet, Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { BOOKING_SITES, BOOKING_CATEGORIES } from '../data/accommodation';
import SearchBar from '../components/SearchBar';
import { COLORS, SPACING, RADIUS } from '../theme';

export default function AccommodationScreen() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');

  const filtered = BOOKING_SITES.filter((b) => {
    const matchSearch =
      b.name.toLowerCase().includes(search.toLowerCase()) ||
      b.description.toLowerCase().includes(search.toLowerCase());
    const matchCat = category === 'All' || b.category === category;
    return matchSearch && matchCat;
  });

  const popular = filtered.filter((b) => b.popular);
  const others = filtered.filter((b) => !b.popular);
  const sorted = [...popular, ...others];

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => Linking.openURL(item.url)}
      activeOpacity={0.75}
    >
      <View style={styles.cardTop}>
        <View style={[styles.iconCircle, { backgroundColor: COLORS.primary + '22' }]}>
          <Ionicons name={item.icon} size={22} color={COLORS.primary} />
        </View>
        <View style={{ flex: 1, marginLeft: 12 }}>
          <View style={styles.nameRow}>
            <Text style={styles.name}>{item.name}</Text>
            {item.popular && (
              <View style={styles.popularBadge}>
                <Text style={styles.popularText}>Popular</Text>
              </View>
            )}
          </View>
          <View style={styles.categoryChip}>
            <Text style={styles.categoryText}>{item.category}</Text>
          </View>
        </View>
        <Ionicons name="open-outline" size={18} color={COLORS.textSecondary} />
      </View>

      <Text style={styles.description}>{item.description}</Text>

      <View style={styles.tipRow}>
        <Ionicons name="bulb" size={14} color={COLORS.accent} />
        <Text style={styles.tipText}>{item.tip}</Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <View style={styles.intro}>
        <Text style={styles.introTitle}>Accommodation & Booking</Text>
        <Text style={styles.introSub}>
          Tap any card to open the booking website. All links open in your browser.
        </Text>
      </View>

      <SearchBar
        value={search}
        onChangeText={setSearch}
        placeholder="Search booking platforms..."
        onClear={() => setSearch('')}
      />

      <FlatList
        data={sorted}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <View style={styles.filterWrap}>
            <FlatList
              data={BOOKING_CATEGORIES}
              horizontal
              showsHorizontalScrollIndicator={false}
              keyExtractor={(c) => c}
              renderItem={({ item: c }) => (
                <TouchableOpacity
                  style={[styles.filterBtn, category === c && styles.filterBtnActive]}
                  onPress={() => setCategory(c)}
                >
                  <Text style={[styles.filterText, category === c && styles.filterTextActive]}>
                    {c}
                  </Text>
                </TouchableOpacity>
              )}
              contentContainerStyle={styles.filters}
            />
          </View>
        }
        ListEmptyComponent={
          <Text style={styles.empty}>No booking sites found.</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  intro: { paddingHorizontal: SPACING.md, paddingTop: SPACING.md, paddingBottom: SPACING.sm },
  introTitle: { fontSize: 20, fontWeight: '800', color: COLORS.text },
  introSub: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  filterWrap: { marginBottom: SPACING.sm },
  filters: { paddingHorizontal: SPACING.md, gap: 8 },
  filterBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: RADIUS.full,
    backgroundColor: COLORS.card,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterBtnActive: { backgroundColor: COLORS.accent, borderColor: COLORS.accent },
  filterText: { fontSize: 12, color: COLORS.textSecondary, fontWeight: '600' },
  filterTextActive: { color: COLORS.black },
  list: { padding: SPACING.md, gap: 12 },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardTop: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  iconCircle: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  nameRow: { flexDirection: 'row', alignItems: 'center', gap: 6, flexWrap: 'wrap' },
  name: { fontSize: 15, fontWeight: '700', color: COLORS.text },
  popularBadge: { backgroundColor: COLORS.accent + '33', borderRadius: RADIUS.full, paddingHorizontal: 6, paddingVertical: 2 },
  popularText: { fontSize: 10, color: COLORS.accent, fontWeight: '700' },
  categoryChip: { marginTop: 4 },
  categoryText: { fontSize: 11, color: COLORS.textSecondary },
  description: { fontSize: 13, color: COLORS.textSecondary, lineHeight: 19, marginBottom: 8 },
  tipRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 6, backgroundColor: COLORS.accent + '11', borderRadius: RADIUS.sm, padding: SPACING.sm },
  tipText: { fontSize: 12, color: COLORS.accent, flex: 1, lineHeight: 17 },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40 },
});

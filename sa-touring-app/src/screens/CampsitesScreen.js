import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { CAMPSITES } from '../data/campsites';
import SearchBar from '../components/SearchBar';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

const REGIONS = ['All', 'Western Cape', 'Eastern Cape', 'KwaZulu-Natal', 'Mpumalanga', 'Limpopo', 'Northern Cape', 'North West / Gauteng'];

export default function CampsitesScreen({ navigation }) {
  const [search, setSearch] = useState('');
  const [region, setRegion] = useState('All');

  const filtered = CAMPSITES.filter((c) => {
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.park.toLowerCase().includes(search.toLowerCase()) ||
      c.region.toLowerCase().includes(search.toLowerCase());
    const matchRegion = region === 'All' || c.region.includes(region.split(' /')[0]);
    return matchSearch && matchRegion;
  });

  const renderStars = (rating) => {
    const full = Math.floor(rating);
    return '★'.repeat(full) + (rating % 1 >= 0.5 ? '½' : '');
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('CampsiteDetail', { campsite: item })}
      activeOpacity={0.75}
    >
      <View style={styles.cardTop}>
        <View style={{ flex: 1 }}>
          <Text style={styles.name}>{item.name}</Text>
          <Text style={styles.park}>{item.park}</Text>
          <Text style={styles.region}>
            <Ionicons name="location" size={12} color={COLORS.textSecondary} /> {item.region}
          </Text>
        </View>
        <View style={styles.ratingBlock}>
          <Text style={styles.ratingStars}>{renderStars(item.rating)}</Text>
          <Text style={styles.ratingNum}>{item.rating}</Text>
        </View>
      </View>

      <Text style={styles.desc} numberOfLines={2}>{item.description}</Text>

      <View style={styles.infoRow}>
        <View style={styles.infoItem}>
          <Ionicons name="pricetag" size={12} color={COLORS.accent} />
          <Text style={styles.infoText}>{item.priceRange}</Text>
        </View>
        <View style={styles.infoItem}>
          <Ionicons name="people" size={12} color={COLORS.textSecondary} />
          <Text style={styles.infoText}>{item.capacity}</Text>
        </View>
      </View>

      <View style={styles.tags}>
        {item.tags.slice(0, 4).map((t) => (
          <TagBadge key={t} label={t} />
        ))}
      </View>

      <View style={styles.facilityRow}>
        {item.facilities.slice(0, 4).map((f) => (
          <View key={f} style={styles.facility}>
            <Ionicons name="checkmark-circle" size={12} color={COLORS.success} />
            <Text style={styles.facilityText}>{f}</Text>
          </View>
        ))}
        {item.facilities.length > 4 && (
          <Text style={styles.moreFacilities}>+{item.facilities.length - 4} more</Text>
        )}
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <SearchBar
        value={search}
        onChangeText={setSearch}
        placeholder="Search campsites or parks..."
        onClear={() => setSearch('')}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <View style={styles.filterWrap}>
            <FlatList
              data={REGIONS}
              horizontal
              showsHorizontalScrollIndicator={false}
              keyExtractor={(r) => r}
              renderItem={({ item: r }) => (
                <TouchableOpacity
                  style={[styles.filterBtn, region === r && styles.filterBtnActive]}
                  onPress={() => setRegion(r)}
                >
                  <Text style={[styles.filterText, region === r && styles.filterTextActive]}>
                    {r}
                  </Text>
                </TouchableOpacity>
              )}
              contentContainerStyle={styles.filters}
            />
          </View>
        }
        ListEmptyComponent={
          <Text style={styles.empty}>No campsites found.</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
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
  cardTop: { flexDirection: 'row', marginBottom: 6 },
  name: { fontSize: 15, fontWeight: '700', color: COLORS.text },
  park: { fontSize: 12, color: COLORS.primary, fontWeight: '600', marginTop: 2 },
  region: { fontSize: 11, color: COLORS.textSecondary, marginTop: 2 },
  ratingBlock: { alignItems: 'flex-end' },
  ratingStars: { fontSize: 12, color: COLORS.accent },
  ratingNum: { fontSize: 14, fontWeight: '700', color: COLORS.text },
  desc: { fontSize: 13, color: COLORS.textSecondary, lineHeight: 18, marginBottom: 8 },
  infoRow: { flexDirection: 'row', gap: 16, marginBottom: 8 },
  infoItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  infoText: { fontSize: 12, color: COLORS.textSecondary },
  tags: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 6 },
  facilityRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 6 },
  facility: { flexDirection: 'row', alignItems: 'center', gap: 3 },
  facilityText: { fontSize: 11, color: COLORS.textSecondary },
  moreFacilities: { fontSize: 11, color: COLORS.textMuted, fontStyle: 'italic' },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40 },
});

import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ROUTES, DIFFICULTY_COLORS, CATEGORY_LABELS } from '../data/routes';
import SearchBar from '../components/SearchBar';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

const FILTERS = ['All', '4x4', 'scenic'];

export default function RoutesScreen({ navigation }) {
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('All');

  const filtered = ROUTES.filter((r) => {
    const matchSearch =
      r.name.toLowerCase().includes(search.toLowerCase()) ||
      r.region.toLowerCase().includes(search.toLowerCase());
    const matchFilter = filter === 'All' || r.category === filter;
    return matchSearch && matchFilter;
  });

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('RouteDetail', { route: item })}
      activeOpacity={0.75}
    >
      <View style={styles.cardHeader}>
        <View style={styles.cardHeaderLeft}>
          <Text style={styles.cardName}>{item.name}</Text>
          <Text style={styles.cardRegion}>
            <Ionicons name="location" size={12} color={COLORS.textSecondary} /> {item.region}
          </Text>
        </View>
        <View
          style={[
            styles.diffBadge,
            { backgroundColor: DIFFICULTY_COLORS[item.difficulty] + '33' },
          ]}
        >
          <Text
            style={[styles.diffText, { color: DIFFICULTY_COLORS[item.difficulty] }]}
          >
            {item.difficulty}
          </Text>
        </View>
      </View>

      <Text style={styles.cardDesc} numberOfLines={2}>
        {item.description}
      </Text>

      <View style={styles.metaRow}>
        <View style={styles.metaItem}>
          <Ionicons name="resize" size={13} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>{item.distance}</Text>
        </View>
        <View style={styles.metaItem}>
          <Ionicons name="time" size={13} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>{item.duration}</Text>
        </View>
        <View style={styles.metaItem}>
          <Ionicons name="sunny" size={13} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>{item.bestSeason}</Text>
        </View>
      </View>

      <View style={styles.tags}>
        {item.tags.slice(0, 3).map((t) => (
          <TagBadge key={t} label={t} />
        ))}
        <View style={styles.categoryBadge}>
          <Text style={styles.categoryText}>
            {CATEGORY_LABELS[item.category]}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <SearchBar
        value={search}
        onChangeText={setSearch}
        placeholder="Search routes or regions..."
        onClear={() => setSearch('')}
      />

      <View style={styles.filterRow}>
        {FILTERS.map((f) => (
          <TouchableOpacity
            key={f}
            style={[styles.filterBtn, filter === f && styles.filterBtnActive]}
            onPress={() => setFilter(f)}
          >
            <Text style={[styles.filterText, filter === f && styles.filterTextActive]}>
              {f === '4x4' ? '4x4 Off-Road' : f === 'scenic' ? 'Scenic Drive' : f}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <FlatList
        data={filtered}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <Text style={styles.empty}>No routes found for "{search}"</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  filterRow: {
    flexDirection: 'row',
    paddingHorizontal: SPACING.md,
    marginBottom: SPACING.sm,
    gap: 8,
  },
  filterBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: RADIUS.full,
    backgroundColor: COLORS.card,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterBtnActive: {
    backgroundColor: COLORS.accent,
    borderColor: COLORS.accent,
  },
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
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 6,
  },
  cardHeaderLeft: { flex: 1, marginRight: 8 },
  cardName: { fontSize: 16, fontWeight: '700', color: COLORS.text },
  cardRegion: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  diffBadge: {
    borderRadius: RADIUS.full,
    paddingHorizontal: 10,
    paddingVertical: 4,
  },
  diffText: { fontSize: 11, fontWeight: '700' },
  cardDesc: {
    fontSize: 13,
    color: COLORS.textSecondary,
    lineHeight: 19,
    marginBottom: 10,
  },
  metaRow: { flexDirection: 'row', marginBottom: 8, gap: 12 },
  metaItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  metaText: { fontSize: 11, color: COLORS.textSecondary },
  tags: { flexDirection: 'row', flexWrap: 'wrap', alignItems: 'center' },
  categoryBadge: {
    backgroundColor: COLORS.accent + '22',
    borderRadius: RADIUS.full,
    paddingHorizontal: 8,
    paddingVertical: 3,
    marginLeft: 4,
  },
  categoryText: { fontSize: 11, fontWeight: '600', color: COLORS.accent },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40, fontSize: 14 },
});

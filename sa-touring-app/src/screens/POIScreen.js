import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet, Linking,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { POINTS_OF_INTEREST, POI_CATEGORIES } from '../data/poi';
import SearchBar from '../components/SearchBar';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

const CATEGORY_ICONS = {
  Viewpoint: 'eye',
  Heritage: 'library',
  Nature: 'leaf',
  Adventure: 'flash',
  'Food & Wine': 'wine',
  Experience: 'ticket',
  Town: 'business',
};

export default function POIScreen() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');

  const filtered = POINTS_OF_INTEREST.filter((p) => {
    const matchSearch =
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.region.toLowerCase().includes(search.toLowerCase());
    const matchCat = category === 'All' || p.category === category;
    return matchSearch && matchCat;
  });

  const openMaps = (coords, name) => {
    Linking.openURL(`https://maps.google.com/?q=${coords.lat},${coords.lng}(${encodeURIComponent(name)})`);
  };

  const openUrl = (url) => {
    if (url) Linking.openURL(url);
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.cardTop}>
        <View style={[styles.catIcon, { backgroundColor: COLORS.info + '22' }]}>
          <Ionicons name={CATEGORY_ICONS[item.category] || 'location'} size={22} color={COLORS.info} />
        </View>
        <View style={{ flex: 1, marginLeft: 10 }}>
          <Text style={styles.name}>{item.name}</Text>
          <Text style={styles.region}>
            <Ionicons name="location" size={12} color={COLORS.textSecondary} /> {item.region}
          </Text>
        </View>
        <View style={styles.catBadge}>
          <Text style={styles.catText}>{item.category}</Text>
        </View>
      </View>

      <Text style={styles.desc}>{item.description}</Text>

      {item.highlights && (
        <View style={styles.highlightsWrap}>
          {item.highlights.slice(0, 3).map((h, i) => (
            <View key={i} style={styles.highlight}>
              <Ionicons name="star" size={12} color={COLORS.accent} />
              <Text style={styles.highlightText}>{h}</Text>
            </View>
          ))}
        </View>
      )}

      <View style={styles.infoRow}>
        {item.entryFee && (
          <View style={styles.feeTag}>
            <Ionicons name="pricetag" size={12} color={COLORS.accent} />
            <Text style={styles.feeText}>{item.entryFee}</Text>
          </View>
        )}
        {item.bestTime && (
          <View style={styles.feeTag}>
            <Ionicons name="sunny" size={12} color={COLORS.warning} />
            <Text style={[styles.feeText, { color: COLORS.warning }]}>{item.bestTime}</Text>
          </View>
        )}
      </View>

      <View style={styles.tags}>
        {item.tags.map((t) => (
          <TagBadge key={t} label={t} />
        ))}
      </View>

      <View style={styles.btnRow}>
        <TouchableOpacity
          style={styles.mapBtn}
          onPress={() => openMaps(item.coordinates, item.name)}
        >
          <Ionicons name="navigate" size={16} color={COLORS.accent} />
          <Text style={styles.mapBtnText}>Directions</Text>
        </TouchableOpacity>
        {item.bookingUrl && (
          <TouchableOpacity
            style={[styles.mapBtn, { flex: 1.5 }]}
            onPress={() => openUrl(item.bookingUrl)}
          >
            <Ionicons name="globe" size={16} color={COLORS.primary} />
            <Text style={[styles.mapBtnText, { color: COLORS.primary }]}>More Info</Text>
          </TouchableOpacity>
        )}
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <SearchBar
        value={search}
        onChangeText={setSearch}
        placeholder="Search points of interest..."
        onClear={() => setSearch('')}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <FlatList
            data={POI_CATEGORIES}
            horizontal
            showsHorizontalScrollIndicator={false}
            keyExtractor={(c) => c}
            renderItem={({ item: c }) => (
              <TouchableOpacity
                style={[styles.filterBtn, category === c && styles.filterBtnActive]}
                onPress={() => setCategory(c)}
              >
                <Text style={[styles.filterText, category === c && styles.filterTextActive]}>{c}</Text>
              </TouchableOpacity>
            )}
            contentContainerStyle={styles.filters}
          />
        }
        ListEmptyComponent={
          <Text style={styles.empty}>No points of interest found.</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  filters: { paddingHorizontal: SPACING.md, gap: 8, paddingBottom: SPACING.sm },
  filterBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: RADIUS.full,
    backgroundColor: COLORS.card,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  filterBtnActive: { backgroundColor: COLORS.info, borderColor: COLORS.info },
  filterText: { fontSize: 12, color: COLORS.textSecondary, fontWeight: '600' },
  filterTextActive: { color: COLORS.white },
  list: { padding: SPACING.md, gap: 12 },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardTop: { flexDirection: 'row', alignItems: 'center', marginBottom: 8 },
  catIcon: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  name: { fontSize: 15, fontWeight: '700', color: COLORS.text },
  region: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  catBadge: { backgroundColor: COLORS.info + '22', borderRadius: RADIUS.full, paddingHorizontal: 8, paddingVertical: 3 },
  catText: { fontSize: 11, color: COLORS.info, fontWeight: '600' },
  desc: { fontSize: 13, color: COLORS.textSecondary, lineHeight: 19, marginBottom: 8 },
  highlightsWrap: { marginBottom: 8, gap: 4 },
  highlight: { flexDirection: 'row', alignItems: 'center', gap: 6 },
  highlightText: { fontSize: 12, color: COLORS.text },
  infoRow: { flexDirection: 'row', gap: 8, marginBottom: 8, flexWrap: 'wrap' },
  feeTag: { flexDirection: 'row', alignItems: 'center', gap: 4, backgroundColor: COLORS.surface, borderRadius: RADIUS.sm, paddingHorizontal: 8, paddingVertical: 4 },
  feeText: { fontSize: 11, color: COLORS.accent },
  tags: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 8 },
  btnRow: { flexDirection: 'row', gap: 8 },
  mapBtn: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: COLORS.accent,
    borderRadius: RADIUS.sm,
    paddingVertical: 8,
    gap: 6,
  },
  mapBtnText: { fontSize: 13, color: COLORS.accent, fontWeight: '600' },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40 },
});

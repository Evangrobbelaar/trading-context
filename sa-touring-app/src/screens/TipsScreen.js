import React, { useState } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, StyleSheet, ScrollView,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { TRAVEL_TIPS, TIP_CATEGORIES } from '../data/tips';
import SearchBar from '../components/SearchBar';
import { COLORS, SPACING, RADIUS } from '../theme';

export default function TipsScreen() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');
  const [expanded, setExpanded] = useState(null);

  const filtered = TRAVEL_TIPS.filter((t) => {
    const matchCat = category === 'All' || t.category === category;
    const matchSearch = search === '' || t.title.toLowerCase().includes(search.toLowerCase()) ||
      t.tips.some((tip) => tip.toLowerCase().includes(search.toLowerCase()));
    return matchCat && matchSearch;
  });

  const toggleExpand = (id) => setExpanded(expanded === id ? null : id);

  const renderItem = ({ item }) => {
    const isOpen = expanded === item.id;
    const matchingTips = search
      ? item.tips.filter((t) => t.toLowerCase().includes(search.toLowerCase()))
      : item.tips;

    return (
      <View style={styles.card}>
        <TouchableOpacity style={styles.cardHeader} onPress={() => toggleExpand(item.id)} activeOpacity={0.7}>
          <View style={[styles.iconCircle, { backgroundColor: COLORS.primary + '22' }]}>
            <Ionicons name={item.icon} size={22} color={COLORS.primary} />
          </View>
          <View style={{ flex: 1, marginLeft: 12 }}>
            <Text style={styles.cardTitle}>{item.title}</Text>
            <Text style={styles.cardSubtitle}>{item.tips.length} tips</Text>
          </View>
          <Ionicons
            name={isOpen ? 'chevron-up' : 'chevron-down'}
            size={20}
            color={COLORS.textSecondary}
          />
        </TouchableOpacity>

        {isOpen && (
          <View style={styles.tipsBody}>
            {matchingTips.map((tip, i) => (
              <View key={i} style={styles.tipRow}>
                <View style={styles.tipBullet}>
                  <Text style={styles.tipBulletText}>{i + 1}</Text>
                </View>
                <Text style={styles.tipText}>{tip}</Text>
              </View>
            ))}
          </View>
        )}
      </View>
    );
  };

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <SearchBar
        value={search}
        onChangeText={(t) => { setSearch(t); if (t) setExpanded('all'); }}
        placeholder="Search tips..."
        onClear={() => { setSearch(''); setExpanded(null); }}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
            <View style={styles.filters}>
              {TIP_CATEGORIES.map((c) => (
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
        }
        ListEmptyComponent={
          <Text style={styles.empty}>No tips found for your search.</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
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
  filterBtnActive: { backgroundColor: COLORS.primary, borderColor: COLORS.primary },
  filterText: { fontSize: 12, color: COLORS.textSecondary, fontWeight: '600' },
  filterTextActive: { color: COLORS.white },
  list: { padding: SPACING.md, gap: 10 },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    overflow: 'hidden',
  },
  cardHeader: { flexDirection: 'row', alignItems: 'center', padding: SPACING.md },
  iconCircle: { width: 44, height: 44, borderRadius: 22, justifyContent: 'center', alignItems: 'center' },
  cardTitle: { fontSize: 14, fontWeight: '700', color: COLORS.text },
  cardSubtitle: { fontSize: 11, color: COLORS.textSecondary, marginTop: 2 },
  tipsBody: { borderTopWidth: 1, borderTopColor: COLORS.border, padding: SPACING.md, gap: 10 },
  tipRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 10 },
  tipBullet: {
    width: 22,
    height: 22,
    borderRadius: 11,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 1,
    flexShrink: 0,
  },
  tipBulletText: { fontSize: 11, fontWeight: '800', color: COLORS.white },
  tipText: { flex: 1, fontSize: 13, color: COLORS.text, lineHeight: 19 },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40 },
});

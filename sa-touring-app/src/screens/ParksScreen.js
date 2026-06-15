import React, { useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PARKS } from '../data/parks';
import SearchBar from '../components/SearchBar';
import TagBadge from '../components/TagBadge';
import { COLORS, SPACING, RADIUS } from '../theme';

export default function ParksScreen({ navigation }) {
  const [search, setSearch] = useState('');

  const filtered = PARKS.filter(
    (p) =>
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.region.toLowerCase().includes(search.toLowerCase()),
  );

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={styles.card}
      onPress={() => navigation.navigate('ParkDetail', { park: item })}
      activeOpacity={0.75}
    >
      <View style={styles.cardHeader}>
        <View style={{ flex: 1 }}>
          <Text style={styles.name}>{item.name}</Text>
          <Text style={styles.region}>
            <Ionicons name="location" size={12} color={COLORS.textSecondary} /> {item.region}
          </Text>
        </View>
        <View style={styles.sizeBadge}>
          <Text style={styles.sizeText}>{item.size}</Text>
        </View>
      </View>

      <Text style={styles.desc} numberOfLines={2}>{item.description}</Text>

      <View style={styles.metaRow}>
        <View style={styles.metaItem}>
          <Ionicons name="calendar" size={12} color={COLORS.textSecondary} />
          <Text style={styles.metaText}>Est. {item.established}</Text>
        </View>
        <View style={styles.metaItem}>
          <Ionicons name="pricetag" size={12} color={COLORS.accent} />
          <Text style={styles.metaText}>{item.fees.split(':')[0]}</Text>
        </View>
        {item.malariaRisk && (
          <View style={styles.malariaTag}>
            <Ionicons name="warning" size={11} color={COLORS.danger} />
            <Text style={styles.malariaText}>Malaria Zone</Text>
          </View>
        )}
      </View>

      <View style={styles.wildlife}>
        <Text style={styles.wildlifeLabel}>Wildlife: </Text>
        <Text style={styles.wildlifeText} numberOfLines={1}>
          {item.wildlife.join(' · ')}
        </Text>
      </View>

      <View style={styles.tags}>
        {item.tags.map((t) => (
          <TagBadge key={t} label={t} />
        ))}
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <SearchBar
        value={search}
        onChangeText={setSearch}
        placeholder="Search parks or regions..."
        onClear={() => setSearch('')}
      />
      <FlatList
        data={filtered}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.list}
        ListEmptyComponent={
          <Text style={styles.empty}>No parks found.</Text>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  list: { padding: SPACING.md, gap: 12 },
  card: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardHeader: { flexDirection: 'row', marginBottom: 6, alignItems: 'flex-start' },
  name: { fontSize: 16, fontWeight: '700', color: COLORS.text },
  region: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  sizeBadge: {
    backgroundColor: COLORS.primary + '22',
    borderRadius: RADIUS.full,
    paddingHorizontal: 8,
    paddingVertical: 3,
  },
  sizeText: { fontSize: 11, color: COLORS.primary, fontWeight: '600' },
  desc: { fontSize: 13, color: COLORS.textSecondary, lineHeight: 18, marginBottom: 8 },
  metaRow: { flexDirection: 'row', alignItems: 'center', gap: 10, marginBottom: 8 },
  metaItem: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  metaText: { fontSize: 11, color: COLORS.textSecondary },
  malariaTag: { flexDirection: 'row', alignItems: 'center', gap: 3, backgroundColor: COLORS.danger + '22', borderRadius: RADIUS.full, paddingHorizontal: 8, paddingVertical: 2 },
  malariaText: { fontSize: 11, color: COLORS.danger, fontWeight: '600' },
  wildlife: { flexDirection: 'row', marginBottom: 8, alignItems: 'center' },
  wildlifeLabel: { fontSize: 12, color: COLORS.accent, fontWeight: '600' },
  wildlifeText: { fontSize: 12, color: COLORS.textSecondary, flex: 1 },
  tags: { flexDirection: 'row', flexWrap: 'wrap' },
  empty: { textAlign: 'center', color: COLORS.textSecondary, marginTop: 40 },
});

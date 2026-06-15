import React, { useState, useEffect } from 'react';
import {
  View, Text, ScrollView, StyleSheet, TouchableOpacity,
  TextInput, Alert, FlatList,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { COLORS, SPACING, RADIUS } from '../theme';

const STORAGE_KEY = '@sa_touring_trips';

const SA_DESTINATIONS = [
  'Cape Town', 'Kruger National Park', 'Johannesburg', 'Durban', 'Garden Route',
  'Drakensberg', 'Knysna', 'Plettenberg Bay', 'Wilderness', 'Oudtshoorn',
  'Stellenbosch', 'Franschhoek', 'Hermanus', 'Springbok', 'Upington',
  'Kgalagadi', 'Augrabies', 'Kimberley', 'Bloemfontein', 'Clarens',
  'Skukuza', 'Phalaborwa', 'Hoedspruit', 'Hazyview', 'Graskop',
  'Hluhluwe', 'St Lucia', 'Bergville', 'Winterton', 'Ladysmith',
  'Addo', 'Port Elizabeth (Gqeberha)', 'East London', 'Mthatha', 'Cradock',
  'Calvinia', 'Clanwilliam', 'Citrusdal', 'Swellendam', 'Montagu',
  'Richtersveld', 'Port Nolloth', 'Alexander Bay', 'Vioolsdrift',
  'Polokwane', 'Tzaneen', 'Bela-Bela', 'Mokopane', 'Musina',
];

const VEHICLE_TYPES = ['Sedan', 'SUV', '4x4', 'Bakkie (2WD)', 'Bakkie (4x4)', 'Campervan'];

export default function TripPlannerScreen() {
  const [trips, setTrips] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [tripName, setTripName] = useState('');
  const [stops, setStops] = useState(['', '']);
  const [nights, setNights] = useState(['']);
  const [vehicle, setVehicle] = useState('4x4');
  const [notes, setNotes] = useState('');
  const [destSearch, setDestSearch] = useState('');
  const [activeStop, setActiveStop] = useState(null);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY).then((v) => {
      if (v) setTrips(JSON.parse(v));
    });
  }, []);

  const saveTrips = async (newTrips) => {
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(newTrips));
    setTrips(newTrips);
  };

  const addStop = () => setStops([...stops, '']);

  const setStop = (i, val) => {
    const s = [...stops];
    s[i] = val;
    setStops(s);
  };

  const removeStop = (i) => {
    if (stops.length <= 2) return;
    setStops(stops.filter((_, idx) => idx !== i));
  };

  const saveTrip = () => {
    if (!tripName.trim()) {
      Alert.alert('Trip name required');
      return;
    }
    const validStops = stops.filter((s) => s.trim());
    if (validStops.length < 2) {
      Alert.alert('Add at least 2 destinations');
      return;
    }
    const trip = {
      id: Date.now().toString(),
      name: tripName,
      stops: validStops,
      vehicle,
      notes,
      created: new Date().toLocaleDateString('en-ZA'),
    };
    saveTrips([trip, ...trips]);
    setShowNew(false);
    setTripName('');
    setStops(['', '']);
    setNotes('');
  };

  const deleteTrip = (id) => {
    Alert.alert('Delete Trip', 'Remove this trip plan?', [
      { text: 'Cancel' },
      { text: 'Delete', style: 'destructive', onPress: () => saveTrips(trips.filter((t) => t.id !== id)) },
    ]);
  };

  const suggestions = SA_DESTINATIONS.filter(
    (d) => destSearch && d.toLowerCase().includes(destSearch.toLowerCase()),
  ).slice(0, 5);

  const renderTrip = ({ item }) => (
    <View style={styles.tripCard}>
      <View style={styles.tripHeader}>
        <View>
          <Text style={styles.tripName}>{item.name}</Text>
          <Text style={styles.tripMeta}>Created {item.created} · {item.vehicle}</Text>
        </View>
        <TouchableOpacity onPress={() => deleteTrip(item.id)}>
          <Ionicons name="trash-outline" size={20} color={COLORS.danger} />
        </TouchableOpacity>
      </View>
      <View style={styles.routeViz}>
        {item.stops.map((stop, i) => (
          <View key={i} style={styles.stopRow}>
            <View style={styles.stopDot}>
              <Text style={styles.stopDotNum}>{i + 1}</Text>
            </View>
            {i < item.stops.length - 1 && <View style={styles.stopLine} />}
            <Text style={styles.stopName}>{stop}</Text>
          </View>
        ))}
      </View>
      {item.notes ? (
        <View style={styles.notesRow}>
          <Ionicons name="document-text" size={14} color={COLORS.textSecondary} />
          <Text style={styles.notesText}>{item.notes}</Text>
        </View>
      ) : null}
    </View>
  );

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <FlatList
        data={trips}
        keyExtractor={(item) => item.id}
        renderItem={renderTrip}
        contentContainerStyle={styles.list}
        ListHeaderComponent={
          <View>
            <View style={styles.headerRow}>
              <View>
                <Text style={styles.title}>Trip Planner</Text>
                <Text style={styles.subtitle}>Plan your South Africa road trip</Text>
              </View>
              <TouchableOpacity
                style={styles.newBtn}
                onPress={() => setShowNew(!showNew)}
              >
                <Ionicons name={showNew ? 'close' : 'add'} size={20} color={COLORS.black} />
                <Text style={styles.newBtnText}>{showNew ? 'Cancel' : 'New Trip'}</Text>
              </TouchableOpacity>
            </View>

            {showNew && (
              <View style={styles.form}>
                <Text style={styles.formLabel}>Trip Name</Text>
                <TextInput
                  style={styles.input}
                  value={tripName}
                  onChangeText={setTripName}
                  placeholder="e.g. Kruger & Panorama Route 2026"
                  placeholderTextColor={COLORS.textMuted}
                />

                <Text style={styles.formLabel}>Vehicle Type</Text>
                <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.vehicleScroll}>
                  <View style={styles.vehicleRow}>
                    {VEHICLE_TYPES.map((v) => (
                      <TouchableOpacity
                        key={v}
                        style={[styles.vehicleBtn, vehicle === v && styles.vehicleBtnActive]}
                        onPress={() => setVehicle(v)}
                      >
                        <Text style={[styles.vehicleBtnText, vehicle === v && styles.vehicleBtnTextActive]}>{v}</Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                </ScrollView>

                <Text style={styles.formLabel}>Destinations / Route Stops</Text>
                {stops.map((stop, i) => (
                  <View key={i} style={styles.stopInputRow}>
                    <View style={styles.stopNumBadge}>
                      <Text style={styles.stopNum}>{i + 1}</Text>
                    </View>
                    <TextInput
                      style={[styles.input, { flex: 1, marginBottom: 0 }]}
                      value={stop}
                      onChangeText={(v) => { setStop(i, v); setDestSearch(v); setActiveStop(i); }}
                      onFocus={() => setActiveStop(i)}
                      placeholder={i === 0 ? 'Start (e.g. Cape Town)' : i === stops.length - 1 ? 'End destination' : `Stop ${i + 1}`}
                      placeholderTextColor={COLORS.textMuted}
                    />
                    {stops.length > 2 && (
                      <TouchableOpacity onPress={() => removeStop(i)} style={styles.removeStop}>
                        <Ionicons name="close-circle" size={20} color={COLORS.danger} />
                      </TouchableOpacity>
                    )}
                  </View>
                ))}

                {activeStop !== null && suggestions.length > 0 && (
                  <View style={styles.suggestions}>
                    {suggestions.map((s) => (
                      <TouchableOpacity
                        key={s}
                        style={styles.suggRow}
                        onPress={() => {
                          setStop(activeStop, s);
                          setDestSearch('');
                        }}
                      >
                        <Ionicons name="location" size={14} color={COLORS.textSecondary} />
                        <Text style={styles.suggText}>{s}</Text>
                      </TouchableOpacity>
                    ))}
                  </View>
                )}

                <TouchableOpacity style={styles.addStopBtn} onPress={addStop}>
                  <Ionicons name="add-circle-outline" size={18} color={COLORS.primary} />
                  <Text style={styles.addStopText}>Add another stop</Text>
                </TouchableOpacity>

                <Text style={styles.formLabel}>Notes (optional)</Text>
                <TextInput
                  style={[styles.input, styles.notesInput]}
                  value={notes}
                  onChangeText={setNotes}
                  multiline
                  placeholder="Accommodation booked? Permits needed? Special notes..."
                  placeholderTextColor={COLORS.textMuted}
                />

                <TouchableOpacity style={styles.saveBtn} onPress={saveTrip}>
                  <Ionicons name="checkmark-circle" size={20} color={COLORS.black} />
                  <Text style={styles.saveBtnText}>Save Trip Plan</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
        }
        ListEmptyComponent={
          !showNew ? (
            <View style={styles.empty}>
              <Ionicons name="map-outline" size={48} color={COLORS.textMuted} />
              <Text style={styles.emptyText}>No trips planned yet.</Text>
              <Text style={styles.emptySub}>Tap "New Trip" to start planning your South Africa adventure.</Text>
            </View>
          ) : null
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  list: { padding: SPACING.md, gap: 12 },
  headerRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: SPACING.md },
  title: { fontSize: 22, fontWeight: '800', color: COLORS.text },
  subtitle: { fontSize: 12, color: COLORS.textSecondary, marginTop: 2 },
  newBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.accent,
    borderRadius: RADIUS.md,
    paddingHorizontal: 12,
    paddingVertical: 8,
    gap: 4,
  },
  newBtnText: { fontSize: 13, fontWeight: '700', color: COLORS.black },
  form: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.md,
  },
  formLabel: { fontSize: 12, fontWeight: '700', color: COLORS.accent, marginBottom: 6, marginTop: 12, textTransform: 'uppercase' },
  input: {
    backgroundColor: COLORS.surface,
    borderRadius: RADIUS.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
    color: COLORS.text,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    marginBottom: SPACING.sm,
  },
  vehicleScroll: { marginBottom: SPACING.sm },
  vehicleRow: { flexDirection: 'row', gap: 8 },
  vehicleBtn: {
    paddingHorizontal: 12,
    paddingVertical: 7,
    borderRadius: RADIUS.full,
    backgroundColor: COLORS.surface,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  vehicleBtnActive: { backgroundColor: COLORS.accent, borderColor: COLORS.accent },
  vehicleBtnText: { fontSize: 12, color: COLORS.textSecondary, fontWeight: '600' },
  vehicleBtnTextActive: { color: COLORS.black },
  stopInputRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: SPACING.sm },
  stopNumBadge: { width: 26, height: 26, borderRadius: 13, backgroundColor: COLORS.primary, justifyContent: 'center', alignItems: 'center' },
  stopNum: { fontSize: 12, fontWeight: '700', color: COLORS.white },
  removeStop: { padding: 4 },
  suggestions: {
    backgroundColor: COLORS.cardElevated,
    borderRadius: RADIUS.sm,
    borderWidth: 1,
    borderColor: COLORS.border,
    marginBottom: SPACING.sm,
  },
  suggRow: { flexDirection: 'row', alignItems: 'center', gap: 8, paddingHorizontal: 12, paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: COLORS.border },
  suggText: { fontSize: 14, color: COLORS.text },
  addStopBtn: { flexDirection: 'row', alignItems: 'center', gap: 6, paddingVertical: 6 },
  addStopText: { fontSize: 13, color: COLORS.primary, fontWeight: '600' },
  notesInput: { height: 80, textAlignVertical: 'top' },
  saveBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: COLORS.accent,
    borderRadius: RADIUS.md,
    paddingVertical: 14,
    marginTop: SPACING.md,
    gap: 8,
  },
  saveBtnText: { fontSize: 15, fontWeight: '700', color: COLORS.black },
  tripCard: {
    backgroundColor: COLORS.card,
    borderRadius: RADIUS.md,
    padding: SPACING.md,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  tripHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 },
  tripName: { fontSize: 16, fontWeight: '700', color: COLORS.text },
  tripMeta: { fontSize: 11, color: COLORS.textSecondary, marginTop: 2 },
  routeViz: { gap: 0 },
  stopRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 0 },
  stopDot: { width: 22, height: 22, borderRadius: 11, backgroundColor: COLORS.primary, justifyContent: 'center', alignItems: 'center', zIndex: 1 },
  stopDotNum: { fontSize: 10, fontWeight: '800', color: COLORS.white },
  stopLine: { position: 'absolute', left: 10, top: 22, width: 2, height: 16, backgroundColor: COLORS.border, zIndex: 0 },
  stopName: { fontSize: 14, color: COLORS.text, marginLeft: 10, paddingBottom: 12 },
  notesRow: { flexDirection: 'row', alignItems: 'flex-start', gap: 6, marginTop: 8, backgroundColor: COLORS.surface, borderRadius: RADIUS.sm, padding: SPACING.sm },
  notesText: { fontSize: 12, color: COLORS.textSecondary, flex: 1 },
  empty: { alignItems: 'center', paddingTop: 60 },
  emptyText: { fontSize: 16, color: COLORS.textSecondary, marginTop: 12, fontWeight: '600' },
  emptySub: { fontSize: 13, color: COLORS.textMuted, textAlign: 'center', marginTop: 6, paddingHorizontal: 20 },
});

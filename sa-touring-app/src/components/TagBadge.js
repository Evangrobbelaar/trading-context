import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, RADIUS } from '../theme';

export default function TagBadge({ label, color, textColor }) {
  return (
    <View style={[styles.badge, { backgroundColor: color || COLORS.primary + '33' }]}>
      <Text style={[styles.text, { color: textColor || COLORS.primary }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    borderRadius: RADIUS.full,
    paddingHorizontal: 8,
    paddingVertical: 3,
    marginRight: 4,
    marginBottom: 4,
  },
  text: {
    fontSize: 11,
    fontWeight: '600',
  },
});

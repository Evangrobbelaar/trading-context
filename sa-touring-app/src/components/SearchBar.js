import React from 'react';
import { View, TextInput, StyleSheet, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { COLORS } from '../theme';

export default function SearchBar({ value, onChangeText, placeholder, onClear }) {
  return (
    <View style={styles.container}>
      <Ionicons name="search" size={18} color={COLORS.textSecondary} style={styles.icon} />
      <TextInput
        style={styles.input}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder || 'Search...'}
        placeholderTextColor={COLORS.textSecondary}
        clearButtonMode="while-editing"
      />
      {value.length > 0 && (
        <TouchableOpacity onPress={onClear} style={styles.clearBtn}>
          <Ionicons name="close-circle" size={18} color={COLORS.textSecondary} />
        </TouchableOpacity>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.card,
    borderRadius: 10,
    paddingHorizontal: 10,
    marginHorizontal: 16,
    marginVertical: 8,
    height: 42,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  icon: { marginRight: 8 },
  input: {
    flex: 1,
    color: COLORS.text,
    fontSize: 15,
  },
  clearBtn: { padding: 4 },
});

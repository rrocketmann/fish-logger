import React, { useState } from 'react';
import { View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Image, Alert } from 'react-native';
import { useDatabase } from '../context/DatabaseContext';

export default function SubmitScreen({ route, navigation }) {
  const { photoUri, suggestedSpecies } = route.params || {};
  const { addCatch, syncStatus } = useDatabase();

  const [species, setSpecies] = useState(suggestedSpecies || '');
  const [fisherName, setFisherName] = useState('');
  const [location, setLocation] = useState('');
  const [notes, setNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!photoUri) {
      Alert.alert('Error', 'No photo selected');
      return;
    }

    setSubmitting(true);

    try {
      await addCatch({
        photo_uri: photoUri,
        species: species || 'Unknown',
        fisher_name: fisherName,
        location,
        notes,
      });

      Alert.alert(
        'Success', 
        syncStatus === 'offline' 
          ? 'Catch saved locally. Will sync when online.' 
          : 'Catch submitted successfully!',
        [{ text: 'OK', onPress: () => navigation.navigate('Home') }]
      );
    } catch (error) {
      Alert.alert('Error', 'Failed to save catch. Please try again.');
      console.error(error);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      {photoUri && (
        <View style={styles.imageContainer}>
          <Image source={{ uri: photoUri }} style={styles.image} />
        </View>
      )}

      <View style={styles.form}>
        <View style={styles.formGroup}>
          <Text style={styles.label}>Species {!species && <Text style={styles.optional}>(Optional - defaults to Unknown)</Text>}</Text>
          <TextInput
            style={styles.input}
            value={species}
            onChangeText={setSpecies}
            placeholder="e.g., Sea Bass"
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Your Name</Text>
          <TextInput
            style={styles.input}
            value={fisherName}
            onChangeText={setFisherName}
            placeholder="Fisher or researcher name"
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Location</Text>
          <TextInput
            style={styles.input}
            value={location}
            onChangeText={setLocation}
            placeholder="e.g., Mediterranean Sea, 36.5°N 28.2°E"
          />
        </View>

        <View style={styles.formGroup}>
          <Text style={styles.label}>Notes</Text>
          <TextInput
            style={[styles.input, styles.textArea]}
            value={notes}
            onChangeText={setNotes}
            placeholder="Additional observations, size, conditions, etc."
            multiline
            numberOfLines={4}
          />
        </View>

        <TouchableOpacity
          style={[styles.submitButton, submitting && styles.submitButtonDisabled]}
          onPress={handleSubmit}
          disabled={submitting}
        >
          <Text style={styles.submitButtonText}>
            {submitting ? 'Submitting...' : 'Submit Catch'}
          </Text>
        </TouchableOpacity>

        {syncStatus === 'offline' && (
          <View style={styles.offlineNotice}>
            <Text style={styles.offlineText}>
              📡 Offline Mode - Data will sync when connection is restored
            </Text>
          </View>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafffa',
  },
  imageContainer: {
    backgroundColor: '#e8f5e8',
    padding: 20,
    borderBottomWidth: 3,
    borderBottomColor: '#d4f1d4',
  },
  image: {
    width: '100%',
    height: 250,
    resizeMode: 'contain',
    borderWidth: 2,
    borderColor: '#b8e6b8',
  },
  form: {
    padding: 20,
  },
  formGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a3a1a',
    marginBottom: 8,
  },
  optional: {
    fontSize: 12,
    fontWeight: 'normal',
    color: '#2d5a2d',
  },
  input: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderColor: '#b8e6b8',
    padding: 12,
    fontSize: 16,
    color: '#1a3a1a',
  },
  textArea: {
    height: 100,
    textAlignVertical: 'top',
  },
  submitButton: {
    backgroundColor: '#b8e6b8',
    padding: 18,
    borderWidth: 3,
    borderColor: '#7cb87c',
    marginTop: 10,
  },
  submitButtonDisabled: {
    opacity: 0.5,
  },
  submitButtonText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1a3a1a',
    textAlign: 'center',
  },
  offlineNotice: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#fff4e6',
    borderWidth: 2,
    borderColor: '#ffd699',
  },
  offlineText: {
    fontSize: 14,
    color: '#663c00',
    textAlign: 'center',
  },
});

import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, Image, TouchableOpacity, RefreshControl } from 'react-native';
import { useDatabase } from '../context/DatabaseContext';

export default function DatabaseScreen() {
  const { getAllCatches, syncPendingCatches, syncStatus } = useDatabase();
  const [catches, setCatches] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadCatches();
  }, []);

  const loadCatches = async () => {
    const data = await getAllCatches();
    setCatches(data);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await syncPendingCatches();
    await loadCatches();
    setRefreshing(false);
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <Image source={{ uri: item.photo_uri }} style={styles.cardImage} />
      <View style={styles.cardContent}>
        <Text style={styles.species}>{item.species}</Text>
        {item.fisher_name ? (
          <Text style={styles.info}>By: {item.fisher_name}</Text>
        ) : null}
        {item.location ? (
          <Text style={styles.info}>Location: {item.location}</Text>
        ) : null}
        {item.notes ? (
          <Text style={styles.notes}>{item.notes}</Text>
        ) : null}
        <Text style={styles.date}>{formatDate(item.timestamp)}</Text>
        <View style={styles.syncBadge}>
          <Text style={[styles.syncText, item.synced ? styles.synced : styles.notSynced]}>
            {item.synced ? '✓ Synced' : '⏳ Pending sync'}
          </Text>
        </View>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerText}>
          {catches.length} {catches.length === 1 ? 'catch' : 'catches'} logged
        </Text>
        {syncStatus && (
          <Text style={styles.syncStatus}>
            Status: {syncStatus}
          </Text>
        )}
      </View>

      <FlatList
        data={catches}
        renderItem={renderItem}
        keyExtractor={item => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={['#b8e6b8']}
            tintColor="#b8e6b8"
          />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No catches yet</Text>
            <Text style={styles.emptySubtext}>Start by taking a photo</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fafffa',
  },
  header: {
    backgroundColor: '#e8f5e8',
    padding: 15,
    borderBottomWidth: 3,
    borderBottomColor: '#d4f1d4',
  },
  headerText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1a3a1a',
  },
  syncStatus: {
    fontSize: 14,
    color: '#2d5a2d',
    marginTop: 5,
  },
  list: {
    padding: 15,
  },
  card: {
    backgroundColor: '#e8f5e8',
    borderWidth: 3,
    borderColor: '#d4f1d4',
    marginBottom: 15,
  },
  cardImage: {
    width: '100%',
    height: 200,
    resizeMode: 'cover',
    borderBottomWidth: 2,
    borderBottomColor: '#b8e6b8',
  },
  cardContent: {
    padding: 15,
  },
  species: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1a3a1a',
    marginBottom: 8,
  },
  info: {
    fontSize: 14,
    color: '#2d5a2d',
    marginBottom: 4,
  },
  notes: {
    fontSize: 14,
    color: '#2d5a2d',
    marginTop: 8,
    marginBottom: 8,
    fontStyle: 'italic',
  },
  date: {
    fontSize: 12,
    color: '#5a7a5a',
    marginTop: 8,
  },
  syncBadge: {
    marginTop: 10,
  },
  syncText: {
    fontSize: 12,
    fontWeight: '600',
  },
  synced: {
    color: '#2d5a2d',
  },
  notSynced: {
    color: '#996600',
  },
  emptyContainer: {
    padding: 60,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    color: '#2d5a2d',
    marginBottom: 10,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#5a7a5a',
  },
});

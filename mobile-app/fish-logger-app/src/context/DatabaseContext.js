import React, { createContext, useContext, useState, useEffect } from 'react';
import * as SQLite from 'expo-sqlite';
import * as Network from 'expo-network';
import axios from 'axios';

const DatabaseContext = createContext();

const SERVER_URL = 'http://100.118.217.22:5000';

export const DatabaseProvider = ({ children }) => {
  const [db, setDb] = useState(null);
  const [syncStatus, setSyncStatus] = useState('idle');

  useEffect(() => {
    initDatabase();
  }, []);

  const initDatabase = async () => {
    const database = await SQLite.openDatabaseAsync('fishlogger.db');
    
    await database.execAsync(`
      CREATE TABLE IF NOT EXISTS catches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        photo_uri TEXT NOT NULL,
        species TEXT DEFAULT 'Unknown',
        location TEXT,
        notes TEXT,
        fisher_name TEXT,
        timestamp INTEGER NOT NULL,
        synced INTEGER DEFAULT 0
      );
    `);

    setDb(database);
  };

  const addCatch = async (catchData) => {
    if (!db) return;
    
    const result = await db.runAsync(
      `INSERT INTO catches (photo_uri, species, location, notes, fisher_name, timestamp, synced) 
       VALUES (?, ?, ?, ?, ?, ?, 0)`,
      [
        catchData.photo_uri,
        catchData.species || 'Unknown',
        catchData.location || '',
        catchData.notes || '',
        catchData.fisher_name || '',
        Date.now()
      ]
    );

    // Try to sync immediately if online
    syncPendingCatches();

    return result.lastInsertRowId;
  };

  const getAllCatches = async () => {
    if (!db) return [];
    
    const catches = await db.getAllAsync(
      'SELECT * FROM catches ORDER BY timestamp DESC'
    );
    
    return catches;
  };

  const syncPendingCatches = async () => {
    if (!db) return;

    const networkState = await Network.getNetworkStateAsync();
    if (!networkState.isConnected) {
      setSyncStatus('offline');
      return;
    }

    setSyncStatus('syncing');

    try {
      const unsyncedCatches = await db.getAllAsync(
        'SELECT * FROM catches WHERE synced = 0'
      );

      for (const catchData of unsyncedCatches) {
        const formData = new FormData();
        formData.append('fish_image', {
          uri: catchData.photo_uri,
          type: 'image/jpeg',
          name: `catch_${catchData.id}.jpg`
        });
        formData.append('species_label', catchData.species);
        formData.append('location', catchData.location);
        formData.append('notes', catchData.notes);
        formData.append('uploader_name', catchData.fisher_name);

        await axios.post(`${SERVER_URL}/api/submit`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        await db.runAsync(
          'UPDATE catches SET synced = 1 WHERE id = ?',
          [catchData.id]
        );
      }

      setSyncStatus('synced');
    } catch (error) {
      console.error('Sync error:', error);
      setSyncStatus('error');
    }
  };

  const downloadDatabase = async () => {
    try {
      const response = await axios.get(`${SERVER_URL}/api/database`);
      return response.data;
    } catch (error) {
      console.error('Download error:', error);
      return [];
    }
  };

  return (
    <DatabaseContext.Provider 
      value={{ 
        db, 
        addCatch, 
        getAllCatches, 
        syncPendingCatches, 
        downloadDatabase,
        syncStatus 
      }}
    >
      {children}
    </DatabaseContext.Provider>
  );
};

export const useDatabase = () => useContext(DatabaseContext);

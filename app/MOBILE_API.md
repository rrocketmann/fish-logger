# Marine Species ID - Mobile App API

## API Endpoints

### Submit Catch (Mobile App)
```
POST /api/submit
Content-Type: multipart/form-data

Parameters:
- fish_image: image file (required)
- species_label: string (optional, defaults to "Unknown")
- uploader_name: string (required)
- location: string (optional)
- notes: string (optional)

Response:
{
  "success": true,
  "id": 123,
  "message": "Catch data submitted successfully"
}
```

### Get Database
```
GET /api/database

Response:
{
  "count": 150,
  "entries": [
    {
      "id": 123,
      "species": "Trout",
      "submitted_by": "John Fisher",
      "location": "Lake Michigan",
      "notes": "Caught at 20ft depth",
      "date": "2026-03-28T12:00:00",
      "likes": 5,
      "image": "20260328_120000_trout.jpg"
    },
    ...
  ]
}
```

## Mobile App Workflow

### Offline Mode
1. User takes photo of catch
2. Fills in species (if known), location, notes
3. App stores data locally (SQLite/JSON)
4. Shows "Queued for sync" message

### Online Sync
1. App detects network connection
2. Reads queued entries from local storage
3. POSTs each entry to /api/submit
4. Marks as synced on success
5. Shows sync status to user

### Download Database
1. User can download full database as JSON or CSV
2. Available at /export/json or /export/csv
3. For offline analysis by researchers

## Example Mobile App Code (React Native)

```javascript
// Store catch offline
const storeCatchOffline = async (catchData) => {
  const queue = await AsyncStorage.getItem('catchQueue') || '[]';
  const catches = JSON.parse(queue);
  catches.push({
    ...catchData,
    id: Date.now(),
    synced: false
  });
  await AsyncStorage.setItem('catchQueue', JSON.stringify(catches));
};

// Sync when online
const syncCatches = async () => {
  const queue = await AsyncStorage.getItem('catchQueue') || '[]';
  const catches = JSON.parse(queue);
  
  for (const catchData of catches) {
    if (!catchData.synced) {
      try {
        const formData = new FormData();
        formData.append('fish_image', catchData.image);
        formData.append('species_label', catchData.species);
        formData.append('uploader_name', catchData.name);
        formData.append('location', catchData.location);
        formData.append('notes', catchData.notes);
        
        const response = await fetch('http://server/api/submit', {
          method: 'POST',
          body: formData
        });
        
        if (response.ok) {
          catchData.synced = true;
        }
      } catch (error) {
        console.log('Sync failed, will retry later');
      }
    }
  }
  
  // Save updated queue
  await AsyncStorage.setItem('catchQueue', JSON.stringify(catches));
};
```

## Database Export Formats

### JSON Export
- Full database with metadata
- Includes all fields
- Easy to parse programmatically

### CSV Export
- Spreadsheet-compatible
- For analysis in Excel/Google Sheets
- Includes: ID, Species, Submitted By, Location, Notes, Date, Likes, Image

## Security Notes

For production mobile app:
1. Add API authentication (JWT tokens)
2. Rate limiting on endpoints
3. HTTPS only
4. Validate all inputs
5. Sanitize file uploads

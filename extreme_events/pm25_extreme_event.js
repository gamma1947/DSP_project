const fs = require('fs');
const csv = require('csv-parser');

const inputFile = 'hourly_resampled_o3.csv';

// ==========================================
// ENTER YOUR POLLUTANT RANGE VALUE HERE
// ==========================================
// For O3, anything > 100 is "Moderate/Poor" 
// Change this number for other pollutants!
const POLLUTANT_LIMIT = 100; 
// ==========================================

async function findAbnormalLocations() {
    const abnormalLocations = new Set(); // Using a Set to avoid duplicates

    console.log(`Scanning for locations where pollutant value > ${POLLUTANT_LIMIT}...`);

    await new Promise((resolve, reject) => {
        fs.createReadStream(inputFile)
            .pipe(csv())
            .on('data', (row) => {
                const value = parseFloat(row.value);
                const locationId = row.location_id;

                // Check if the reading is beyond the normal limit
                if (!isNaN(value) && value > POLLUTANT_LIMIT) {
                    abnormalLocations.add(locationId);
                }
            })
            .on('end', resolve)
            .on('error', reject);
    });

    // Convert Set to an Array so we can print it easily
    const locationArray = Array.from(abnormalLocations);

    console.log('\n--- Results ---');
    console.log(`Found ${locationArray.length} unique location IDs beyond the limit:`);
    console.log(locationArray);
}

// Execute the function
findAbnormalLocations().catch(console.error);
import Dexie from "dexie";

export const db = new Dexie("VitalPawsDB");

db.version(1).stores({
    pets: "++id, name, type, breed, photo"
});

// Added recordings table
db.version(2).stores({
    recordings: "++id, petId, date, records"
});


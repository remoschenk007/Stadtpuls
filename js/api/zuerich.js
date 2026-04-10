/* ═══════════════════════════════════════════════════════════
   STADTPULS — Zürich Tourismus API
   js/api/zuerich.js
   © 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

const ZuerichAPI = {

  BASE_URL: 'https://www.zuerich.com/en/api/v2/data',

  async fetchAll() {
    try {
      const response = await fetch(ZuerichAPI.BASE_URL);
      if (!response.ok) throw new Error(`API Fehler: ${response.status}`);
      const data = await response.json();
      console.log(`✅ Zürich API: ${data.length} Einträge geladen`);
      return data;
    } catch (err) {
      console.error('❌ Zürich API Fehler:', err);
      return [];
    }
  },

  mapKategorie(categories) {
    const c = categories.map(k => k.toLowerCase());
    if (c.some(k => k.includes('restaurant') || k.includes('gastro') || k.includes('café'))) return 'gastro';
    if (c.some(k => k.includes('event') || k.includes('konzert') || k.includes('festival'))) return 'events';
    if (c.some(k => k.includes('club') || k.includes('bar') || k.includes('nightlife'))) return 'nachtleben';
    if (c.some(k => k.includes('shop') || k.includes('store') || k.includes('laden'))) return 'shopping';
    return 'sonstige';
  },

  mapToLocation(item) {
    return {
      name:         item.name?.de || item.name || '',
      beschreibung: item.disambiguatingDescription?.de || '',
      kategorie:    ZuerichAPI.mapKategorie(item.category || []),
      subkategorie: item.category?.[1] || '',
      adresse:      item.address?.streetAddress || '',
      plz:          item.address?.postalCode || '',
      lat:          item.geo?.latitude || null,
      lng:          item.geo?.longitude || null,
      quelle:       'zuerich-tourismus',
      aktiv:        true
    };
  },

  async getLocations() {
    const raw = await ZuerichAPI.fetchAll();
    return raw.map(ZuerichAPI.mapToLocation);
  }

};

export default ZuerichAPI;

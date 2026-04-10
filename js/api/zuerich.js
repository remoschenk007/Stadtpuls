/* ═══════════════════════════════════════════════════════════
   STADTPULS — Zürich Tourismus API
   js/api/zuerich.js
   © 2026 by raimondo*
═══════════════════════════════════════════════════════════ */

const ZuerichAPI = {

  BASE_URL: 'https://www.zuerich.com/en/api/v2/data?id=100',

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

  mapKategorie(type, categories) {
    const t = (type || '').toLowerCase();
    const c = (categories || []).map(k => k.toLowerCase());
    if (t.includes('bar') || t.includes('pub') || c.some(k => k.includes('nightlife') || k.includes('club'))) return 'nachtleben';
    if (t.includes('localbusiness') || c.some(k => k.includes('restaurant') || k.includes('gastro') || k.includes('café') || k.includes('cafe'))) return 'gastro';
    if (c.some(k => k.includes('event') || k.includes('konzert') || k.includes('festival'))) return 'events';
    if (c.some(k => k.includes('shop') || k.includes('store') || k.includes('laden'))) return 'shopping';
    return 'gastro';
  },

  mapSubkategorie(categories) {
    const c = (categories || []).map(k => k.toLowerCase());
    if (c.some(k => k.includes('asian'))) return 'asiatisch';
    if (c.some(k => k.includes('italian'))) return 'italienisch';
    if (c.some(k => k.includes('swiss'))) return 'schweizer';
    if (c.some(k => k.includes('vegetarian') || k.includes('vegan'))) return 'vegisch';
    if (c.some(k => k.includes('bar') || k.includes('cocktail'))) return 'bar';
    if (c.some(k => k.includes('brunch') || k.includes('breakfast'))) return 'brunch';
    if (c.some(k => k.includes('american'))) return 'amerikanisch';
    if (c.some(k => k.includes('mediterranean'))) return 'mediterran';
    return 'international';
  },

  mapToLocation(item) {
    const categories = Object.keys(item.category || {});
    return {
      name:         item.name?.de || item.name?.en || '',
      beschreibung: item.disambiguatingDescription?.de || item.disambiguatingDescription?.en || '',
      kategorie:    ZuerichAPI.mapKategorie(item['@type'], categories),
      subkategorie: ZuerichAPI.mapSubkategorie(categories),
      adresse:      item.address?.streetAddress || '',
      plz:          item.address?.postalCode || '',
      lat:          item.geo?.latitude || null,
      lng:          item.geo?.longitude || null,
      slug:         item.identifier || '',
      quelle:       'zuerich-tourismus',
      aktiv:        true
    };
  },

  async getLocations() {
    const raw = await ZuerichAPI.fetchAll();
    return raw.map(ZuerichAPI.mapToLocation);
  },

  async getGastro() {
    const all = await ZuerichAPI.getLocations();
    return all.filter(l => l.kategorie === 'gastro');
  },

  async getNachtleben() {
    const all = await ZuerichAPI.getLocations();
    return all.filter(l => l.kategorie === 'nachtleben');
  }

};

export default ZuerichAPI;

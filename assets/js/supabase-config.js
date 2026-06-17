// Fase 3: configurare SUPABASE_URL e SUPABASE_ANON_KEY per sync diario
window.TVSupabase = {
  url: '',
  anonKey: '',
  async sync(entries) {
    if (!this.url || !this.anonKey) {
      console.info('Supabase non configurato. Export JSON disponibile.');
      return false;
    }
    // Placeholder per integrazione @supabase/supabase-js
    console.info('Sync diario:', entries.length, 'entries');
    return true;
  },
};

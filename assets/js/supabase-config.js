// Config Supabase per sync opzionale del diario (chiave publishable = pubblica, protetta da RLS)
window.TVSupabase = {
  url: 'https://skpnogasbwvewwzouawm.supabase.co',
  anonKey: 'sb_publishable_-Y-tRo3L_7XVZnK-arvvUg_Y12JBknG',
  _client: null,

  isConfigured() {
    return Boolean(this.url && this.anonKey);
  },

  getClient() {
    if (!this.isConfigured()) return null;
    if (!window.supabase?.createClient) return null;
    if (!this._client) {
      this._client = window.supabase.createClient(this.url, this.anonKey);
    }
    return this._client;
  },

  async ensureSession() {
    const client = this.getClient();
    if (!client) return null;
    const { data: existing } = await client.auth.getSession();
    if (existing.session) return existing.session;
    const { data, error } = await client.auth.signInAnonymously();
    if (error) throw error;
    return data.session;
  },

  entryToRow(entry, userId) {
    return {
      user_id: userId,
      client_id: entry.id,
      varieta: entry.varieta ?? entry.varietà ?? '',
      temp: entry.temp ? Number(entry.temp) : null,
      grams: entry.grams ? Number(entry.grams) : null,
      seconds: entry.seconds ? Number(entry.seconds) : null,
      note: entry.note || '',
      tags: Array.isArray(entry.tags) ? entry.tags : [],
      momento: entry.momento || null,
      season: entry.season || null,
      created_at: entry.date || new Date().toISOString(),
    };
  },

  async sync(entries) {
    if (!this.isConfigured()) {
      return { ok: false, reason: 'not_configured' };
    }
    const client = this.getClient();
    if (!client) {
      return { ok: false, reason: 'library_missing' };
    }
    try {
      const session = await this.ensureSession();
      if (!session?.user) {
        return { ok: false, reason: 'auth_failed' };
      }
      if (!entries.length) {
        return { ok: true, synced: 0 };
      }
      const rows = entries.map((entry) => this.entryToRow(entry, session.user.id));
      const { error } = await client.from('infusioni').upsert(rows, {
        onConflict: 'user_id,client_id',
      });
      if (error) throw error;
      return { ok: true, synced: entries.length };
    } catch (err) {
      console.error('Supabase sync failed', err);
      const message = err.message || '';
      if (message.includes('Anonymous sign-ins are disabled')) {
        return { ok: false, reason: 'anonymous_disabled' };
      }
      return { ok: false, reason: 'error', message };
    }
  },
};

// ============================================
// STADTPULS — Supabase Client
// js/supabase.js
// © 2026 by raimondo*
// ============================================

import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL = 'https://pnynkzrqnfoshojqfqxn.supabase.co'
const SUPABASE_KEY = 'sb_publishable_T8XzRIhQymVgGn2sqZPdpA_LK0a_iyH'

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)


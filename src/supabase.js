// src/supabase.js
import { createClient } from '@supabase/supabase-js'

// 1. 这里填你截图里的 Project URL
const supabaseUrl = 'https://hvsmloywzdlvegjfvyss.supabase.co'

// 2. 这里填你截图里的 anon public Key (注意：是那个能在浏览器用的 public key，不是 service_role！)
const supabaseKey = 'sb_publishable_IiQz8uVag4DG2ue1HJlHww_PjIM4Oje'
export const supabase = createClient(supabaseUrl, supabaseKey)
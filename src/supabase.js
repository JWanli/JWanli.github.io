// src/supabase.js
import { createClient } from '@supabase/supabase-js'

// 1. 这里填你截图里的 Project URL
const supabaseUrl = 'https://hvsmloywzdlvegjfvyss.supabase.co'

// 2. 这里填你截图里的 anon public Key (注意：是那个能在浏览器用的 public key，不是 service_role！)
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2c21sb3l3emRsdmVnamZ2eXNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc5NDI4NTcsImV4cCI6MjA4MzUxODg1N30.AUDMSS7QCFnn6A9XzYK1lnDhZ7Mu1hV6YNdAfWtjMhI' 
// (请把你截图里完整的 anon key 复制进去，截图里显示不全，要去网页后台点 Copy)

export const supabase = createClient(supabaseUrl, supabaseKey)
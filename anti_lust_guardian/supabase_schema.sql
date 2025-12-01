-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  current_streak INT DEFAULT 0,
  longest_streak INT DEFAULT 0,
  purpose_statement TEXT
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own data
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own data" ON users
  FOR INSERT WITH CHECK (auth.uid() = id);

-----------------------------------

-- Subscriptions table
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  stripe_subscription_id TEXT UNIQUE,
  stripe_customer_id TEXT,
  plan_type TEXT NOT NULL CHECK (plan_type IN ('monthly', 'yearly', 'lifetime')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'canceled', 'past_due', 'trialing')),
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only view their own subscriptions
CREATE POLICY "Users can view own subscriptions" ON subscriptions
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "System can manage subscriptions" ON subscriptions
  FOR ALL USING (true);

-----------------------------------

-- Devices table
CREATE TABLE devices (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  device_name TEXT,
  platform TEXT CHECK (platform IN ('android', 'ios', 'windows', 'macos', 'linux')),
  device_id TEXT UNIQUE NOT NULL,
  last_sync TIMESTAMP DEFAULT NOW(),
  protection_level TEXT DEFAULT 'high' CHECK (protection_level IN ('low', 'medium', 'high', 'maximum')),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE devices ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own devices
CREATE POLICY "Users can view own devices" ON devices
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own devices" ON devices
  FOR ALL USING (auth.uid() = user_id);

-----------------------------------

-- Threats table (global threat intelligence)
CREATE TABLE threats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  url TEXT NOT NULL,
  domain TEXT NOT NULL,
  risk_score FLOAT CHECK (risk_score BETWEEN 0 AND 1),
  category TEXT,
  source TEXT CHECK (source IN ('safe_browsing', 'user_report', 'ai_classifier', 'manual')),
  active BOOLEAN DEFAULT TRUE,
  added_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast URL lookups
CREATE INDEX idx_threats_url ON threats(url);
CREATE INDEX idx_threats_domain ON threats(domain);
CREATE INDEX idx_threats_active ON threats(active);

-- Enable Row Level Security (threats are globally viewable)
ALTER TABLE threats ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone authenticated can read threats
CREATE POLICY "Authenticated users can view threats" ON threats
  FOR SELECT USING (auth.role() = 'authenticated');

-----------------------------------

-- Block logs (track what was blocked for each user)
CREATE TABLE block_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE NOT NULL,
  device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  threat_id UUID REFERENCES threats(id),
  blocked_at TIMESTAMP DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE block_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only view their own block logs
CREATE POLICY "Users can view own block logs" ON block_logs
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "System can log blocks" ON block_logs
  FOR INSERT WITH CHECK (true);

-----------------------------------

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for auto-updating timestamps
CREATE TRIGGER update_users_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at
  BEFORE UPDATE ON subscriptions
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_threats_updated_at
  BEFORE UPDATE ON threats
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Reusable relational practice tables for public census and school datasets.
-- Import cleaned, licensed public CSVs into these tables before using the joins.
CREATE TABLE IF NOT EXISTS census (
  district_id TEXT PRIMARY KEY,
  population INTEGER NOT NULL CHECK (population >= 0),
  median_income NUMERIC
);
CREATE TABLE IF NOT EXISTS schools (
  school_id TEXT PRIMARY KEY,
  district_id TEXT NOT NULL REFERENCES census(district_id),
  school_name TEXT NOT NULL,
  school_type TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_schools_district ON schools(district_id);

-- Parameterized example (SQLite named parameters): :school_type
SELECT s.district_id, s.school_name, c.population, c.median_income
FROM schools AS s JOIN census AS c USING (district_id)
WHERE s.school_type = :school_type
ORDER BY c.population DESC;

-- Parameterized grouped flight reliability view: :year
SELECT origin, carrier, COUNT(*) AS flights,
       AVG(CASE WHEN cancelled = 1 THEN 1.0 ELSE 0.0 END) AS cancellation_rate,
       AVG(arr_delay) AS mean_arrival_delay
FROM flights WHERE year = :year
GROUP BY origin, carrier HAVING COUNT(*) >= 30
ORDER BY cancellation_rate DESC;

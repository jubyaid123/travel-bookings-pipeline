-- Cancellation rate by country
SELECT
  country,
  COUNT(*) AS bookings,
  AVG(is_canceled::int) AS cancellation_rate
FROM fact_bookings
GROUP BY country
ORDER BY cancellation_rate DESC;

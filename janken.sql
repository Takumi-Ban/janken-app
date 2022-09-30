SELECT
    username,
    COUNT(point = 1 or NULL) AS cor,
    COUNT(id) AS all
FROM results
GROUP BY username
ORDER BY COUNT(point = 1 or NULL) DESC;

SELECT username, COUNT(point = 1 or NULL) AS cor, COUNT(id) AS all FROM results GROUP BY username ORDER BY COUNT(point = 1 or NULL) DESC;
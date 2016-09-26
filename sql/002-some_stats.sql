DELETE FROM sources s WHERE s.domain = 'sabotin.ung.si';

SELECT * FROM sources s WHERE s.domain = 'dk.um.si';
-- and s.id = '191088d0-37b4-48d3-b26a-8d0c41123a90'::uuid;

UPDATE
	sources
SET files = ARRAY[replace(files[1], 'full/', '')];
-- WHERE sources.id = '191088d0-37b4-48d3-b26a-8d0c41123a90'::uuid;

-- SELECT id, ARRAY[replace(files[1], 'full/', '')] FROM sources WHERE sources.id = '191088d0-37b4-48d3-b26a-8d0c41123a90'::uuid;

SELECT
	domain,
	COUNT(*) as CNT
FROM
	sources
GROUP BY
	sources.domain
ORDER BY CNT DESC;

SELECT COUNT(*) FROM sources;
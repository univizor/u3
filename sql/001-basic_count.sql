SELECT 
	s.scraped_url,
	replace(s.files[1], 'full/', '')
FROM
	sources s;
	
SELECT
	COUNT(id)
FROM
	sources s;
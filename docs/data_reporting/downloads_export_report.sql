SELECT date_format(date_add('day', -1, current_date), '%e/%b/%Y') AS date, "object", COUNT("cloudfront_logs"."resource_downloads"."object") AS requests, 'Success' AS response_type
FROM "cloudfront_logs"."resource_downloads"
WHERE "cloudfront_logs"."resource_downloads"."datetime" LIKE concat('[', date_format(date_add('day', -1, current_date), '%e/%b/%Y'), '%')
        AND "cloudfront_logs"."resource_downloads"."object" LIKE 'documents/%'
        AND "cloudfront_logs"."resource_downloads"."method"='"GET'
        AND ("cloudfront_logs"."resource_downloads"."response_code" LIKE '2%'
        OR "cloudfront_logs"."resource_downloads"."response_code" LIKE '3%')
GROUP BY  "cloudfront_logs"."resource_downloads"."object"
UNION
SELECT date_format(date_add('day', -1, current_date), '%e/%b/%Y') AS date, "object", COUNT("cloudfront_logs"."resource_downloads"."object") AS requests, 'Error' AS response_type
FROM "cloudfront_logs"."resource_downloads"
WHERE "cloudfront_logs"."resource_downloads"."datetime" LIKE concat('[', date_format(date_add('day', -1, current_date), '%e/%b/%Y'), '%')
        AND "cloudfront_logs"."resource_downloads"."object" LIKE 'documents/%'
        AND "cloudfront_logs"."resource_downloads"."method"='"GET'
        AND ("cloudfront_logs"."resource_downloads"."response_code" LIKE '4%'
        OR "cloudfront_logs"."resource_downloads"."response_code" LIKE '5%')
GROUP BY  "cloudfront_logs"."resource_downloads"."object"
ORDER BY  "object"
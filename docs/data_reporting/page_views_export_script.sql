SELECT '{{report date}}' AS date, "path", COUNT("cloudfront_logs"."page_views"."path") AS requests, 'Success' AS response_type
FROM "cloudfront_logs"."page_views"
WHERE "cloudfront_logs"."page_views"."datetime" LIKE '[{{report date}}%'
        AND "cloudfront_logs"."page_views"."method"='"GET'
        AND ("cloudfront_logs"."page_views"."response_code" LIKE '2%'
        OR "cloudfront_logs"."page_views"."response_code" LIKE '3%')
GROUP BY  "cloudfront_logs"."page_views"."path"
UNION
SELECT '{{report date}}' AS date, "path", COUNT("cloudfront_logs"."page_views"."path") AS requests, 'Error' AS response_type
FROM "cloudfront_logs"."page_views"
WHERE "cloudfront_logs"."page_views"."datetime" LIKE '[{{report date}}%'
        AND "cloudfront_logs"."page_views"."method"='"GET'
        AND ("cloudfront_logs"."page_views"."response_code" LIKE '4%'
        OR "cloudfront_logs"."page_views"."response_code" LIKE '5%')
GROUP BY  "cloudfront_logs"."page_views"."path"
ORDER BY  "path"
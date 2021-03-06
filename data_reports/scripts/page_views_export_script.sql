SELECT date_format(date_add('day', -1, current_date), '%d/%b/%Y') AS date, "path", COUNT("cloudfront_logs"."new_page_views"."path") AS requests, 'Success' AS response_type
FROM "cloudfront_logs"."new_page_views"
WHERE "cloudfront_logs"."new_page_views"."datetime" LIKE concat('[', date_format(date_add('day', -1, current_date), '%d/%b/%Y'), '%')
        AND "cloudfront_logs"."new_page_views"."method"='"GET'
        AND ("cloudfront_logs"."new_page_views"."response_code" LIKE '2%'
        OR "cloudfront_logs"."new_page_views"."response_code" LIKE '3%')
GROUP BY  "cloudfront_logs"."new_page_views"."path"
UNION
SELECT date_format(date_add('day', -1, current_date), '%d/%b/%Y') AS date, "path", COUNT("cloudfront_logs"."new_page_views"."path") AS requests, 'Error' AS response_type
FROM "cloudfront_logs"."new_page_views"
WHERE "cloudfront_logs"."new_page_views"."datetime" LIKE concat('[', date_format(date_add('day', -1, current_date), '%d/%b/%Y'), '%')
        AND "cloudfront_logs"."new_page_views"."method"='"GET'
        AND ("cloudfront_logs"."new_page_views"."response_code" LIKE '4%'
        OR "cloudfront_logs"."new_page_views"."response_code" LIKE '5%')
GROUP BY  "cloudfront_logs"."new_page_views"."path"
ORDER BY  "path"
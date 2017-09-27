SELECT s.site_id, s.user_id, group4.site_area_id, group4.design_id, group4.cpm
FROM (
    SELECT group3.*, a.parent_id
    FROM (
        SELECT group1.*
        FROM (
            SELECT d.site_area_id, c.cpm, c.design_id
            FROM (
                SELECT design_id,  MAX(partner_gain/view_count*1000) cpm
                FROM stat_design_cache
                GROUP BY design_id
            ) c
                JOIN site_area_design_1 d
                  ON d.site_area_design_1_id = c.design_id
            WHERE c.cpm > 0
        ) group1
            LEFT JOIN (
                SELECT d.site_area_id, c.cpm, c.design_id
                FROM (
                    SELECT design_id,  MAX(partner_gain/view_count*1000) cpm
                    FROM stat_design_cache
                    GROUP BY design_id
                ) c
                    JOIN site_area_design_1 d
                      ON d.site_area_design_1_id = c.design_id
            ) group2
              ON group1.site_area_id = group2.site_area_id AND group1.cpm < group2.cpm
        WHERE group2.cpm is NULL
    ) group3
        JOIN site_area a USING(site_area_id)
) group4
    JOIN site s
      ON group4.parent_id = s.site_id

-- Menu Items per Restaurant View
CREATE VIEW menu_items_per_restaurant AS
SELECT 
    r.name as restaurant_name,
    COUNT(mi.item_id) as total_items,
    AVG(mi.price) as average_price
FROM menu_app_restaurant r
JOIN menu_app_menu m ON r.restaurant_id = m.restaurant_id
JOIN menu_app_menusection ms ON m.menu_id = ms.menu_id
JOIN menu_app_menuitem mi ON ms.section_id = mi.section_id
GROUP BY r.restaurant_id, r.name;

-- Dietary Restrictions Distribution View
CREATE VIEW dietary_restrictions_distribution AS
SELECT 
    dr.label as restriction_type,
    COUNT(mi.item_id) as item_count,
    COUNT(mi.item_id) * 100.0 / (SELECT COUNT(*) FROM menu_app_menuitem) as percentage
FROM menu_app_dietaryrestriction dr
LEFT JOIN menu_app_menuitem mi ON dr.restriction_id = mi.dietary_restriction_id
GROUP BY dr.restriction_id, dr.label;

-- Price Analysis View
CREATE VIEW price_analysis_per_restaurant AS
SELECT 
    r.name as restaurant_name,
    MIN(mi.price) as min_price,
    MAX(mi.price) as max_price,
    AVG(mi.price) as avg_price
FROM menu_app_restaurant r
JOIN menu_app_menu m ON r.restaurant_id = m.restaurant_id
JOIN menu_app_menusection ms ON m.menu_id = ms.menu_id
JOIN menu_app_menuitem mi ON ms.section_id = mi.section_id
GROUP BY r.restaurant_id, r.name;
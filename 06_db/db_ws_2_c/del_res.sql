
DELETE FROM menus
WHERE item_name = 'Salmon Nigiri'



DELETE FROM menus
WHERE restaurant_id = (
    SELECT id
    FROM restaurants
    WHERE name = 'Pasta Paradise'
);


DELETE FROM restaurants
WHERE name = 'Pasta Paradise';
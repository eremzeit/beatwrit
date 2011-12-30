use beatwrit;


DROP TABLE IF exists main_writ_sort_views_today;
DROP TABLE IF exists main_writ_sort_views_week;
DROP TABLE IF exists main_writ_sort_views_month;
DROP TABLE IF exists main_writ_sort_views_year;

DROP TABLE IF exists main_writ_sort_nods_today;
DROP TABLE IF exists main_writ_sort_nods_week;
DROP TABLE IF exists main_writ_sort_nods_month;
DROP TABLE IF exists main_writ_sort_nods_year;

DROP TABLE IF exists main_addition_sort_nods_today;
DROP TABLE IF exists main_addition_sort_nods_week;
DROP TABLE IF exists main_addition_sort_nods_month;
DROP TABLE IF exists main_addition_sort_nods_year;

DROP TABLE IF exists main_user_sort_nods;



main_writ_sort_views_today;
DROP TABLE IF NOT exists main_writ_sort_views_week LIKE main_writ;
DROP TABLE IF NOT exists main_writ_sort_views_month LIKE main_writ;
DROP TABLE IF NOT exists main_writ_sort_views_year LIKE main_writ;

DROP TABLE IF NOT exists main_writ_sort_nods_today LIKE main_writ;
DROP TABLE IF NOT exists main_writ_sort_nods_week LIKE main_writ;
DROP TABLE IF NOT exists main_writ_sort_nods_month LIKE main_writ;
DROP TABLE IF NOT exists main_writ_sort_nods_year LIKE main_writ;

DROP TABLE IF NOT exists main_addition_sort_nods_today LIKE main_addition;
DROP TABLE IF NOT exists main_addition_sort_nods_week LIKE main_addition;
DROP TABLE IF NOT exists main_addition_sort_nods_month LIKE main_addition;
DROP TABLE IF NOT exists main_addition_sort_nods_year LIKE main_addition;

DROP TABLE IF NOT exists main_beatwrituser_sort_nods LIKE main_beatwrituser;

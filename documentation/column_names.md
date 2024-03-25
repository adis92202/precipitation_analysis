Original column names from used files had polish names with lots of special characters and whitespaces. They have all been mapped as following:

Precipitation data:
    "Kod stacji" -> "station_code"
    "Nazwa stacji" -> "station_name"
    "Rok" -> "year"
    "Miesiąc" -> "month" 
    "Dzień" -> "day"
    "Suma dobowa opadów w [mm]" -> "24h_precipitation_mm"
    "Status pomiaru SMDB" -> "SMDB_status"
    "Rodzaj opadu [S/W/ ]" -> "precip_type"
    "Wysokość pokrywy śnieżnej [cm]" -> "snow_cover_cm"
    "Status pomiaru PKSN" -> "PKSN_status"
    "Wysokość świeżospałego śniegu [cm]" -> "fresh_snow_cover_cm"
    "Status pomiaru HSS" -> "HSS_status"
    "Gatunek śniegu [kod]" -> "snow_type_code"
    "Status pomiaru GATS" -> "GATS_status"
    "Rodzaj pokrywy śnieżnej [kod]" -> "snow_cover_type_code"
    "Status pomiaru RPSN" -> "RPSN_status"
    

Stations data:
    "LP." -> "N"
    "ID" -> "ID"
    "Nazwa" -> "name"
    "Rzeka" -> "river"
    "Szerokość geograficzna" -> "lat"
    "Długość geograficzna" -> "lon"
    "Wysokość n.p.m." -> "altitude"

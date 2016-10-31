select *
from sensor
where event = 'temperature' and value = (SELECT min(value) FROM (select * from sensor where event = 'temperature'))


SELECT datetime(timestamp,'unixepoch', 'localtime')  FROM sensor
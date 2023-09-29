with temp as 
(SELECT account_id, CASE WHEN income > 50000 THEN 'High Salary' WHEN income >= 20000 THEN 'Average Salary' ELSE 'Low Salary' END AS Category FROM Accounts),

temp1 as
(select Category,count(*) as accounts_count from temp group by Category),
  
tu as
(SELECT CASE WHEN 'Average Salary' NOT IN (SELECT Category FROM temp1) THEN 'Average Salary' WHEN 'Low Salary' NOT IN (SELECT Category FROM temp1) THEN 'Low Salary' 
WHEN 'High Salary' NOT IN (SELECT Category FROM temp1) THEN 'High Salary' END AS Category, 0 AS count1),

pankaj as
(SELECT t1.*,t2.Category as Category1,t2.count1 FROM temp1 t1
RIGHT JOIN tu t2 ON t1.Category = t2.Category
UNION
SELECT t1.*,t2.Category as Category1,t2.count1 FROM temp1 t1
LEFT JOIN tu t2 ON t1.Category = t2.Category)

select * from (select case when Category is not Null then Category else Category1 end as Category, case when Category is not Null then accounts_count else count1 end as accounts_count from pankaj) j where Category is not NULL;





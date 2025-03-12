-- Q1

WITH each_ter_sale (TerritoryID  , total_sale) AS (
SELECT  soh.TerritoryID , avg(soh.TotalDue ) AS total_sale
FROM Sales.SalesOrderHeader  AS soh 
GROUP BY soh.TerritoryID
)
SELECT soh.SalesOrderID , soh.TerritoryID,soh.TotalDue ,
				(SELECT total_sale 
				FROM each_ter_sale AS ets 
				WHERE soh.TerritoryID = ets.TerritoryID ) AS total_sale_ter
FROM Sales.SalesOrderHeader   AS soh 
WHERE soh.TotalDue > (SELECT total_sale FROM each_ter_sale AS ets WHERE soh.TerritoryID = ets.TerritoryID );



--- 
-- Q2



SELECT 
	soh.SalesOrderID ,
    soh.SalesPersonID, 
    soh.OrderDate ,
    SUM(soh.TotalDue) OVER (PARTITION BY soh.SalesPersonID ORDER BY soh.OrderDate ROWS BETWEEN UNBOUNDED PRECEDING AND current row  ) AS running_sum
FROM Sales.SalesOrderHeader AS soh
ORDER BY soh.SalesPersonID DESC  , soh.OrderDate DESC 

-- Q3 
SELECT 
    p.ProductID,
    ps.ProductSubcategoryID,
    p.ListPrice, 
    RANK() OVER (PARTITION BY ps.ProductSubcategoryID ORDER BY p.ListPrice DESC) AS rnk,
    PERCENT_RANK() OVER (PARTITION BY ps.ProductSubcategoryID ORDER BY p.ListPrice DESC) AS prRANK,
    Dense_RANK() OVER (PARTITION BY ps.ProductSubcategoryID ORDER BY p.ListPrice DESC) AS densRANK
FROM Production.Product AS p
JOIN Production.ProductSubcategory AS ps 
    ON p.ProductSubcategoryID = ps.ProductSubcategoryID;


-- Q4 

SELECT soh.SalesPersonID , soh.TerritoryID , sum(soh.SubTotal) AS sum
FROM Sales.SalesOrderHeader  AS soh
GROUP BY GROUPING  SETS (
	soh.SalesPersonID ,
	soh.TerritoryID 
)
HAVING sum(soh.SubTotal)  <= 1000000 ;

-- Q5
-- a
SELECT  st.CountryRegionCode ,
sum(soh.TotalDue)AS t_sum ,
count(soh.TotalDue) AS t_count 
FROM Sales.SalesTerritory  AS st  JOIN Sales.SalesOrderHeader AS soh ON (soh.TerritoryID  = st.TerritoryID )
GROUP BY st.CountryRegionCode

-- b
WITH T AS (
SELECT  st.CountryRegionCode ,
sum(soh.TotalDue)AS t_sum ,
count(soh.TotalDue) AS t_count 
FROM Sales.SalesTerritory  AS st  JOIN Sales.SalesOrderHeader AS soh ON (soh.TerritoryID  = st.TerritoryID )
GROUP BY st.CountryRegionCode
)
SELECT  st.CountryRegionCode ,
sum(soh.TotalDue)AS t_sum ,
count(soh.TotalDue) AS t_count 
FROM Sales.SalesTerritory  AS st  JOIN Sales.SalesOrderHeader AS soh ON (soh.TerritoryID  = st.TerritoryID )
GROUP BY st.CountryRegionCode
HAVING sum(soh.TotalDue) < (SELECT avg(t_sum) FROM T) 




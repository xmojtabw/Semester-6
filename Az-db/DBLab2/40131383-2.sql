WITH t1 AS(
SELECT   st.Name ,sum(soh.TotalDue ) AS TotalSales  
FROM  Sales.SalesOrderHeader AS soh 
JOIN Sales.SalesTerritory AS st on(soh.TerritoryID = st.TerritoryID) 
GROUP  BY st.Name 
HAVING sum(soh.TotalDue ) < 10000000
)
SELECT  * , CASE  
			WHEN TotalSales > 8500000 THEN 'High sales'
			ELSE 'Low sales'
			END AS SalesCategory
FROM t1



----------------------------------


SELECT  c.CustomerID  , p.FirstName , p.LastName , count(soh.SalesOrderID) AS count ,  CASE 
																				WHEN sum(soh.TotalDue) IS NULL THEN 0
																				ELSE sum(soh.TotalDue)
																			END AS sum
FROM 
Sales.Customer  AS c
LEFT JOIN 
Sales.SalesOrderHeader  AS soh ON (c.CustomerID = soh.CustomerID)
LEFT JOIN 
Person.Person AS p on(c.PersonID = p.BusinessEntityID )
GROUP  BY c.CustomerID , p.FirstName  , p.LastName 



--------------------------------------------




WITH fhalf AS (
SELECT  p.ProductID , sum (soh.TotalDue) AS sum
FROM 
Sales.SalesOrderHeader  AS soh 
JOIN 
Sales.SalesOrderDetail  AS sod ON (soh.SalesOrderID = sod.SalesOrderID)
JOIN 
Production.Product  AS p  ON (sod.ProductID = p.ProductID)
WHERE (MONTH(soh.OrderDate) BETWEEN 1 AND 6 ) AND YEAR(soh.OrderDate) BETWEEN 2006 AND 2007 
GROUP  BY p.ProductID
),
shalf AS 
(
SELECT  p.ProductID , sum (soh.TotalDue) AS sum
FROM 
Sales.SalesOrderHeader  AS soh 
JOIN 
Sales.SalesOrderDetail  AS sod ON (soh.SalesOrderID = sod.SalesOrderID)
JOIN 
Production.Product  AS p  ON (sod.ProductID = p.ProductID)
WHERE (MONTH(soh.OrderDate) BETWEEN 7 AND 12 ) AND YEAR(soh.OrderDate) BETWEEN 2006 AND 2007 
GROUP  BY p.ProductID
)
SELECT  fh.ProductID , p.Name , CASE 
	WHEN fh.sum < sh.sum THEN 'Increased'
	else 'Decreased'
END AS SalesTrend
FROM 
fhalf AS fh
FULL OUTER JOIN 
shalf AS sh ON (fh.ProductID = sh.ProductID)
JOIN 
Production.Product AS p ON (p.ProductID = fh.ProductID) 
ORDER BY p.ProductID 

------------



CREATE TABLE  Farzi (
ID int ,
job varchar(20) CHECK ( job IN ('Teacher', 'Student', 'Manager')),
PRIMARY KEY (ID)
);

INSERT INTO Farzi (ID,job) VALUES (1, 'Teacher');
INSERT INTO Farzi (ID,job) VALUES (2 , 'Teacher');
INSERT INTO Farzi (ID,job) VALUES (12, 'Teacher');
INSERT INTO Farzi (ID,job) VALUES (123, 'Manager');
INSERT INTO Farzi (ID,job) VALUES (435, 'Manager');
INSERT INTO Farzi (ID,job) VALUES (433, 'Manager');
INSERT INTO Farzi (ID,job) VALUES (954, 'Manager');
INSERT INTO Farzi (ID,job) VALUES (543, 'Student');
INSERT INTO Farzi (ID,job) VALUES (544, 'Student');
INSERT INTO Farzi (ID,job) VALUES (68, 'Student');
INSERT INTO Farzi (ID,job) VALUES (678, 'Student');
INSERT INTO Farzi (ID,job) VALUES (670, 'Student');


SELECT  	sum(CASE WHEN job =  'Teacher' THEN 1 ELSE 0 end ) AS Teacher ,
			sum (CASE WHEN job = 'Manager' THEN 1 ELSE 0 END ) AS Manager, 
			sum (CASE WHEN job = 'Student' THEN 1 ELSE 0 end ) AS Student
FROM Farzi  

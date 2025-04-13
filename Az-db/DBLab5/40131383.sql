-- Q1


WITH T1 AS (
SELECT *
, ROW_NUMBER() OVER (PARTITION BY soh.SalesPersonID ORDER BY soh.OrderDate  ) AS r 
FROM Sales.SalesOrderHeader  AS soh 
WHERE soh.SalesPersonID IS NOT NULL 
)
SELECT SalesPersonID , SalesOrderID ,   OrderDate  , TotalDue  
FROM T1 
WHERE  r = 5
ORDER BY SalesPersonID 




-- Q2

SELECT 
    SalesPersonID, 
    ISNULL([2006], 0) AS [2006], 
    ISNULL([2007], 0) AS [2007], 
    ISNULL([2008], 0) AS [2008]
FROM
(
    SELECT SalesPersonID, YEAR(OrderDate) AS OrderYear, TotalDue
    FROM Sales.SalesOrderHeader
) AS SourceTable
PIVOT 
(
    SUM(TotalDue)
    FOR OrderYear IN ([2006], [2007], [2008])
) AS P;


-- Q3 

CREATE OR alter FUNCTION dbo.myfunc(@Customer_id int)
RETURNS varchar(40)
AS 
BEGIN 
	DECLARE @ret nvarchar(40);
	SELECT @ret = CONCAT('Client:',  
    CONCAT( UPPER(
	        	TRIM(
	        		REPLACE(TRANSLATE(p.FirstName, '0123456789', '          '), ' ', '')
	        		)
	        ),
       ' ',LOWER(
	        	TRIM(REPLACE(TRANSLATE(p.LastName, '0123456789', '          '), ' ', ''))
	       )
    	)
    )  
	FROM Person.Person AS p
	WHERE p.BusinessEntityID = @Customer_id
	IF (@ret IS null)
		SET @ret = 'Unknown'
	RETURN @ret
END;


SELECT dbo.myfunc(123123213); -- NOT exist

SELECT dbo.myfunc(953); -- exist

SELECT p.BusinessEntityID AS Customer_id , dbo.myfunc(p.BusinessEntityID) AS corrected_name
FROM Person.Person AS p
WHERE p.FirstName LIKE 'ma%' 






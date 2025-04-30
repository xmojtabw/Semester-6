
CREATE OR alter PROCEDURE Production.myproce
@year int 
AS 
SET NOCOUNT ON; 
WITH FavoriteProduct AS (
    SELECT 
        p.BusinessEntityID,
        MONTH(soh.OrderDate) AS ordermonth,
        sod.ProductID,
        COUNT(*) AS productcount,
        ROW_NUMBER() OVER (PARTITION BY p.BusinessEntityID, MONTH(soh.OrderDate) ORDER BY sum(sod.OrderQty) DESC,sod.ProductID  ASC) AS rn
    FROM Sales.Customer AS c
    JOIN Person.Person AS p ON c.PersonID = p.BusinessEntityID
    JOIN Sales.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID
    JOIN Sales.SalesOrderDetail AS sod ON soh.SalesOrderID = sod.SalesOrderID
    WHERE YEAR(soh.OrderDate) = @year
    GROUP BY p.BusinessEntityID, MONTH(soh.OrderDate), sod.ProductID
), t1 AS (
SELECT 
    p.BusinessEntityID  ,
    SUM(soh.TotalDue) AS TotalSum,
    MAX(soh.TotalDue) AS maxTotalDue,
    COUNT(soh.SalesOrderID) AS ordercount,
    MONTH(soh.OrderDate) AS ordermonth,
    fp.ProductID AS FavoriteProductID
FROM 
    Sales.Customer AS c 
JOIN Person.Person AS p ON c.PersonID = p.BusinessEntityID
JOIN Sales.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID
inner JOIN FavoriteProduct AS fp 
    ON fp.BusinessEntityID = p.BusinessEntityID 
    AND fp.ordermonth = MONTH(soh.OrderDate)
    AND fp.rn = 1
WHERE YEAR(soh.OrderDate) = @year  
GROUP BY p.BusinessEntityID   , MONTH(soh.OrderDate), fp.ProductID
) 
SELECT c.CustomerID,
	CONCAT(p.FirstName,' ',p.LastName) AS fullname,
	t1.ordermonth, 
	t1.ordercount,
	t1.TotalSum,
	t1.maxTotalDue,
	pr.Name
FROM 
t1 JOIN 
Sales.Customer AS c ON (c.PersonID = t1.BusinessEntityID ) 
JOIN 
Person.Person AS p ON (p.BusinessEntityID  = t1.BusinessEntityID )
JOIN 
Production.Product  AS pr ON (t1.FavoriteProductID  = pr.ProductID )
ORDER BY ordermonth ASC   , c.CustomerID ASC ;


EXECUTE Production.myproce 2008 ; 



-- Q2 -----


CREATE TABLE ProductsPriceHistory  (
	ProductionId int, 
	name NVARCHAR(255),
	ListPrice money ,
	StartDate datetime, 
	EndDate datetime , 
	CurrentFlag int
);

INSERT INTO ProductsPriceHistory
SELECT p.ProductID  , p.Name , p.ListPrice  , p.ModifiedDate , NULL , 1 
FROM Production.Product AS p;


SELECT * FROM ProductsPriceHistory ;


CREATE TRIGGER mytrigger
ON Production.Product
AFTER UPDATE
AS
BEGIN
    IF UPDATE(ListPrice)
    BEGIN
        UPDATE p
        SET EndDate = GETDATE(), CurrentFlag = 0
        FROM ProductsPriceHistory AS p
        INNER JOIN deleted AS d ON d.ProductID = p.ProductionId
        WHERE p.CurrentFlag = 1;

        INSERT INTO ProductsPriceHistory (ProductionId, name, ListPrice, StartDate, EndDate, CurrentFlag)
        SELECT pr.ProductID, pr.Name, pr.ListPrice, GETDATE(), NULL, 1
        FROM inserted AS pr;
    END
END;




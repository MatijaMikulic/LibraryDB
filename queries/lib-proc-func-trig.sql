CREATE PROCEDURE PRINT_LOAN_DETAILS @idmember INT
AS
 SELECT M.ID_M AS "ID member", M.FIRST_NAME AS "First name",
		M.LAST_NAME AS "Last name", C.ID_BOOK AS "ID book", C.TITLE AS "Book",
 	    L.DATE_LOAN AS "Date of loan", L.DATE_DEADLINE AS "Deadline",
		L.DATE_RETURN AS "Return date", L.DELAY_COST AS "Cost of delay"
 FROM LIB_MEMBER AS M, BOOK AS C, LOAN AS L
 WHERE M.ID_M=@idmember AND L.ID_M = M.ID_M AND L.ID_BOOK=C.ID_BOOK;

GO

CREATE PROCEDURE PRINT_MEMBERS_BY_NAME @name VARCHAR(40)
AS
	DECLARE @firstName VARCHAR(40), @lastName VARCHAR(40)
	SET @firstName = SUBSTRING(@name,1,CHARINDEX(' ',@name + ' ')-1)
	SET @lastName = SUBSTRING(@name,CHARINDEX(' ',@name + ' ')+1,LEN(@name))

	SELECT M.FIRST_NAME AS "First Name", M.LAST_NAME AS "Last Name",
		   M.DATE_OF_MEMBERSHIP AS "Date of Membership", M.DATE_OF_PAYMENT AS "Date of Payment",
		   M.TYPE_MEMBER AS "Type", M.PBR AS "Postal Code"
	FROM LIB_MEMBER AS M
	WHERE FIRST_NAME COLLATE Latin1_General_CI_AI  LIKE @firstName + '%' AND
		  LAST_NAME COLLATE Latin1_General_CI_AI LIKE @lastName + '%';

GO

CREATE PROCEDURE PRINT_MEMBERS_BY_NAME @name VARCHAR(40)
AS
	DECLARE @firstName VARCHAR(40), @lastName VARCHAR(40)
	SET @firstName = SUBSTRING(@name,1,CHARINDEX(' ',@name + ' ')-1)
	SET @lastName = SUBSTRING(@name,CHARINDEX(' ',@name + ' ')+1,LEN(@name))

	SELECT M.ID_M AS "ID",M.FIRST_NAME AS "First Name", M.LAST_NAME AS "Last Name",
		   M.DATE_OF_MEMBERSHIP AS "Date of Membership", M.DATE_OF_PAYMENT AS "Date of Payment",
		   M.TYPE_MEMBER AS "Type", M.PBR AS "Postal Code"
	FROM LIB_MEMBER AS M
	WHERE M.FIRST_NAME COLLATE Latin1_General_CI_AI  LIKE @firstName + '%' AND
		  M.LAST_NAME COLLATE Latin1_General_CI_AI LIKE @lastName + '%';

GO


CREATE PROCEDURE PRINT_AUTHOR_BY_NAME @name VARCHAR(40)
AS
	DECLARE @firstName VARCHAR(40), @lastName VARCHAR(40)
	SET @firstName = SUBSTRING(@name,1,CHARINDEX(' ',@name + ' ')-1)
	SET @lastName = SUBSTRING(@name,CHARINDEX(' ',@name + ' ')+1,LEN(@name))

	SELECT A.ID_AUTH AS "ID",A.FIRST_NAME AS "First Name", A.LAST_NAME AS "Last Name",
		   A.DATE_OF_BIRTH AS "Date of Birth", C.TITLE AS "Book"
	FROM AUTHOR AS A, BOOK AS C, WRITES AS W
	WHERE A.FIRST_NAME COLLATE Latin1_General_CI_AI  LIKE @firstName + '%' AND
		  A.LAST_NAME COLLATE Latin1_General_CI_AI LIKE @lastName + '%' AND
		  W.ID_AUTHOR = A.ID_AUTH AND W.ID_BOOK = C.ID_BOOK

GO

CREATE PROCEDURE PRINT_BOOK_BY_TITLE @title VARCHAR(20)
AS	
	SELECT C.ID_BOOK AS "ID", C.TITLE AS "Title", C.NUMBER_AVAILABLE AS "Available Number", C.PUBLISH_DATE AS "Date of Publish",
			C.NAME_TYPE AS "Type", CONCAT(A.FIRST_NAME,' ',A.LAST_NAME) AS "Author", P.PUB_NAME AS "Publisher"
	FROM BOOK AS C, WRITES AS W, AUTHOR AS A, PUBLISHER AS P
	WHERE C.TITLE COLLATE Latin1_General_CI_AI  LIKE @title + '%' AND
		 W.ID_BOOK = C.ID_BOOK AND W.ID_AUTHOR = A.ID_AUTH AND C.ID_PUBLISHER=P.ID_PUB
	
GO

CREATE PROCEDURE PRINT_MEMBERS_OF_TYPE @type CHAR(1)
AS
	SELECT M.ID_M AS "ID member", M.FIRST_NAME AS "First name",
			M.LAST_NAME AS "Last name", M.DATE_OF_PAYMENT AS "Date of payment",
			M.TYPE_MEMBER "Type", C.CITY_NAME AS "City"
	FROM LIB_MEMBER AS M, CITY AS C
	WHERE M.TYPE_MEMBER=@type AND M.PBR=C.PBR
	ORDER BY M.LAST_NAME ASC;


GO


CREATE PROCEDURE PRINT_BOOKS_OF_AUTHOR @idauthor INT
AS
	SELECT  A.ID_AUTH AS "ID author", A.FIRST_NAME +' '+ A.LAST_NAME AS "Author",
			C.ID_BOOK AS "ID book", C.TITLE AS "Book",
			C.NUMBER_AVAILABLE AS "Available number",
			YEAR(C.PUBLISH_DATE) AS "Year of publish",
			P.PUB_NAME as "Publisher", C.NAME_TYPE AS "Type"
	FROM AUTHOR AS A, BOOK AS C, PUBLISHER AS P,WRITES AS W
	WHERE W.ID_BOOK = C.ID_BOOK AND W.ID_AUTHOR = A.ID_AUTH
		  AND W.ID_AUTHOR=@idauthor AND C.ID_PUBLISHER = P.ID_PUB
	ORDER BY C.TITLE;

GO


CREATE FUNCTION DELAY_COST_BOOK (@returnDay DATE, @deadline DATE)
RETURNS INT
	BEGIN
		DECLARE @result INT;
		DECLARE @dayDiff INT;
		
		SET @dayDiff = DATEDIFF(day, @deadline, @returnDay);
		
		IF @dayDiff > 0
			SET @result = 1* @dayDiff;
		ELSE
			SET @result = 0;
		
		RETURN @result;
       END


GO


CREATE PROCEDURE CHANGE_AVAILABLE_NUMBER_BY @idBook INT, @n INT
AS
	UPDATE BOOK
	SET NUMBER_AVAILABLE = NUMBER_AVAILABLE + @n
	WHERE ID_BOOK = @idBook;


GO


CREATE PROCEDURE BOOK_RETURN_ENTRY @idBook INT, @idMember INT
AS
	DECLARE @returnDate DATE, @deadline DATE, @cost INT;

	SELECT @deadline = DATE_DEADLINE
	FROM LOAN
	WHERE ID_BOOK = @idBook AND ID_M = @idMember

	SET @returnDate = GETDATE();
	SELECT @cost = dbo.DELAY_COST_BOOK(@returnDate,@deadline)

	UPDATE LOAN
		SET DELAY_COST = @cost, DATE_RETURN =@returnDate
		WHERE ID_BOOK = @idBook AND ID_M = @idMember

	--increment available number
	EXEC dbo.CHANGE_AVAILABLE_NUMBER_BY @idBook=@idBook,@n=1

GO


CREATE PROCEDURE MEMBERSHIP_RENEWAL @idMember INT
AS
	UPDATE LIB_MEMBER
	SET DATE_OF_PAYMENT = GETDATE()
	WHERE ID_M = @idMember;


GO

CREATE PROCEDURE REMOVE_MEMBER @idMember INT
AS
	DELETE FROM LIB_MEMBER
	WHERE ID_M = @idMember;


GO 


CREATE PROCEDURE REMOVE_BOOK @idBook INT
AS
	DELETE FROM BOOK
	WHERE ID_BOOK = @idBook;


GO

CREATE PROCEDURE REMOVE_LOAN @idBook INT, @idMember INT
AS
	DELETE FROM LOAN
	WHERE ID_BOOK = @idBook AND ID_M = @idMember;

GO



CREATE TRIGGER ADD_LOAN
ON LOAN FOR INSERT,UPDATE
AS
	DECLARE @dateLoan DATE, @deadline DATE, @idBook INT, @idMember INT;
	
	SELECT @idBook=ID_BOOK, @idMember=ID_M, @dateLoan = DATE_LOAN, @deadline = DATE_DEADLINE
	FROM inserted
	
	IF DATEDIFF(day,@dateLoan, @deadline) <> 14 
		BEGIN
			SET @deadline= DATEADD(day, 14, @dateLoan);
		
			UPDATE LOAN
			SET DATE_DEADLINE =@deadline
			WHERE  ID_BOOK=@idBook AND ID_M=@idMember
		END
		
	--decrement number of available
	EXEC dbo.CHANGE_AVAILABLE_NUMBER_BY @idBook=@idBook, @n=-1

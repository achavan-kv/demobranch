-- bad-user-query.sql

CREATE PROCEDURE GetUser
    @UserId NVARCHAR(50)
AS
BEGIN

    DECLARE @Sql NVARCHAR(MAX)

    SET @Sql = '
        SELECT *
        FROM Users
        WHERE UserId = ''' + @UserId + '''
    '

    EXEC(@Sql)

END

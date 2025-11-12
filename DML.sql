SELECT * FROM Movies;
SELECT * FROM Genres;
SELECT * FROM Directors;
SELECT * FROM Actors;
SELECT * FROM Audiences;
SELECT * FROM AudienceReviews;
SELECT * FROM Movies_has_Directors;
SELECT * FROM Movies_has_Actors;-- Select all Users
SELECT * FROM Movies;

-- Select all Genres
SELECT * FROM Genres;

-- Select all Directors
SELECT * FROM Directors;

-- Select all Actors
SELECT * FROM Actors;

-- Audiences

-- Select all Audiences
SELECT * FROM Audiences;

-- Insert into Audiences
INSERT INTO
    Audiences (
        firstName,
        lastName,
        middleName,
        email
    )
VALUES (
        @firstName,
        @lastName,
        @middleName,
        @email
    );

-- Update into Audiences
UPDATE Audiences
SET
    firstName = @firstName,
    lastName = @lastName,
    middleName = @middleName,
    email = @emails
WHERE
    idAudience = @idAudience;

-- Delete Audiences
DELETE FROM Audiences WHERE idAudience = @idAudience;

-- Select all AudienceReviews
SELECT * FROM AudienceReviews;

-- Insert into AudiencesReviews
INSERT INTO
    AudiencesReviews (review, stars)
VALUES (@review, @stars);

-- Update into AudiencesReviews
UPDATE Audiences
SET
    review = @review,
    stars = @stars
WHERE
    idAudienceReview = @idAudienceReview;

-- Delete AudiencesReviews
DELETE FROM AudiencesReviews
WHERE
    idAudienceReview = @idAudienceReview;

-- Select all Movies_has_Directors
SELECT * FROM Movies_has_Directors;

-- Select all Movies_has_Actors
SELECT * FROM Movies_has_Actors;
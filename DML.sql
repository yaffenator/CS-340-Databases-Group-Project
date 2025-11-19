-- Movies

-- Select all Movies
SELECT * FROM Movies;

-- Update Movie
UPDATE Movies
SET
    title = @title,
    releaseYear = @releaseYear,
    description = @description,
    averageRating = @averageRating
WHERE
    idMovie = @idMovie;

-- Delete Movie
DELETE FROM Movies WHERE idMovie = @idMovie;

-- Selecting specific Movie
SELECT * FROM Movies WHERE idMovie = @idMovie;

-- Genres

-- Select all Genres
SELECT * FROM Genres;

-- Directors

-- Select all Directors
SELECT * FROM Directors;

-- Insert into Directors
INSERT INTO Directors (firstName, lastName, middleName) VALUES (@firstName, @lastName, @middleName);

-- Delete Director
DELETE FROM Directors WHERE idDirector = @idDirector;

-- Update Director
UPDATE Directors SET firstName = @firstName, lastName = @lastName, middleName = @middleName WHERE idDirector = @idDirector;

-- Selecting specific Directors
SELECT * FROM Directors WHERE idDirector = @idDirector;

-- Actors

-- Select all Actors
SELECT * FROM Actors;

-- Insert into Actors
INSERT INTO Actors (firstName, lastName, middleName) VALUES (@firstName, @lastName, @middleName);

-- Delete Actor
DELETE FROM Actors WHERE idActor = @idActor;

-- Update Actor
UPDATE Actors SET firstName = @firstName, lastName = @lastName, middleName = @middleName WHERE idActor = @idActor;

-- Selecting specific Actor
SELECT * FROM Actors WHERE idActor = @idActor;

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

-- Update Audience
UPDATE Audiences
SET
    firstName = @firstName,
    lastName = @lastName,
    middleName = @middleName,
    email = @emails
WHERE
    idAudience = @idAudience;

-- Delete Audience
DELETE FROM Audiences WHERE idAudience = @idAudience;

-- Selecting specific Audience
SELECT * FROM Audiences WHERE idAudience = @idAudience;

-- Audience Reviews

-- Select all AudienceReviews
SELECT * FROM AudienceReviews;

-- Insert into AudiencesReviews
INSERT INTO AudienceReviews (idMovie, idAudience, review, stars) VALUES (@idMovie, @idAudience, @review, @stars);

-- Update into AudiencesReviews
UPDATE AudienceReviews SET review = @review, stars = @stars WHERE idAudienceReview = @idAudienceReview;

-- Delete AudiencesReviews
DELETE FROM AudienceReviews WHERE idAudienceReview = @idAudienceReview;

-- Select specific Audience Review
SELECT * FROM AudienceReviews WHERE idAudienceReview = @idAudienceReview;

-- Select all Movies_has_Directors
SELECT * FROM Movies_has_Directors;

-- Select all Movies_has_Actors
SELECT * FROM Movies_has_Actors;
-- -----------------------------------------------------
-- Autors: Ayowade Owojori, Noam Yaffe
-- Title: Project Group 40 Step 2 DDL Draft
-- Date: October 30, 2025
-- -----------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

SET AUTOCOMMIT = 0;

-- -----------------------------------------------------
-- Genres Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Genres`;

CREATE TABLE Genres (
    idGenre INT AUTO_INCREMENT NOT NULL UNIQUE,
    category VARCHAR(30) NOT NULL,
    PRIMARY KEY (idGenre)
);

INSERT INTO
    Genres (category)
VALUES ("Action"),
    ("Sci-Fi"),
    ("Family");

-- -----------------------------------------------------
-- Genres Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Movies`;

CREATE TABLE Movies (
    idMovie INT AUTO_INCREMENT NOT NULL UNIQUE,
    title VARCHAR(145) NOT NULL,
    releaseYear YEAR NOT NULL,
    idGenre INT NOT NULL,
    description VARCHAR(300) NOT NULL,
    averageRating DECIMAL(3, 1) NOT NULL,
    PRIMARY KEY (idMovie),
    FOREIGN KEY (idGenre) REFERENCES Genres (idGenre) ON DELETE CASCADE
);

INSERT INTO
    Movies (
        title,
        releaseYear,
        idGenre,
        description,
        averageRating
    )
VALUES (
        "Spider-Man: Across the Spider Verse",
        2023,
        (
            SELECT idGenre
            FROM Genres
            WHERE
                category = "Sci-Fi"
        ),
        "Spider-Man animated movies about Miles Morales",
        9.5
    ),
    (
        "Avengers: Endgame",
        2019,
        (
            SELECT idGenre
            FROM Genres
            WHERE
                category = "Action"
        ),
        "End of the Avengers seiries",
        8.7
    ),
    (
        "UP",
        2009,
        (
            SELECT idGenre
            FROM Genres
            WHERE
                category = "Family"
        ),
        "A movie about a boy who met an old man and flew in his house with balloons",
        8.8
    );

-- -----------------------------------------------------
-- Directors Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Directors`;

CREATE TABLE Directors (
    idDirector INT AUTO_INCREMENT NOT NULL UNIQUE,
    firstName VARCHAR(45) NOT NULL,
    lastName VARCHAR(45) NOT NULL,
    middleName VARCHAR(45),
    PRIMARY KEY (idDirector)
);

INSERT INTO
    Directors (
        firstName,
        lastName,
        middleName
    )
VALUES ("Joaquim", "Dos Santos", NULL),
    ("Kemp", "Powers", NULL),
    ("Justin", "Thompson", "Kent");

-- -----------------------------------------------------
-- Actors Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Actors`;

CREATE TABLE Actors (
    idActor INT AUTO_INCREMENT NOT NULL UNIQUE,
    firstName VARCHAR(45) NOT NULL,
    lastName VARCHAR(45) NOT NULL,
    middleName VARCHAR(45),
    PRIMARY KEY (idActor)
);

INSERT INTO
    Actors (
        firstName,
        lastName,
        middleName
    )
VALUES ("Shameik", "Moore", NULL),
    ("Hailee", "Steinfeld", NULL),
    ("Brian", "Henry", "Tyree");

-- -----------------------------------------------------
-- Audiences Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Audiences`;

CREATE TABLE Audiences (
    idAudience INT AUTO_INCREMENT NOT NULL UNIQUE,
    firstName VARCHAR(45) NOT NULL,
    lastName VARCHAR(45) NOT NULL,
    middleName VARCHAR(45),
    email varchar(145) NOT NULL,
    PRIMARY KEY (idAudience)
);

INSERT INTO
    Audiences (
        firstName,
        lastName,
        middleName,
        email
    )
VALUES (
        "John",
        "Adams",
        NULL,
        "Adamsj@OSU.edu"
    ),
    (
        "Adam",
        "James",
        "Curry",
        "Jamesadam@OSU.edu"
    ),
    (
        "Jawan",
        "Curry",
        NULL,
        "Curryjaw@OSU.edu"
    );

-- -----------------------------------------------------
-- AudienceReviews Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `AudienceReviews`;

CREATE TABLE AudienceReviews (
    idAudienceReview INT AUTO_INCREMENT NOT NULL UNIQUE,
    idMovie INT NOT NULL,
    idAudience INT NOT NULL,
    review VARCHAR(300) NOT NULL,
    stars TINYINT NOT NULL CHECK (stars BETWEEN 1 AND 5),
    PRIMARY KEY (idAudienceReview),
    FOREIGN KEY (idMovie) REFERENCES Movies (idMovie) ON DELETE CASCADE,
    FOREIGN KEY (idAudience) REFERENCES Audiences (idAudience) ON DELETE CASCADE
);

INSERT INTO
    AudienceReviews (
        review,
        idMovie,
        idAudience,
        stars
    )
VALUES (
        "This movie is life-changing!",
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idAudience
            FROM Audiences
            WHERE
                firstName = "John"
                AND lastName = "Adams"
        ),
        5
    ),
    (
        "Mid",
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idAudience
            FROM Audiences
            WHERE
                firstName = "Adam"
                AND lastName = "James"
        ),
        3
    ),
    (
        "Hate the cliff-hanger, for that 1 star.",
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idAudience
            FROM Audiences
            WHERE
                firstName = "Jawan"
                AND lastName = "Curry"
        ),
        1
    );

-- -----------------------------------------------------
-- Movies_has_Actors Intersection Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Movies_has_Actors`;

CREATE TABLE Movies_has_Actors (
    idMovies_has_Actors INT AUTO_INCREMENT NOT NULL UNIQUE,
    idMovie INT NOT NULL,
    idActor INT NOT NULL,
    PRIMARY KEY (idMovies_has_Actors),
    FOREIGN KEY (idMovie) REFERENCES Movies (idMovie) ON DELETE CASCADE,
    FOREIGN KEY (idActor) REFERENCES Actors (idActor) ON DELETE CASCADE,
    CONSTRAINT movie_actor UNIQUE (idMovie, idActor)
);

INSERT INTO
    Movies_has_Actors (idMovie, idActor)
VALUES (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idActor
            FROM Actors
            WHERE
                firstName = "Shameik"
                AND lastName = "Moore"
        )
    ),
    (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idActor
            FROM Actors
            WHERE
                firstName = "Hailee"
                AND lastName = "Steinfeld"
        )
    ),
    (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idActor
            FROM Actors
            WHERE
                firstName = "Brian"
                AND lastName = "Henry"
                AND middleName = "Tyree"
        )
    );

-- -----------------------------------------------------
-- Movies_has_Directors Intersection Table & Insert Values
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Movies_has_Directors`;

CREATE TABLE Movies_has_Directors (
    idMovies_has_Directors INT AUTO_INCREMENT NOT NULL UNIQUE,
    idMovie INT NOT NULL,
    idDirector INT NOT NULL,
    PRIMARY KEY (idMovies_has_Directors),
    FOREIGN KEY (idMovie) REFERENCES Movies (idMovie) ON DELETE CASCADE,
    FOREIGN KEY (idDirector) REFERENCES Directors (idDirector) ON DELETE CASCADE,
    CONSTRAINT movie_directors UNIQUE (idMovie, idDirector)
);

INSERT INTO
    Movies_has_Directors (idMovie, idDirector)
VALUES (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idDirector
            FROM Directors
            WHERE
                firstName = "Joaquim"
                AND lastName = "Dos Santos"
        )
    ),
    (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idDirector
            FROM Directors
            WHERE
                firstName = "Kemp"
                AND lastName = "Powers"
        )
    ),
    (
        (
            SELECT idMovie
            FROM Movies
            WHERE
                title = "Spider-Man: Across the Spider Verse"
        ),
        (
            SELECT idDirector
            FROM Directors
            WHERE
                firstName = "Justin"
                AND lastName = "Thompson"
        )
    );

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;
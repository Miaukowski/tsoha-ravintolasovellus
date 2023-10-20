
-- Stores users, has column for deletion
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    deleted BOOLEAN DEFAULT FALSE  
);


-- Stores restaurants
CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    average_rating NUMERIC(3, 2) DEFAULT 0.00
);

-- Stores reviews with a foreign key reference to restaurants
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL,
    rating INT NOT NULL,
    review_text TEXT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

-- Stores hashtags
CREATE TABLE hashtags (
    id SERIAL PRIMARY KEY,
    hashtag_text VARCHAR(50) UNIQUE NOT NULL
);

-- Aassociates restaurants with hashtags
CREATE TABLE restaurant_hashtags (
    id SERIAL PRIMARY KEY,
    restaurant_id INT NOT NULL,
    hashtag_id INT NOT NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (hashtag_id) REFERENCES hashtags(id)
);
-- Associates reviews with hastags
CREATE TABLE review_hashtags (
	id SERIAL PRIMARY KEY, 
	review_id INT NOT NULL,
	hashtag_id INT NOT NULL,
	FOREIGN KEY (review_id) REFERENCES reviews(id),
	FOREIGN KEY (hashtag_id) REFERENCES hashtags(id) 
);


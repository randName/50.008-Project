/* ITEMS */

CREATE TABLE category(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE creator(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE company(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE item(
    id INTEGER AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date_created DATE,
    company_id INTEGER,
    price NUMERIC(10,2),
    quantity INTEGER,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

CREATE TABLE item_category(
    item_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE CASCADE,
    PRIMARY KEY (item_id, category_id)
);

CREATE TABLE item_creator(
    item_id INTEGER,
    creator_id INTEGER,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    FOREIGN KEY (creator_id) REFERENCES creator(id) ON DELETE CASCADE,
    PRIMARY KEY (item_id, creator_id)
);

/* FEEDBACK */

CREATE TABLE feedback(
    id INTEGER AUTO_INCREMENT,
    item_id INTEGER,
    user_id INTEGER,
    score INTEGER NOT NULL,
    review TEXT NOT NULL,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    PRIMARY KEY (id, item_id, user_id)
);

CREATE TABLE rating(
    user_id INTEGER,
    feedback_id INTEGER,
    usefulness INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    FOREIGN KEY (feedback_id) REFERENCES feedback(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, feedback_id)
);

/* ORDERS */

CREATE TABLE purchase(
    id INTEGER AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    ordered DATETIME NOT NULL,
    total NUMERIC(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    PRIMARY KEY (id)
);

CREATE TABLE purchase_item(
    purchase_id INTEGER,
    item_id INTEGER,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (purchase_id) REFERENCES purchase(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    PRIMARY KEY (purchase_id, item_id)
);

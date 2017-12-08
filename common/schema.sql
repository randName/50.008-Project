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
    item_id INTEGER,
    user_id INTEGER,
    made_on DATETIME NOT NULL,
    score INTEGER NOT NULL,
    review TEXT NOT NULL,
    CONSTRAINT score_range CHECK (score >= 0 AND score <= 10),
    FOREIGN KEY (item_id) REFERENCES item(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    PRIMARY KEY (item_id, user_id)
);

CREATE TABLE rating(
    item_id INTEGER,
    user_id INTEGER,
    rater_id INTEGER,
    usefulness INTEGER NOT NULL,
    CONSTRAINT no_self_rate CHECK (user_id <> rater_id),
    CONSTRAINT useful_range CHECK (usefulness >= 0 AND usefulness <= 2),
    FOREIGN KEY (item_id, user_id) REFERENCES feedback(item_id, user_id) ON DELETE CASCADE,
    FOREIGN KEY (rater_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    PRIMARY KEY (item_id, user_id, rater_id)
);

/* ORDERS */

CREATE TABLE purchase(
    id INTEGER AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    made_on DATETIME NOT NULL,
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

/* TRIGGERS */

DELIMITER |
CREATE TRIGGER subtract_quantity AFTER INSERT ON purchase_item
 FOR EACH ROW BEGIN
      UPDATE item
      SET item.quantity =  GREATEST(0, item.quantity - NEW.quantity)
      WHERE item.id = NEW.id
      and item.quantity > 0;
 END; |
DELIMITER ;

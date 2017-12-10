# Solid Eureka
![Solid Eureka's Landing Page](img/landing_page.png)
Solid Eureka is a web application with a database backend built using Django with the implemented
features described below.

## Features
A few things that are implemented in Solid Eureka:
* Registration
![Solid Eureka's Registration Page](img/registration.png)
* Feedback (Reviews)
![Solid Eureka's Feedback Page](img/item_information.png)
* Browsing (Search) & Usefulness rating
![Solid Eureka's Browsing & Usefulness Page](img/search_item.png)
* Ordering
![Solid Eureka's Ordering Page](img/cart.png)
* Recommendation
![Solid Eureka's Recommendation Page](img/recommendation.png)
* User Record
![Solid Eureka's User Page](img/user.png)
* Inventory management
![Solid Eureka's Inventory Management Page](img/inventory_management.png)
* Statistics
![Solid Eureka's Statistics Management Page](img/statistics.png)

## Getting Started

### Prerequisites

What you need to install and how to install them

```
# MariaDB
sudo apt-get install mariadb-server libmysqlclient-dev
sudo mysql_secure_installation

# Pipenv
pip install pipenv
pipenv --python 3.6
pipenv install

# configure and init database
cp .env.example .env
vi .env
pipenv run ./db.sh init

# webpack
npm install
npm build
```

## Built With

* [Vue](https://vuejs.org/) - Front-End framework used
* [Vuetify](https://vuetifyjs.com/) - Material Component Framework

* [Django](https://www.djangoproject.com/) - Back-End framework used

* [Web Pack](https://webpack.js.org/) - Dependency Management
* [npm](https://www.npmjs.com/) - Package Manager for JavaScript

* [MariaDB](https://mariadb.org/) - Open Source Relational Database


## Entity Relationship Diagram
![Alt text](img/er-diagram.jpeg "ER Diagram")

The relational schema SQL DDL code can be found [here](common/schema.sql)

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details

## Authors

* [Shun Git](https://github.com/randName)
* [Guo Yuan Jing](https://github.com/guoyuanjing2988)
* Jiang Tao
* Wang Shuo
* Lee Yue Ning
* [Ong Wei Jie Joel](https://github.com/joelowj)

## Acknowledgments
* Dorien Herremans
* [Jon Wong](https://github.com/jon-wong-sutd) guidance on Agile software development and inspiration to adopt a design thinking approach to Software Development for this project

# 50.008 Database Project
Development of database-based system in Django

# Features

## Registration
Using Django's auth mode and session DB module.

## Feedback (Reviews)
- Date, Score (0 to 10), Optional text
- One feedback per user per item
- No changes allowed

## Usefulness rating
- 0 (Useless), 1 (Useful), 2 (Very Useful)
- One rating per user per feedback
- Not allowed to rate own feedback

## Feedback query
- Retrieve top N useful feedbacks
- Ranked by average usefulness
- N specified by user

## Browsing (Search)
- Allow conjunctive queries on all combinations of fields
- Allow sorting by year or average feedback score

## Ordering
- A user is able to order items in any quantity and type
- Payment and Delivery not implemented

## Reccomendation
- Upon ordering item A, suggest item B if there exists a user that bought both A and B
- Sorted by sales to users who bought both items

## User Record
Upon request, display current user's:
- Account Information
- Order History
- Feedback History
- List of others' Feedback rated by current user

## Inventory management
- Addition of new items
- Arrival of stock

## Statistics
Every month, generate rankings based on sales for that month:
- List of N most popular books 
- List of N most popular authors
- List of N most popular publishers

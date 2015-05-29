=====
sqlew
=====
.. image:: https://travis-ci.org/tomokinakamaru/sqlew.svg?branch=master
    :target: https://travis-ci.org/tomokinakamaru/sqlew
    :alt: sqlew Build

About
=====

PEP 249 compat DB client wrapper & query formatting.

Examples
========

.. sourcecode:: python

    from sqew import Client

    cli = Client(user='user',
                 password='password',
                 host='127.0.0.1',
                 db='sqlew_test')

    # blog post data
    blog_post = {'title': 'My First Post',
                 'content': 'Hello World!',
                 'create_datetime': lambda: 'NOW'}

    # insert query
    q = 'INSERT INTO blog_posts (::keys) VALUES (:vals)'

    # execute & commit
    # > INSERT INTO blog_posts (title, content, create_datetime)
    # > VALUES ('My First Post', 'Hello World', NOW())
    cli.exes(q,
             keys=blog_post.keys(),
             vals=blog_post.vals).commit()

    # select query
    q = 'SELECT * FROM blog_posts LIMIT :offset, 10'

    # execute and get result rows as a list
    # > SELECT * FROM blog_posts LIMIT 0, 10
    posts = cli.exew(q, offset=0).all()


Documentation
=============

Under construction...

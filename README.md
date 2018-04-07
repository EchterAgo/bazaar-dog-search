# bazaar-dog-search

[![Build Status](https://travis-ci.org/BazaarDog/bazaar-dog-search.svg?branch=master)](https://travis-ci.org/BazaarDog/bazaar-dog-search)


## requirements


```
# debian-based system requirements
sudo apt-get install python3-pip git sqlite3
```

In addition, you'll need a running node of openbazaar-go, either locally or configured securely
somewhere else. Parameters to connect are stored in [postactivate](postactivate).

## install


```
# get the code

git clone https://github.com/BazaarDog/bazaar-dog-search.git
cd bazaar-dog-search


# install a python3 virtual environment

pip3 install virtualenv
virtualenv ~/.bazaar_dog_venv
source ~/.bazaar_dog_venv/bin/activate

source postactivate

# install project requirements

pip install -r requirements.txt

./manage.py makemigrations ob
./manage.py migrate
./manage.py bootstrap
./manage.py runserver

```

## Usage


### Configuration

In order to keep passwords and local configurations out of harms way, one approach is to store them in environment
variables. Currently configuration variables are stored in [postactivate](postactivate), the base configuration
assumes a `openbazaar-go` server on localhost:4003 with no auth or ssl.

In the future, these variables will likely move to an ansible-vault type configuration.


### Bootstrapping

A management command is provided to bootstrap a node. It uses a list of peers stored in [custom.py](custom.py) in
the variable `the_champions_of_decentralized_commerce`.

It can be run from the project directory in the python virtual environment with like so:

```
./manage.py bootstrap
```

It should spew an inordinate amount of text and load the profiles, listings & reviews of those
peers into the database. It can be rerun if it fails without duplicating all the crawling already done.

In addition to the list of 'safe' peerIDs, it also loads their moderators, reviewers, etc, *so* **the resulting
database may contain content that is NSFW, or illegal in your area.**


### Local Testing, Port Binding, faux-DNS

The OpenBazaar reference client prefers search engines on real domain names and not 'localhost' or '127.0.0.1',
So the easiest approach is to fake it by mapping the development port to a standard port (80/443) and fake the dns.

On a debian based system, following will map your development port from 8000 to 80

```bash
sudo iptables -t nat -I PREROUTING --src 0/0 --dst 127.0.0.1 -p tcp --dport 80 -j REDIRECT --to-ports 8000
sudo iptables -t nat -I OUTPUT --src 0/0 --dst 127.0.0.1 -p tcp --dport 80 -j REDIRECT --to-ports 8000
```

For the purposes of testing, `admin.bazaar.dog` can be pointed at your localhost in your /etc/hosts file or dns.

If you choose something else for your domain name, be sure to add it to `ALLOWED_HOSTS` in `settings`

### Internationalization

Translations are configured in [settings.base](bazaar_dog/settings/base.py) with source in locale, there are a few django-admin
commands that are useful for building international support

```bash
django-admin makemessages -a    # make all language po files for all languages in settings

#  alternatively
#  django-admin makemessages -l de # make just german po files
#  django-admin makemessages -l ko # create po files for Korean

django-admin compilemessages    # compile language files for use

```

### Common Valuations

OpenBazaar listings may be denominated in any currency, which is an issue when comparing apples to oranges.

For the purposes of sorting by price, it's useful to convert all listings to a common base currency and store
that price for speed and usability.

This is done by downloading exchange rates, and then converting all prices to a common currency (i.e. BCH), and storing
the price in a variable called `price_value` on the listing.

```

ob.util.get_exchange_rates()

ob.util.update_price_values()

```

The following function is provided as a convenience, it simply calls exchange rates, waits three seconds,
then calls update_price_values

```
ob.tasks.valuation.update_price_values()
```
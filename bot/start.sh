#!/bin/bash

alembic upgrade head

python bot/main.py
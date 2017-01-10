#!/bin/bash

dropdb poe_data
createdb poe_data
psql poe_data < po_data_schema.sql
python /Users/adam.green/Documents/workspace/poe-client/get-generic-data.py

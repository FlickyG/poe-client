#!/bin/bash

dropdb poe_data
createdb poe_data
psql poe_data < /tmp/tmp-schema

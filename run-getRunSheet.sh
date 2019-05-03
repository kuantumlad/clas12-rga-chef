#!/bin/bash

wget --no-check-certificate -O test.csv 'https://docs.google.com/spreadsheets/d/1g2L33OKvKVFMq3MNGYAuS02l0CCKomPbDm8iULLhueY/export?gid=79484812&format=csv'

mv test.csv newProductionSheet.csv

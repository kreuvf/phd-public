#!/bin/bash
xmllint --format $1 > $1.tmp && mv $1.tmp $1

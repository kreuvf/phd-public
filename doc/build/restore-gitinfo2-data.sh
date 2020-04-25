#!/bin/bash

if [ -f 'build/originalgitHeadInfo.gin' ]; then \
	cp --preserve build/originalgitHeadInfo.gin ../.git/gitHeadInfo.gin; \
	rm --force build/originalgitHeadInfo.gin; \
	echo "Git Data Faking: Restoring original data"; \
fi;

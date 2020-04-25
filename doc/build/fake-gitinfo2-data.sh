#!/bin/bash

CONFIG_FAKE_GIT='no'

if [ -f 'build/config' ]; then
	CONFIG_FAKE_GIT=`grep -E 'fake gitinfo2 data' build/config | sed -r -e 's/^fake gitinfo2 data: //'`;
fi;

if [ "$CONFIG_FAKE_GIT" = "yes" ]; then
	if [ -f 'build/fakegitHeadInfo.gin' ]; then
		if [ -f '../.git/gitHeadInfo.gin' ]; then
			cp --preserve ../.git/gitHeadInfo.gin build/originalgitHeadInfo.gin;
			echo "Git Data Faking: Original data backed up";
		fi;
		cp --preserve build/fakegitHeadInfo.gin ../.git/gitHeadInfo.gin;
		echo "Git Data Faking: Fake data put into place";
	fi;
fi;
#!/usr/bin/env bash

export PATH=/usr/local/bin:$PATH
mount='/usr/local/bin/mountlto ${1}'

eval $mount
echo "mounting . . ."
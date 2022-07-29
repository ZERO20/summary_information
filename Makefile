create-zip:
	cd venv/lib/python3.9/site-packages \
	&& zip -r ${OLDPWD}/function.zip . \
	&& cd ${OLDPWD} \
	&& zip -g function.zip lambda_function.py \
	summaries_information/* \
	db/*
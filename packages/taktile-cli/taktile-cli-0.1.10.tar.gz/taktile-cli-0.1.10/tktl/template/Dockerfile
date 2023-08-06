FROM taktile/base-serving-api:c4509ad5e3c7ce779f74476fdbb869adc4894b1b
ENV APPDIR /app

# Install requirements
COPY ./requirements.txt ${APPDIR}/user_requirements.txt
RUN pip install -r ${APPDIR}/user_requirements.txt

# Copy code and assets for running the application
COPY ./src ${APPDIR}/src
COPY ./assets ${APPDIR}/assets
COPY ./tests ${APPDIR}/user_tests

# Run model profile
RUN python ${APPDIR}/profile_endpoints.py

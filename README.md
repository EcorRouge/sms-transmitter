# sms-transmitter
A general SMS transmitter that can use various services to send SMS messages

# Environment variables

The following instructions are for running the service standalone for testing and SMS verification

Copy `.env.example` file to `.env` file, Keep the EVs as-is, apart from the following three.

`SMS_PROVIDER="twilio"` - This is where you provide the name of the SMS provider, currently, only `twilio` is supported.

If you have selected `twilio` as the SMS provider then, you have to fill in the following two EVs as well.

`TWILIO_ACCOUNT_SID=`
`TWILIO_AUTH_TOKEN=`


# Config.json

Go to your SMS provider dashboard and configure your SMS settings. For Twilio, you'll need to set up a phone number or messaging service.

- Note the sender phone number and create an event in config.json. For example, I have configured SMS settings like this

- And to send SMS using this template I have added the following event in the `src/config.json` file

```json
"TEST_SMS_EVENT": {
    "type": "SMS",
    "template": "Hi {{ name }}, Your test SMS code is {{ code }}."
},
```

# Docker & Docker Compose

A `docker-compose.yml` file is available in the code just for testing this service against rabbitmq. 
In practice, only the docker image of the service will be built & used

### Run services
- `docker-compose build --no-cache` - this will build the image from ground up 
using the latest `ecorrouge/rococo-service-host` base image.

- `docker-compose up -d` - this will run the `rabbitmq` & `sms-transmitter` services

## Monitoring
- Run the following command to see the logs of the `sms-transmitter` and verify that it received messages, 
processed them, and sent SMS using `twilio` provider

```shell
docker compose logs sms_transmitter
```

- Open your Twilio dashboard and verify that SMS messages were sent to the corresponding phone numbers

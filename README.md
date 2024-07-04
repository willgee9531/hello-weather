# hello-weather

A basic web server using Flask that exposes an API endpoint that conforms to this criteria below:\n
Endpoint: [GET] <example.com>/api/hello?visitor_name="Mark" (where <example.com> is the server origin)\n
Response:\n
```
{
  "client_ip": "127.0.0.1", // The IP address of the requester
  "location": "New York" // The city of the requester
  "greeting": "Hello, Mark!, the temperature is 11 degrees Celcius in New York"
}
```
---
Try it out:\n
https://hello-weather.koyeb.app/api/hello?visitor_name="Mark"\n\n
NB: This API receives as argument the visitor's name

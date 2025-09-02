#!/bin/bash


curl --request POST http://localhost:5000/api/timeline_post \
  -d "name=Wei" \
  -d "email=wei.he@mlh.io" \
  -d "content=Just Added Database to my portfolio site!"


curl --request POST http://localhost:5000/api/timeline_post \
  -d "name=Wei" \
  -d "email=wei.he@mlh.io" \
  -d "content=Testing my endpoints with postman and curl."


curl http://localhost:5000/api/timeline_post

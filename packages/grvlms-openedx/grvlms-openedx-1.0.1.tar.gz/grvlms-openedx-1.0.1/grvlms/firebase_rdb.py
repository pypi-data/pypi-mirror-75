import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os

PROJECT_ID = "grvlms"
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "grvlms",
  "private_key_id": "41a5ee79442a0d8146480679119d9eaadc133737",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCeSZmW4PeIOJ9J\nZiLA5FGBCTuUE5yzZulIlRcL3bB8knskgXgZrZN8kUceiEfuhJlwU7TIUqTBk3S0\nOlXRLVdgBDjIXelxlOhYA+9JEZYRBO7IPg9TEMcW3Ls0pIUNXxxDadbi0EzEKLgp\nkQnrHqsMaChyCAi50Op/0MSwjuwjJFhtHkPmapX34Bx7wXgk9bxiMaz6+DoaH7bQ\nv5HAXJGMy/xXpOi8hWYi48i3ONl3yPW51Wzs1MOu20JvmQSFqn4/+v6DA5cR89EO\nYC6YUH6hAPvM6KsHp5MHxU5otmgV5xtv5oTEjEWYdVPn4ZZmM3qJSADOm1mn8dOp\nOqCzOOJdAgMBAAECggEABAY+ha/EE15PLHRQk2NqsBNuRJpIDGakLUB/JMHW7B/k\nSh4RkeOQIaVm77+KxqVv6kNyj/pL7pEDcVafWnFi7JHG6M88cXMWAjDda1frXxTn\nRkePp67ARRRJHTJGoLunkg41lLAzl3QqlIH3xNbThf3680VBhYnqgGPsMEn99nm6\nmFf2jQQA7LQOKPf7yiY0alxdTowAtM3sK9ZtCCd44l3q3tI0qpYEjVVNnH3v6vmv\n/G3fV66VrfR2YjdSY2RVkXL90OX/j8WuFnTKd5i2vPvDJtorgmIrBi7Hy5LBVbrw\nUG41AtcGAIwumsSOxiuysMc5sCMrmZ5YLIjimr3VSQKBgQDRZoWHl1IoTHlw5b3N\n4LGsrsjTJ217EpaDco6XLALfCJqr7vMNc0cAnwR0rsxntop91bczHL9il49iIF72\nzccJsYgK4xk5syNI8fsX9+t0PiiRWPy4KRZ4huxFqQZZycAnjCmQXV85TniDc4FG\n2zULWgldlsFBAlAA20I7jk/lVQKBgQDBgzA9QNZL1liYTPnBD8LDwUVVrCm5Gwc5\n7zYH0YlH6oIDvsJMPgnK5qVMxD024um+H9QNtdKRXaQW5odu0seJo1+DmcxpUAc1\nxziVW2vw95E42TJf8chjnqUvQfcgsqnsMHorXCWowkIU8lW0BpmrOO/ThSdg2eCx\nhaLMD/yI6QKBgGEOS8XU9VeIWqFhWuAZzUBkouB73dq1et3iMwUOeSY3LrmSP0V0\nsOwwyDfs7QEFMpuwewFNycdAyEyLBHkQV7i+eHfTWtXLmgctYVxypMd0KAl2XWxe\nXvPuVYTUGwVy5YVvCbTIEmLVZDZJSxo0cBma2cxvG5OuJra+6awBAjchAoGANrL7\nhsT2DjfHkT1o956Z4jWWgLIKlS1DrKemcS1UjcSG/cIFMAH1SKpLnVh3KTWY9soO\nadW0cKy0flipfbUM/CX3EL7/neEmOJhYsTdHWrTQEu6qI563kxk7/hC6Zz65c278\niZchegN3JG6ftSSMeW69s9+WkvTjY6qvqtj1/EkCgYEAvrWxg7XamgiNqv7YF61F\nbiSVxsdVhMhmJlZF+BpASk7OK57qHrBZn/wZQXMe0KeJDKdMFeELHjsRxeK1t7Gc\n12PWK7MDDxBZ3WCSTAC9yM96s554cWa0QWF9eXIwKy7jmsuy+xFAUl/tybd3FFfd\nk7e+1s/ZdjVj74SypO26/as=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-pfyk4@grvlms.iam.gserviceaccount.com",
  "client_id": "114302582580251716091",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-pfyk4%40grvlms.iam.gserviceaccount.com"
}
)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://{}.firebaseio.com/'.format(PROJECT_ID)
})

def get(ref):
  return db.reference(ref).get()


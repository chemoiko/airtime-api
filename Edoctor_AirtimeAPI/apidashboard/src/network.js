const axios = require('node-fetch');

function login()
{
    const url = 'https://edoct-android-app-intern.vercel.app/airtime/api/auth/login';
    
    const requestOptions = {
                                method: 'POST',
                                headers: {
                                            'Content-Type': 'application/json'
                             },
                                body: JSON.stringify(postData)
                            };
    console.log("hello");
    fetch(url, requestOptions)
  .then(response => response.json())
  .then(data => {
    console.log('Response:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

login();